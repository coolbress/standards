#!/usr/bin/env python3
"""Issue/PR convention census — N=2000 widening (GraphQL-batched).

Widens the original 500-repo census (census.py) to the global top-2000 top-starred SOFTWARE repos, to
strengthen the section/field-label frequency statistics the issue/PR template standard is grounded in.

Two differences from census.py, both for scale:
  1. Population — a true GLOBAL top-2000-by-stars set: per-language star-sorted `gh search repos` (the same
     software-biased, language-tagged methodology as census-expanded) unioned, deduped, globally star-sorted.
  2. Harvest — ONE GraphQL query per BATCH of repos (issue-template tree + blob text, PR template, recent PR +
     issue titles) instead of ~8 REST calls/repo, with a rateLimit guard + incremental checkpoint. The REST
     path would be ~15k calls / several hours at 2000 AND has no rate-limit handling (→ silent empty records).

Run from repo root:
  python docs/research/census-data/census-issue-pr/census2k.py pop      # build pop-2k.json
  python docs/research/census-data/census-issue-pr/census2k.py harvest   # → records-2k.json + stats-2k.json
  python docs/research/census-data/census-issue-pr/census2k.py stats     # recompute stats from records-2k.json
Out: census-issue-pr/{pop-2k.json, records-2k.json, stats-2k.json}
"""
import json, math, re, subprocess, sys, time
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

ROOT = 'docs/research/census-data'
DIR = f'{ROOT}/census-issue-pr'
POP = f'{DIR}/pop-2k.json'
REC = f'{DIR}/records-2k.json'
OUT = f'{DIR}/stats-2k.json'
N = 2000
BATCH = 8
LANGS = ['python', 'javascript', 'typescript', 'go', 'rust', 'java', 'c++', 'ruby', 'c#', 'php', 'kotlin',
         'swift', 'c', 'dart', 'elixir', 'scala', 'shell']
CC = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?:\s.+')
PREFIX = re.compile(r'^\[[^\]]+\]|^[A-Za-z0-9_-]+:')  # [area] or word: lead
LABEL = re.compile(r'^\s*label:\s*(.+?)\s*$', re.M)
HEADER = re.compile(r'^#{1,4}\s+(.+)$', re.M)


def ratio(hits, total):
    return float(Decimal(hits / total).quantize(Decimal('0.01'), ROUND_HALF_UP)) if total else None


# ---- population: global-by-stars CANDIDATE pool (software-filtered later at harvest) --------------
# NOTE per-language star search is polluted with non-software (awesome-lists / books / roadmaps); the
# manifest filter (at harvest) keeps only real software, mirroring census-expanded's methodology. So the
# pool is a CANDIDATE set (all unique, star-ranked); harvest walks it in star order and keeps the first
# N that are software — yielding the true global top-N-by-stars *software* set.
def _search_budget():
    try:
        p = subprocess.run(['gh', 'api', 'rate_limit', '--jq', '.resources.search.remaining'],
                           capture_output=True, text=True, timeout=20)
        return int(p.stdout.strip() or 0)
    except Exception:
        return 0


def build_pop():
    cand = {}  # fullName -> stars (keep max)
    for lang in LANGS:
        rows = []
        for attempt in (1, 2):
            if _search_budget() < 6:
                print('search budget low — waiting 60s for reset', file=sys.stderr)
                time.sleep(60)
            try:
                p = subprocess.run(['gh', 'search', 'repos', '--language', lang, '--sort', 'stars',
                                    '--limit', '400', '--json', 'fullName,stargazersCount'],
                                   capture_output=True, text=True, timeout=90)
                rows = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else []
            except Exception:
                rows = []
            if rows:
                break
            time.sleep(10)
        for r in rows:
            fn, st = r.get('fullName'), r.get('stargazersCount') or 0
            if fn and st > cand.get(fn, -1):
                cand[fn] = st
        print(f'search {lang}: +{len(rows)} rows, pool now {len(cand)}', file=sys.stderr)
        time.sleep(5)
    ranked = sorted(cand.items(), key=lambda kv: (-kv[1], kv[0]))
    pop = [{'repo': fn, 'stars': st} for fn, st in ranked]
    json.dump(pop, open(POP, 'w'), indent=2)
    print(f'built candidate pool: {len(pop)} repos (stars {pop[0]["stars"]}..{pop[-1]["stars"]}) -> {POP}',
          file=sys.stderr)
    return pop


