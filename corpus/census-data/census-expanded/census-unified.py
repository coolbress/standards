#!/usr/bin/env python3
"""Larger-N, fully-DETERMINISTIC re-census widening ALL existing statistics at once.

Widens: ② foundation file-flags + ④ release signals + Scorecard, over the UNION of the curated 429 set and
new language-stratified, MANIFEST-FILTERED (software-only) repos. Each record tagged source=base|new so stats
separate the DETECTION-METHOD delta (det-429 vs the original LLM-429) from the SAMPLE-SIZE delta (det-429 vs
det-union). Deterministic = reproducible; the original ② census used LLM agents, so this is also a method check.

Run from repo root:  python docs/research/census-expanded/census-unified.py harvest | stats
Out: census-expanded/records.json (+ stats to stdout).
"""
import json, os, re, subprocess, sys, time
from datetime import datetime

ROOT = 'docs/research/census-data'
REC = f'{ROOT}/census-expanded/records.json'
REF = datetime(2026, 6, 24)
H = 2.0
LANGS = ['python', 'javascript', 'typescript', 'go', 'rust', 'java', 'c++', 'ruby', 'c#', 'php', 'kotlin',
         'swift', 'c', 'dart', 'elixir', 'scala', 'shell']
CAP_NEW = 700
SC_KEYS = ['Code-Review', 'Pinned-Dependencies', 'Branch-Protection', 'Security-Policy', 'Maintained', 'Token-Permissions', 'SAST']

P = {  # foundation flags by file-path presence (deterministic)
 'manifest': r'(^|/)(pyproject\.toml|package\.json|Cargo\.toml|go\.mod|pom\.xml|build\.gradle(\.kts)?|Gemfile|composer\.json|setup\.py|Package\.swift|mix\.exs|build\.sbt|pubspec\.yaml)$',
 'license': r'(^|/)(LICENSE|LICENCE|COPYING)(\.\w+)?$',
 'readme': r'(^|/)README(\.\w+)?$',
 'gitignore': r'(^|/)\.gitignore$',
 'gitattributes': r'(^|/)\.gitattributes$',
 'editorconfig': r'(^|/)\.editorconfig$',
 'ci': r'(^|/)\.github/workflows/.+\.ya?ml$|(^|/)\.gitlab-ci\.yml$|(^|/)\.circleci/|(^|/)azure-pipelines\.yml$|(^|/)\.travis\.yml$',
 'dependabot': r'(^|/)\.github/dependabot\.ya?ml$|(^|/)renovate\.json$|(^|/)\.renovaterc',
 'issue_template': r'(^|/)\.github/ISSUE_TEMPLATE',
 'pr_template': r'(^|/)(\.github/)?(PULL_REQUEST_TEMPLATE|pull_request_template)',
 'dockerfile': r'(^|/)Dockerfile|(^|/)docker-compose\.ya?ml$|(^|/)compose\.ya?ml$',
 'env_example': r'(^|/)\.env\.(example|sample|template|dist)$',
 'devcontainer': r'(^|/)\.devcontainer',
 'changelog': r'(^|/)CHANGELOG',
 'contributing': r'(^|/)CONTRIBUTING',
 'security_md': r'(^|/)SECURITY(\.\w+)?$|(^|/)\.github/SECURITY',
 'code_of_conduct': r'(^|/)CODE_OF_CONDUCT',
 'codeowners': r'(^|/)(\.github/)?CODEOWNERS$',
 'lockfile': r'(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|Cargo\.lock|poetry\.lock|uv\.lock|Gemfile\.lock|composer\.lock|go\.sum|Pipfile\.lock)$',
 'runtime_pin': r'(^|/)(\.nvmrc|\.node-version|\.tool-versions|\.python-version|\.ruby-version|runtime\.txt|rust-toolchain(\.toml)?|\.sdkmanrc|\.go-version)$',
 'linter': r'(^|/)(\.eslintrc|biome\.jsonc?|ruff\.toml|\.ruff\.toml|\.flake8|\.pylintrc|\.golangci\.ya?ml|\.rubocop\.yml|\.stylelintrc)',
 'formatter': r'(^|/)(\.prettierrc|biome\.jsonc?|\.clang-format|rustfmt\.toml|\.rustfmt\.toml|\.black|\.yapfignore)',
 'typechecker': r'(^|/)(tsconfig\.json|jsconfig\.json|mypy\.ini|\.mypy\.ini|pyrightconfig\.json)$',
 'test_framework': r'(^|/)(tests?|spec)/|(^|/)(pytest\.ini|jest\.config\.\w+|vitest\.config\.\w+|\.mocharc|phpunit\.xml)|(_test\.go|\.test\.\w+|\.spec\.\w+)$',
 'precommit_hooks': r'(^|/)\.pre-commit-config\.ya?ml$|(^|/)lefthook\.ya?ml$|(^|/)\.husky/',
 'task_runner': r'(^|/)(Makefile|makefile|Taskfile\.ya?ml|[Jj]ustfile)$',
 'supply_chain': r'(^|/)\.github/workflows/.*(codeql|trivy|snyk|semgrep|scorecard)|(^|/)\.snyk$|(^|/)sbom',
}
FOUND = {k: re.compile(v, re.I | re.M) for k, v in P.items()}
MANIFEST = FOUND['manifest']
SEMVER = re.compile(r'^v?\d+\.\d+\.\d+')
CC = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]*\))?!?:\s', re.I)
FOUND_KEYS = list(P.keys())


