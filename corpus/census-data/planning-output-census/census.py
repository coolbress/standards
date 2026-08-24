#!/usr/bin/env python3
"""planning-output-census — Mode A (per-repo SAMPLED census).

Empirically grounds gingoa's PLANNING/SPEC output standard by measuring, across a sample of
high-star GitHub repos, the PER-REPO PREVALENCE of planning/spec artifacts (ADRs, feature specs,
PRD, requirements/roadmap/RFC/changelog, spec-driven tool dirs, agent constitutions, docs/).

Method (Mode A, deterministic): sample top-starred repos via `gh search repos` across an all-language
slice + per-language slices + topic slices, dedupe, then for EACH repo fetch the recursive file tree
ONCE (`gh api repos/{repo}/git/trees/HEAD?recursive=1`) and regex-detect each artifact by path.
Tally % of repos with each. Also a small code-search supplement (Mode B) corroborates with raw
global filename/path counts.

Run from repo root:
  python docs/research/census-data/planning-output-census/census.py sample    # -> sample.json
  python docs/research/census-data/planning-output-census/census.py harvest   # -> records.json
  python docs/research/census-data/planning-output-census/census.py stats      # -> stats.json + tally.csv
  python docs/research/census-data/planning-output-census/census.py codesearch # -> codesearch.json (rate-limited)

Caveats: GitHub star-count != quality; planning artifacts often live in wikis/issues/external trackers
(this UNDER-counts those); tree fetch is default-branch HEAD only; truncated trees (>100k entries / >7MB)
are flagged and counted as best-effort; code-search API is auth-gated, indexes a subset, total_count
approximate. Sample size is modest (target 150-300). Read percentages as directional.
"""
import csv, json, os, re, subprocess, sys, time
from collections import Counter

ROOT = 'docs/research/census-data/planning-output-census'
SAMPLE = f'{ROOT}/sample.json'
REC = f'{ROOT}/records.json'

# Language slices keep it from being all mega-libraries; topic slices add framework/cli flavor.
LANGS = ['typescript', 'python', 'go', 'rust', 'javascript', 'java', 'c++', 'ruby', 'shell']
TOPICS = ['framework', 'cli']
ALL_LIMIT = 100   # all-language top-starred
LANG_LIMIT = 30   # per language slice
TOPIC_LIMIT = 30  # per topic slice
STAR_FLOOR = '>500'

# Artifact detectors — matched against the newline-joined list of tree paths (case-insensitive, multiline).
# Each key is an artifact family; the regex is ANY path that evidences it.
P = {
    # ADRs / decision records
    'adr': r'(^|/)(docs?/adr|adr|docs?/decisions)/',
    # Feature specs dir
    'specs_dir': r'(^|/)(docs?/specs?|specs?)/',
    # PRD
    'prd': r'(^|/)(prd\.md|.*product[-_ ]requirements.*\.md|docs?/prd\.md)$',
    # requirements.md (any location)
    'requirements_md': r'(^|/)requirements\.md$',
    # ROADMAP.md
    'roadmap': r'(^|/)roadmap\.md$',
    # RFCs (dir or RFC-named files)
    'rfc': r'(^|/)(rfcs?|docs?/rfcs?)/|(^|/)rfc[-_]?\d',
    # CHANGELOG.md
    'changelog': r'(^|/)changelog(\.md|\.rst|\.txt)?$',
    # Spec-driven tool dirs
    'speckit': r'(^|/)\.specify/',
    'kiro': r'(^|/)\.kiro/',
    'openspec': r'(^|/)openspec/',
    # Agent constitutions
    'agents_md': r'(^|/)agents\.md$',
    'claude_md': r'(^|/)claude\.md$',
    # any docs/ dir at all
    'docs_dir': r'(^|/)docs?/',
}
FOUND = {k: re.compile(v, re.I | re.M) for k, v in P.items()}
KEYS = list(P.keys())


def run(args, timeout=60):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    return (p.stdout, None) if p.returncode == 0 else (None, (p.stderr or '').strip())