# ---- GraphQL batch harvest -----------------------------------------------------------------------
# root-level package manifests (mirrors census-expanded's MANIFEST set) → "is this real software?"
MANIFESTS = ['package.json', 'pyproject.toml', 'setup.py', 'Cargo.toml', 'go.mod', 'pom.xml',
             'build.gradle', 'build.gradle.kts', 'Gemfile', 'composer.json', 'Package.swift',
             'mix.exs', 'build.sbt', 'pubspec.yaml']


def _repo_query(alias, owner, name):
    o, n = json.dumps(owner), json.dumps(name)
    man = '\n    '.join(
        f'm{i}: object(expression: "HEAD:{m}") {{ ... on Blob {{ byteSize }} }}'
        for i, m in enumerate(MANIFESTS))
    return f'''{alias}: repository(owner: {o}, name: {n}) {{
    {man}
    itdir: object(expression: "HEAD:.github/ISSUE_TEMPLATE") {{ ... on Tree {{ entries {{ name object {{ ... on Blob {{ text }} }} }} }} }}
    pr1: object(expression: "HEAD:.github/PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }}
    pr2: object(expression: "HEAD:PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }}
    pr3: object(expression: "HEAD:docs/PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }}
    pulls: pullRequests(first: 30, orderBy: {{field: CREATED_AT, direction: DESC}}) {{ nodes {{ title }} }}
    issues: issues(first: 30, orderBy: {{field: CREATED_AT, direction: DESC}}) {{ nodes {{ title }} }}
  }}'''


def _is_software(node):
    return any(node.get(f'm{i}') for i in range(len(MANIFESTS)))


def _gql(batch):
    parts = []
    for i, repo in enumerate(batch):
        if '/' not in repo:
            continue
        owner, name = repo.split('/', 1)
        parts.append(_repo_query(f'r{i}', owner, name))
    query = '{\n' + '\n'.join(parts) + '\n  rateLimit { remaining resetAt }\n}'
    try:
        p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'],
                           capture_output=True, text=True, timeout=120)
        return json.loads(p.stdout) if p.stdout else None
    except Exception:
        return None


def _record(repo, node, stars):
    forms = md = 0
    config = False
    form_labels, md_headers = [], []
    itdir = node.get('itdir') or {}
    for e in (itdir.get('entries') or []):
        nm = e.get('name', '')
        text = ((e.get('object') or {}) or {}).get('text') or ''
        if nm in ('config.yml', 'config.yaml'):
            config = True
        elif re.search(r'\.ya?ml$', nm):
            forms += 1
            form_labels += [m.group(1).strip(' "\'').lower() for m in LABEL.finditer(text)]
        elif nm.endswith('.md'):
            md += 1
            md_headers += [h.strip().lower() for h in HEADER.findall(text)]
    pr = node.get('pr1') or node.get('pr2') or node.get('pr3')
    pr_raw = pr.get('text') if pr else None
    pr_headers = [h.strip().lower() for h in HEADER.findall(pr_raw)] if pr_raw else []
    pr_titles = [x['title'] for x in ((node.get('pulls') or {}).get('nodes') or []) if x.get('title')]
    iss_titles = [x['title'] for x in ((node.get('issues') or {}).get('nodes') or []) if x.get('title')]
    return {
        'repo': repo, 'stars': stars,
        'issue_forms': forms, 'issue_md': md, 'issue_config': config,
        'has_issue_tmpl': forms + md > 0, 'issue_form_labels': form_labels, 'issue_md_headers': md_headers,
        'has_pr_tmpl': bool(pr_raw), 'pr_tmpl_n_headers': len(pr_headers), 'pr_tmpl_headers': pr_headers,
        'pr_tmpl_has_checklist': bool(pr_raw and '- [ ]' in pr_raw),
        'pr_n': len(pr_titles), 'pr_cc': ratio(sum(bool(CC.match(t)) for t in pr_titles), len(pr_titles)),
        'iss_n': len(iss_titles), 'iss_cc': ratio(sum(bool(CC.match(t)) for t in iss_titles), len(iss_titles)),
        'iss_prefix': ratio(sum(bool(PREFIX.match(t)) for t in iss_titles), len(iss_titles)),
        'iss_avg_len': round(sum(len(t) for t in iss_titles) / len(iss_titles)) if iss_titles else None,
    }