def gh(path, timeout=55):
    for attempt in (1, 2):
        try:
            p = subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None
        if p.returncode == 0:
            try:
                return json.loads(p.stdout)
            except json.JSONDecodeError:
                return None
        if ('rate limit' in (p.stderr or '').lower() or 'secondary' in (p.stderr or '').lower()) and attempt == 1:
            time.sleep(25); continue
        return None


def scorecard(repo, timeout=25):
    try:
        p = subprocess.run(['curl', '-s', '--max-time', str(timeout),
                            f'https://api.securityscorecards.dev/projects/github.com/{repo}'],
                           capture_output=True, text=True, timeout=timeout + 5)
        d = json.loads(p.stdout)
        return d if isinstance(d, dict) and 'checks' in d else None
    except Exception:
        return None


def search(lang):
    try:
        p = subprocess.run(['gh', 'search', 'repos', '--language', lang, '--sort', 'stars', '--limit', '100',
                            '--json', 'fullName,createdAt'], capture_output=True, text=True, timeout=40)
        return json.loads(p.stdout) if p.returncode == 0 else []
    except Exception:
        return []


def one(repo, created, source):
    rec = {'repo': repo, 'created': created, 'source': source}
    tree = gh(f'repos/{repo}/git/trees/HEAD?recursive=1', timeout=60)
    if not (isinstance(tree, dict) and 'tree' in tree):
        return None
    blob = '\n'.join(t.get('path', '') for t in tree['tree'])
    if not MANIFEST.search(blob):
        return None  # software filter
    for k in FOUND_KEYS:
        rec[k] = bool(FOUND[k].search(blob))
    rel = gh(f'repos/{repo}/releases?per_page=100')
    rec['has_releases'] = bool(isinstance(rel, list) and rel)
    rec['has_release_notes'] = bool(isinstance(rel, list) and any((x.get('body') or '').strip() for x in rel))
    tags = gh(f'repos/{repo}/tags?per_page=100')
    names = [t.get('name', '') for t in tags] if isinstance(tags, list) else []
    rec['semver_any'] = any(SEMVER.match(n) for n in names)
    commits = gh(f'repos/{repo}/commits?per_page=30')
    if isinstance(commits, list) and commits:
        nm = [m for m in [(c.get('commit', {}).get('message', '') or '').split('\n')[0] for c in commits if c.get('commit')] if not m.startswith('Merge ')]
        rec['cc_adopted'] = (sum(1 for m in nm if CC.match(m)) / len(nm) >= 0.3) if nm else False
    else:
        rec['cc_adopted'] = False
    sc = scorecard(repo)
    if sc:
        ck = {c['name']: c.get('score') for c in sc.get('checks', [])}
        rec['sc_overall'] = sc.get('score')
        rec['sc'] = {k: ck.get(k) for k in SC_KEYS}
    else:
        rec['sc_overall'] = None
        rec['sc'] = {k: None for k in SC_KEYS}
    return rec


def harvest():
    base = [r['repo'] for r in json.load(open(f'{ROOT}/census-dev-environment/records.json')) if r.get('is_software')]
    dates = {d['fullName']: d.get('createdAt', '')[:10] for d in json.load(open('/tmp/dates.json'))}
    seen = set(base)
    cands = {}
    for lang in LANGS:
        for r in search(lang):
            fn = r.get('fullName')
            if fn and fn not in seen and fn not in cands:
                cands[fn] = r.get('createdAt', '')[:10] or None
        print(f'search {lang}: new candidates so far = {len(cands)}', flush=True)
        time.sleep(4)
    new = list(cands.items())[:CAP_NEW]
    work = [(r, dates.get(r), 'base') for r in base] + [(r, c, 'new') for r, c in new]
    print(f'\nharvesting union: {len(base)} base + {len(new)} new candidates = {len(work)} ...', flush=True)
    out, kept_new = [], 0
    os.makedirs(f'{ROOT}/census-expanded', exist_ok=True)
    for i, (repo, created, src) in enumerate(work, 1):
        rec = one(repo, created, src)
        if rec:
            out.append(rec)
            if src == 'new':
                kept_new += 1
        if i % 25 == 0:
            json.dump(out, open(REC, 'w'), indent=2)  # checkpoint
            print(f'[{i}/{len(work)}] kept={len(out)} (new-sw={kept_new})  last={repo}', flush=True)
        time.sleep(0.1)
    json.dump(out, open(REC, 'w'), indent=2)
    print(f'\nDONE: {len(out)} repos ({sum(1 for r in out if r["source"]=="base")} base + {kept_new} new software) -> {REC}')