def gh_json(path, timeout=60):
    for attempt in (1, 2):
        out, err = run(['gh', 'api', path], timeout=timeout)
        if out is not None:
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                return None
        if err and ('rate limit' in err.lower() or 'secondary' in err.lower()) and attempt == 1:
            time.sleep(25); continue
        return None


def search(extra, limit):
    args = ['gh', 'search', 'repos', '--sort', 'stars', '--stars', STAR_FLOOR,
            '--limit', str(limit), '--json', 'fullName,stargazersCount,primaryLanguage'] + extra
    out, err = run(args, timeout=60)
    if out is None:
        print(f'  search failed ({extra}): {err}', flush=True)
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []


def build_sample():
    """Stratified top-starred sample: all-language + per-language + per-topic slices, deduped."""
    seen = {}   # fullName -> {stars, slice, language}

    def add(rows, slice_tag):
        for r in rows:
            fn = r.get('fullName')
            if not fn:
                continue
            lang = (r.get('primaryLanguage') or {}).get('name') if isinstance(r.get('primaryLanguage'), dict) else None
            if fn not in seen:
                seen[fn] = {'repo': fn, 'stars': r.get('stargazersCount'), 'slice': slice_tag, 'language': lang}

    print('all-language top-starred ...', flush=True)
    add(search([], ALL_LIMIT), 'all')
    time.sleep(3)
    for lang in LANGS:
        print(f'language:{lang} ...', flush=True)
        add(search(['--language', lang], LANG_LIMIT), f'lang:{lang}')
        time.sleep(3)
    for topic in TOPICS:
        print(f'topic:{topic} ...', flush=True)
        add(search(['--topic', topic], TOPIC_LIMIT), f'topic:{topic}')
        time.sleep(3)

    sample = list(seen.values())
    os.makedirs(ROOT, exist_ok=True)
    json.dump(sample, open(SAMPLE, 'w'), indent=2)
    print(f'\nSAMPLE: {len(sample)} distinct repos -> {SAMPLE}')
    print('by slice:', dict(Counter(s['slice'] for s in sample)))


def detect(repo):
    tree = gh_json(f'repos/{repo}/git/trees/HEAD?recursive=1', timeout=70)
    if not (isinstance(tree, dict) and 'tree' in tree):
        return None
    paths = [t.get('path', '') for t in tree['tree']]
    blob = '\n'.join(paths)
    rec = {'repo': repo, 'n_paths': len(paths), 'truncated': bool(tree.get('truncated'))}
    for k in KEYS:
        rec[k] = bool(FOUND[k].search(blob))
    return rec


def harvest():
    sample = json.load(open(SAMPLE))
    out = []
    failed = []
    for i, s in enumerate(sample, 1):
        repo = s['repo']
        rec = detect(repo)
        if rec is None:
            failed.append(repo)
        else:
            rec['stars'] = s.get('stars')
            rec['slice'] = s.get('slice')
            rec['language'] = s.get('language')
            out.append(rec)
        if i % 20 == 0:
            json.dump({'records': out, 'failed': failed}, open(REC, 'w'), indent=2)
            print(f'[{i}/{len(sample)}] kept={len(out)} failed={len(failed)} last={repo}', flush=True)
        time.sleep(0.15)
    json.dump({'records': out, 'failed': failed}, open(REC, 'w'), indent=2)
    print(f'\nDONE: harvested {len(out)} repos ({len(failed)} failed/inaccessible) -> {REC}')
    print('truncated trees:', sum(1 for r in out if r['truncated']))