def harvest():
    pop = json.load(open(POP)) if _exists(POP) else build_pop()
    stars = {r['repo']: r['stars'] for r in pop}
    repos = [r['repo'] for r in pop]  # already star-ranked
    records, scanned, nonsoft = [], 0, 0
    for start in range(0, len(repos), BATCH):
        if len(records) >= N:
            break
        batch = repos[start:start + BATCH]
        data = _gql(batch)
        if data and data.get('data'):
            d = data['data']
            for i, repo in enumerate(batch):
                node = d.get(f'r{i}')
                scanned += 1
                if not node:
                    continue
                if not _is_software(node):
                    nonsoft += 1
                    continue
                records.append(_record(repo, node, stars.get(repo)))
            rl = d.get('rateLimit') or {}
            if rl.get('remaining', 9999) < 200:
                _wait_for_reset(rl.get('resetAt'))
        if (start // BATCH) % 10 == 0:
            json.dump(records, open(REC, 'w'))  # checkpoint
            print(f'...scanned {scanned}, software={len(records)}/{N}, dropped-nonsoftware={nonsoft}',
                  file=sys.stderr)
        time.sleep(0.3)
    json.dump(records[:N], open(REC, 'w'))
    print(f'harvested {len(records[:N])} software repos (scanned {scanned}, dropped {nonsoft} non-software) -> {REC}',
          file=sys.stderr)
    stats()


def _exists(path):
    try:
        open(path).close(); return True
    except OSError:
        return False


# ---- presence repair (census-expanded-comparable, recursive-tree + case-insensitive regex) --------
# The GraphQL harvest checks fixed exact-case paths → undercounts PR templates (lowercase / dir form /
# docs-location). census-expanded detects presence by regex over the FULL recursive tree; replicating it
# here makes the N=2000 presence-% directly comparable to aspect-22's (n=938) numbers.
ISSUE_TMPL_RE = re.compile(r'(^|/)\.github/ISSUE_TEMPLATE', re.I | re.M)
PR_TMPL_RE = re.compile(r'(^|/)(\.github/)?(PULL_REQUEST_TEMPLATE|pull_request_template)', re.I | re.M)
IT_FILE_RE = re.compile(r'(^|/)\.github/ISSUE_TEMPLATE/([^/]+)$', re.I)
CONFIG_RE = re.compile(r'/config\.ya?ml$', re.I)


def _tree_paths(repo):
    try:
        p = subprocess.run(['gh', 'api', f'repos/{repo}/git/trees/HEAD?recursive=1'],
                           capture_output=True, text=True, timeout=60)
        t = json.loads(p.stdout) if p.returncode == 0 and p.stdout else None
    except Exception:
        return None
    if not (isinstance(t, dict) and 'tree' in t):
        return None
    return [x.get('path', '') for x in t['tree']]


def repair():
    """Recompute has_issue_tmpl / has_pr_tmpl / forms·md·config from the recursive tree (census-expanded
    method), so the presence-% is comparable to aspect-22. Field-label / header / title data is untouched."""
    records = json.load(open(REC))
    fixed = 0
    for i, r in enumerate(records, 1):
        paths = _tree_paths(r['repo'])
        if paths is None:
            continue
        blob = '\n'.join(paths)
        had = (r['has_issue_tmpl'], r['has_pr_tmpl'])
        r['has_issue_tmpl'] = bool(ISSUE_TMPL_RE.search(blob))
        r['has_pr_tmpl'] = bool(PR_TMPL_RE.search(blob))
        it_files = [m.group(2) for m in (IT_FILE_RE.search(p) for p in paths) if m]
        r['issue_forms'] = sum(1 for f in it_files if re.search(r'\.ya?ml$', f, re.I) and not re.match(r'config\.ya?ml$', f, re.I))
        r['issue_md'] = sum(1 for f in it_files if f.lower().endswith('.md'))
        r['issue_config'] = any(CONFIG_RE.search(p) for p in paths if IT_FILE_RE.search(p))
        if had != (r['has_issue_tmpl'], r['has_pr_tmpl']):
            fixed += 1
        if i % 200 == 0:
            json.dump(records, open(REC, 'w'))
            print(f'...repaired {i}/{len(records)} (presence-flag changes so far: {fixed})', file=sys.stderr)
    json.dump(records, open(REC, 'w'))
    print(f'repaired {len(records)} records ({fixed} presence-flag corrections) -> {REC}', file=sys.stderr)
    stats()


def _wait_for_reset(reset_at):
    """GraphQL points reset hourly; when the budget is spent, wait until resetAt (+buffer)."""
    from datetime import datetime, timezone
    secs = 65
    if reset_at:
        try:
            r = datetime.fromisoformat(reset_at.replace('Z', '+00:00'))
            secs = max(65, int((r - datetime.now(timezone.utc)).total_seconds()) + 5)
        except Exception:
            pass
    print(f'GraphQL budget low — waiting {secs}s for reset ({reset_at})', file=sys.stderr)
    time.sleep(secs)


def stats():
    records = json.load(open(REC))
    n = len(records)

    def pct(count):
        return math.floor(100 * count / n + 0.5)

    def mean(vals):
        v = [x for x in vals if x is not None]
        return float(Decimal(sum(v) / len(v)).quantize(Decimal('0.01'), ROUND_HALF_UP)) if v else None

    def top(key, k):
        c = Counter(h for r in records for h in (r.get(key) or []))
        return [[name, cnt] for name, cnt in c.most_common(k)]

    pr_data = [r for r in records if r['pr_cc'] is not None]
    star_vals = [r['stars'] for r in records if r.get('stars')]
    out = {
        'n': n,
        'source': 'global top-2000 by stars, per-language star-sorted software repos (census2k.py)',
        'presence_method': 'has_issue_tmpl/has_pr_tmpl via recursive-tree case-insensitive regex (repair mode; census-expanded-comparable). template field-labels/headers/titles via GraphQL.',
        'star_range': [min(star_vals), max(star_vals)] if star_vals else None,
        'issue_templates_pct': pct(sum(1 for r in records if r['has_issue_tmpl'])),
        'issue_forms_pct': pct(sum(1 for r in records if r['issue_forms'] > 0)),
        'issue_legacy_md_pct': pct(sum(1 for r in records if r['issue_md'] > 0)),
        'issue_config_pct': pct(sum(1 for r in records if r['issue_config'])),
        'pr_template_pct': pct(sum(1 for r in records if r['has_pr_tmpl'])),
        'pr_template_with_checklist_pct': pct(sum(1 for r in records if r['has_pr_tmpl'] and r['pr_tmpl_has_checklist'])),
        'pr_cc_adoption_ge70_pct': round(100 * sum(1 for r in pr_data if r['pr_cc'] >= 0.7) / len(pr_data)) if pr_data else None,
        'pr_cc_mostly_ge30_pct': round(100 * sum(1 for r in pr_data if r['pr_cc'] >= 0.3) / len(pr_data)) if pr_data else None,
        'pr_cc_mean_ratio': mean([r['pr_cc'] for r in records]),
        'issue_cc_mean_ratio': mean([r['iss_cc'] for r in records]),
        'issue_prefix_mean_ratio': mean([r['iss_prefix'] for r in records]),
        'issue_title_avg_len': mean([r['iss_avg_len'] for r in records]),
        'pr_template_top_headers': top('pr_tmpl_headers', 25),
        'issue_form_top_field_labels': top('issue_form_labels', 25),
        'issue_md_top_headers': top('issue_md_headers', 20),
        'repos_with_pr_data': len(pr_data),
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(f'wrote {OUT} (n={n})', file=sys.stderr)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'pop': build_pop, 'harvest': harvest, 'repair': repair, 'stats': stats}.get(cmd, stats)()