def stats():
    rows = json.load(open(REC))
    llm = json.load(open(f'{ROOT}/census-dev-environment/stats.json'))['simple'].get('adoptionPctOverall', {})  # LLM-429 %

    def w(r):
        c = r.get('created')
        try:
            c = datetime.strptime(c[:10], '%Y-%m-%d') if c else None
        except ValueError:
            c = None
        return (0.5 ** (((REF - c).days / 365.25) / H)) if c else None
    for r in rows:
        r['_w'] = w(r)
    base = [r for r in rows if r['source'] == 'base']
    union = rows

    def pct(rs, f, weighted=False):
        d = [r for r in rs if r.get(f) is not None and (r.get('_w') is not None or not weighted)]
        if weighted:
            d = [r for r in d if r.get('_w') is not None]
            W = sum(r['_w'] for r in d)
            return round(100 * sum(r['_w'] for r in d if r.get(f)) / W) if W else 0
        return round(100 * sum(1 for r in d if r.get(f)) / len(d)) if d else 0

    print(f"N: base(det)={len(base)}  union(det)={len(union)}  (new software={len(union)-len(base)})")
    print("detΔ = det-429 − LLM-429 (detection-method);  smplΔ = det-UNION − det-429 (sample-size)\n")
    print(f"{'FOUNDATION FLAG':<18} {'LLM-429':>7} {'det-429':>7} {'det-UNION':>9} {'wgt':>5}  {'detΔ':>5} {'smplΔ':>6}")
    for f in FOUND_KEYS:
        lp = llm.get(f)
        d4, du, dw = pct(base, f), pct(union, f), pct(union, f, True)
        detd = f"{d4-lp:+d}" if isinstance(lp, (int, float)) else "-"
        print(f"{f:<18} {str(lp):>7} {d4:>7} {du:>9} {dw:>5}  {detd:>5} {du-d4:>+6}")
    print(f"\n{'RELEASE FLAG':<18} {'det-429':>7} {'det-UNION':>9} {'UNION-wgt':>9}")
    for f in ['has_releases', 'has_release_notes', 'semver_any', 'cc_adopted']:
        print(f"{f:<18} {pct(base,f):>7} {pct(union,f):>9} {pct(union,f,True):>9}")
    # scorecard
    print(f"\n{'SCORECARD(mean)':<18} {'base':>7} {'union':>9}")
    sc_mean = {}
    for k in SC_KEYS:
        bv = [r['sc'][k] for r in base if r.get('sc', {}).get(k) is not None and r['sc'][k] >= 0]
        uv = [r['sc'][k] for r in union if r.get('sc', {}).get(k) is not None and r['sc'][k] >= 0]
        sc_mean[k] = {'base': round(sum(bv) / len(bv), 1) if bv else None, 'union': round(sum(uv) / len(uv), 1) if uv else None}
        print(f"{k:<18} {sc_mean[k]['base'] if sc_mean[k]['base'] is not None else '-':>7} {sc_mean[k]['union'] if sc_mean[k]['union'] is not None else '-':>9}")
    out = {
        'n_base': len(base), 'n_union': len(union), 'n_new_software': len(union) - len(base),
        'half_life_yr': H, 'ref': REF.strftime('%Y-%m-%d'),
        'foundation_flags': {f: {'llm_429': llm.get(f), 'det_429': pct(base, f), 'det_union': pct(union, f), 'union_weighted': pct(union, f, True)} for f in FOUND_KEYS},
        'release_flags': {f: {'det_429': pct(base, f), 'det_union': pct(union, f), 'union_weighted': pct(union, f, True)} for f in ['has_releases', 'has_release_notes', 'semver_any', 'cc_adopted']},
        'scorecard_mean': sc_mean,
    }
    json.dump(out, open(f'{ROOT}/census-expanded/stats.json', 'w'), indent=2)
    print("\nsampleΔ small ⇒ the 429 numbers are robust to sample size. det-vs-LLM gap ⇒ detection-method nuance.")
    print("→ wrote census-expanded/stats.json")


if __name__ == '__main__':
    (harvest if (len(sys.argv) > 1 and sys.argv[1] == 'harvest') else stats)()