def stats():
    data = json.load(open(REC))
    rows = data['records']
    n = len(rows)

    def pct(rs, k):
        return round(100 * sum(1 for r in rs if r.get(k)) / len(rs)) if rs else 0

    overall = {k: {'count': sum(1 for r in rows if r.get(k)), 'pct': pct(rows, k)} for k in KEYS}

    # by-language breakdown (primaryLanguage from search)
    langs = sorted({(r.get('language') or 'unknown') for r in rows})
    by_lang = {}
    for lg in langs:
        sub = [r for r in rows if (r.get('language') or 'unknown') == lg]
        if len(sub) >= 5:  # only report languages with >=5 repos
            by_lang[lg] = {'n': len(sub), **{k: pct(sub, k) for k in KEYS}}

    stats_out = {
        'census': 'planning-output',
        'mode': 'A (per-repo sampled census — gh search repos + recursive tree per repo)',
        'date': '2026-06-27',
        'account': 'coolbress',
        'star_floor': STAR_FLOOR,
        'n_repos': n,
        'n_failed': len(data.get('failed', [])),
        'n_truncated_trees': sum(1 for r in rows if r.get('truncated')),
        'caveats': ('star-count != quality; planning artifacts often in wikis/issues/external trackers '
                    '(under-counts those); default-branch HEAD tree only; truncated trees best-effort; '
                    'modest sample size; percentages directional.'),
        'feeds_aspects': ['01-requirements-planning'],
        'artifact_prevalence': overall,
        'by_language': by_lang,
        'slice_distribution': dict(Counter(r.get('slice') for r in rows)),
    }
    json.dump(stats_out, open(f'{ROOT}/stats.json', 'w'), indent=2)

    # CSV tally
    with open(f'{ROOT}/tally.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['artifact', 'count', 'pct'])
        for k in KEYS:
            w.writerow([k, overall[k]['count'], overall[k]['pct']])

    print(f'N = {n} repos\n')
    print(f"{'ARTIFACT':<16} {'count':>6} {'pct':>5}")
    for k in KEYS:
        print(f"{k:<16} {overall[k]['count']:>6} {overall[k]['pct']:>4}%")
    print('\n-> wrote stats.json + tally.csv')


def codesearch():
    """Mode B supplement: raw global filename/path total_counts. Rate-limited (~10/min code_search)."""
    queries = {
        'filename:PRD.md': 'filename:PRD.md',
        'filename:requirements.md': 'filename:requirements.md',
        'filename:product-requirements.md': 'filename:product-requirements.md',
        'filename:ROADMAP.md': 'filename:ROADMAP.md',
        'filename:CHANGELOG.md': 'filename:CHANGELOG.md',
        'filename:AGENTS.md': 'filename:AGENTS.md',
        'filename:CLAUDE.md': 'filename:CLAUDE.md',
        'path:docs/adr': 'path:docs/adr',
        'path:docs/decisions': 'path:docs/decisions',
        'path:docs/specs': 'path:docs/specs',
        'path:docs/rfcs': 'path:docs/rfcs',
        'path:.specify/memory': 'path:.specify/memory',
        'path:.kiro/specs': 'path:.kiro/specs',
        'path:openspec/changes': 'path:openspec/changes',
    }
    out = {}
    for label, q in queries.items():
        res = gh_json('search/code?q=' + q.replace(' ', '+').replace(':', '%3A').replace('/', '%2F'), timeout=40)
        # simpler: use gh api -X GET with -f q
        if res is None:
            o, err = run(['gh', 'api', '-X', 'GET', 'search/code', '-f', f'q={q}', '--jq', '.total_count'], timeout=40)
            out[label] = int(o.strip()) if (o and o.strip().isdigit()) else None
        else:
            out[label] = res.get('total_count')
        print(f'{label:<36} {out[label]}', flush=True)
        time.sleep(8)
    blob = {
        'mode': 'B (count census supplement — gh search/code total_count; counts FILES not repos)',
        'date': '2026-06-27',
        'caveats': 'auth-gated, default-branch only, total_count approximate/capped, indexes a subset; directional.',
        'counts': out,
    }
    json.dump(blob, open(f'{ROOT}/codesearch.json', 'w'), indent=2)
    print('\n-> wrote codesearch.json')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'sample': build_sample, 'harvest': harvest, 'stats': stats, 'codesearch': codesearch}[cmd]()
