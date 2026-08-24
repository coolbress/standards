#!/usr/bin/env python3
"""Governance/quality FLOOR census — the 3-tier grounding census (N≈7-8k, GraphQL-batched).

Extends census-issue-pr/census2k.py from (issue/PR templates only) to the FULL tree-visible
governance/quality item set, so every candidate scaffold item gets a MEASURED presence % and an
ARCHETYPE-conditioned rate — the evidence that assigns each item to one of three tiers:
  ① industry-standard (near-universal)      → auto-ship
  ② senior-default (weak-in-wild but craft) → default-on with an expert escape hatch
  ③ project-context (archetype/audience-owned) → propose + user-confirm (else silently omit)

Population: a deeper global-top-by-stars SOFTWARE set (per-language star-search `--limit 500`,
software-manifest-filtered at harvest), widened past the 2000-repo census-issue-pr set.

Harvest performance note: an early design probed ~50 individual object(expression:"HEAD:<path>")
files per repo + a 30-PR fetch — that made each 6-repo query take 20-56s (and the PR fetch overflowed
the GraphQL complexity limit, erroring outright). The fix (this version): fetch ~5 DIRECTORY trees per
repo (root · .github · docs · ISSUE_TEMPLATE · workflows) and detect every governance file from its
entry NAMES locally — cheaper server-side AND more robust (all locations + case variants). CC-PR-title
is NOT re-measured here (it already lives in census-issue-pr/stats-2k.json).

Run from repo root:
  python docs/research/census-data/census-governance-floor/census.py smoke     # validate query+parsers + time it
  python docs/research/census-data/census-governance-floor/census.py pop        # build pop.json (deeper search)
  python docs/research/census-data/census-governance-floor/census.py harvest     # -> records.json + stats.json
  python docs/research/census-data/census-governance-floor/census.py stats        # recompute stats from records.json
"""
import json, math, re, subprocess, sys, time
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

DIR = 'docs/research/census-data/census-governance-floor'
POP = f'{DIR}/pop.json'
REC = f'{DIR}/records.json'
OUT = f'{DIR}/stats.json'
N = 8000
BATCH = 10

LANGS = ['python', 'javascript', 'typescript', 'go', 'rust', 'java', 'c++', 'ruby', 'c#', 'php',
         'kotlin', 'swift', 'c', 'dart', 'elixir', 'scala', 'shell', 'lua', 'haskell', 'clojure',
         'julia', 'zig', 'ocaml', 'objective-c', 'groovy', 'perl', 'nim', 'crystal']

# manifest filename -> ecosystem (root-tree entry names; first match in this order wins)
MANIFEST_ECO = [('package.json', 'node'), ('pyproject.toml', 'python'), ('setup.py', 'python'),
                ('cargo.toml', 'rust'), ('go.mod', 'go'), ('pom.xml', 'java'), ('build.gradle', 'java'),
                ('build.gradle.kts', 'java'), ('gemfile', 'ruby'), ('composer.json', 'php'),
                ('package.swift', 'swift'), ('mix.exs', 'elixir'), ('build.sbt', 'scala'),
                ('pubspec.yaml', 'dart')]
MANIFESTS = [m for m, _ in MANIFEST_ECO]
MONO_MARKERS = ['pnpm-workspace.yaml', 'lerna.json', 'nx.json', 'turbo.json', 'go.work']
LOCKFILES = ['pnpm-lock.yaml', 'package-lock.json', 'yarn.lock', 'cargo.lock', 'go.sum',
             'poetry.lock', 'gemfile.lock', 'composer.lock', 'uv.lock', 'bun.lockb']
CI_ROOT_MARKERS = ['.gitlab-ci.yml', '.travis.yml', 'azure-pipelines.yml', '.circleci', 'jenkinsfile',
                   '.drone.yml', 'bitbucket-pipelines.yml']

# governance/quality file detection — lowercased entry names (matched against a dir's entry set)
NAMESETS = {
    'license':       ['license', 'license.md', 'license.txt', 'license.rst', 'copying', 'licence',
                      'licence.md', 'license-mit', 'license-apache'],
    'contributing':  ['contributing', 'contributing.md', 'contributing.rst', 'contribute.md'],
    'security':      ['security', 'security.md', 'security.rst'],
    'codeowners':    ['codeowners'],
    'coc':           ['code_of_conduct', 'code_of_conduct.md', 'code-of-conduct.md', 'code_of_conduct.rst'],
    'changelog':     ['changelog', 'changelog.md', 'changes.md', 'changelog.rst', 'history.md', 'changes'],
    'support':       ['support', 'support.md'],
    'governance':    ['governance', 'governance.md'],
    'cla':           ['cla.md', 'cla'],
    'editorconfig':  ['.editorconfig'],
    'gitattributes': ['.gitattributes'],
    'env_example':   ['.env.example', '.env.sample', '.env.template', '.env.dist'],
    'precommit':     ['.pre-commit-config.yaml', '.pre-commit-config.yml'],
    'gitignore':     ['.gitignore'],
    'agents_md':     ['agents.md'],
    'claude_md':     ['claude.md'],
    'dependabot':    ['dependabot.yml', 'dependabot.yaml'],
    'funding':       ['funding.yml', 'funding.yaml'],
    'renovate':      ['renovate.json', '.renovaterc', '.renovaterc.json', 'renovate.json5'],
    'pr_template':   ['pull_request_template.md', 'pull_request_template'],
    'issue_legacy':  ['issue_template.md', 'issue_template'],
    'adr_dir':       ['adr', 'adrs', 'decisions'],
}


# ---- population: deeper global-by-stars candidate pool (software-filtered later at harvest) -------
def _search_budget():
    try:
        p = subprocess.run(['gh', 'api', 'rate_limit', '--jq', '.resources.search.remaining'],
                           capture_output=True, text=True, timeout=20)
        return int((p.stdout or '0').strip() or 0)
    except Exception:
        return 0


def build_pop():
    cand = {}  # fullName -> stars (keep max)
    for lang in LANGS:
        rows = []
        # The heavy popular-language searches are the most timeout/throttle-prone under this env's
        # gh flakiness → python/js/ts/java silently returned 0. Fix: reliable per-lang limit (500 =
        # 5 pages) + ≥12 budget headroom so a full call + retry never exhausts mid-paging + a loud
        # warning on true-empty.
        for attempt in range(5):
            while _search_budget() < 12:
                print('  search budget low — waiting 30s for refill', file=sys.stderr)
                time.sleep(30)
            try:
                p = subprocess.run(['gh', 'search', 'repos', '--language', lang, '--sort', 'stars',
                                    '--limit', '500', '--json', 'fullName,stargazersCount'],
                                   capture_output=True, text=True, timeout=300)
                rows = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else []
            except Exception:
                rows = []
            if rows:
                break
            print(f'  retry {lang} (attempt {attempt + 1} empty)', file=sys.stderr)
            time.sleep(8 + attempt * 7)
        if not rows:
            print(f'  !! WARNING: {lang} returned 0 rows after 5 attempts — SKEW RISK', file=sys.stderr)
        for r in rows:
            fn, st = r.get('fullName'), r.get('stargazersCount') or 0
            if fn and st > cand.get(fn, -1):
                cand[fn] = st
        print(f'search {lang}: +{len(rows)} rows, pool now {len(cand)}', file=sys.stderr)
        time.sleep(3)
    ranked = sorted(cand.items(), key=lambda kv: (-kv[1], kv[0]))
    pop = [{'repo': fn, 'stars': st} for fn, st in ranked]
    json.dump(pop, open(POP, 'w'), indent=2)
    print(f'built candidate pool: {len(pop)} repos (stars {pop[0]["stars"]}..{pop[-1]["stars"]}) -> {POP}',
          file=sys.stderr)
    return pop


# ---- GraphQL batch harvest: native fields + directory-tree entries (NOT per-file probes) ---------
def _frag(alias, owner, name):
    o, n = json.dumps(owner), json.dumps(name)
    return f'''{alias}: repository(owner: {o}, name: {n}) {{
    stargazerCount
    primaryLanguage {{ name }}
    licenseInfo {{ spdxId key }}
    codeOfConduct {{ key }}
    fundingLinks {{ platform }}
    hasDiscussionsEnabled
    mergeCommitAllowed
    squashMergeAllowed
    rebaseMergeAllowed
    repositoryTopics(first: 12) {{ nodes {{ topic {{ name }} }} }}
    root: object(expression: "HEAD:") {{ ... on Tree {{ entries {{ name type }} }} }}
    gh: object(expression: "HEAD:.github") {{ ... on Tree {{ entries {{ name type }} }} }}
    docs: object(expression: "HEAD:docs") {{ ... on Tree {{ entries {{ name type }} }} }}
    it: object(expression: "HEAD:.github/ISSUE_TEMPLATE") {{ ... on Tree {{ entries {{ name }} }} }}
    wf: object(expression: "HEAD:.github/workflows") {{ ... on Tree {{ entries {{ name }} }} }}
    pkg: object(expression: "HEAD:package.json") {{ ... on Blob {{ text }} }}
    pyproj: object(expression: "HEAD:pyproject.toml") {{ ... on Blob {{ text }} }}
  }}'''


def _gql(batch):
    parts = []
    for i, repo in enumerate(batch):
        if '/' not in repo:
            continue
        owner, name = repo.split('/', 1)
        parts.append(_frag(f'r{i}', owner, name))
    query = '{\n' + '\n'.join(parts) + '\n  rateLimit { remaining resetAt }\n}'
    # Retry transient failures (this env sees frequent gh TLS/dial timeouts) — a skipped batch would
    # silently DROP its repos. A response carrying `data` (even with partial `errors` for a deleted
    # repo in the batch) is a success.
    for attempt in range(5):
        try:
            p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'],
                               capture_output=True, text=True, timeout=120)
            if p.stdout:
                d = json.loads(p.stdout)
                if d and d.get('data'):
                    return d
        except Exception:
            pass
        time.sleep(1 + attempt * 2)
    return None


def _entries(node, key):
    """Return {name_lower: type} for a directory-tree object (missing dir -> {})."""
    o = node.get(key) or {}
    out = {}
    for e in (o.get('entries') or []):
        nm = str(e.get('name', '')).lower()
        if nm:
            out[nm] = e.get('type', 'blob')
    return out


def _names(node, key):
    o = node.get(key) or {}
    return [str(e.get('name', '')) for e in (o.get('entries') or [])]


def _is_software(root):
    return any(m in root for m in MANIFESTS)


def _hit(entset, key):
    return any(nm in entset for nm in NAMESETS[key])


# ecosystem tag: prefer GitHub's primaryLanguage (language-of-most-bytes) so a polyglot repo (e.g.
# django, a Python project carrying a root package.json for docs tooling) isn't mis-tagged 'node' by
# a first-manifest scan; fall back to the manifest only when the language is null/unmapped.
LANG_ECO = {'python': 'python', 'javascript': 'node', 'typescript': 'node', 'go': 'go', 'rust': 'rust',
            'java': 'java', 'kotlin': 'java', 'groovy': 'java', 'ruby': 'ruby', 'php': 'php',
            'swift': 'swift', 'objective-c': 'swift', 'c#': 'dotnet', 'f#': 'dotnet', 'c++': 'cpp',
            'c': 'cpp', 'elixir': 'elixir', 'scala': 'scala', 'dart': 'dart', 'lua': 'lua',
            'haskell': 'haskell', 'clojure': 'clojure', 'julia': 'julia', 'zig': 'zig', 'ocaml': 'ocaml',
            'perl': 'perl', 'nim': 'nim', 'crystal': 'crystal', 'shell': 'shell'}


def _eco(primary_lang, root):
    lang = (primary_lang or '').lower()
    if lang in LANG_ECO:
        return LANG_ECO[lang]
    for m, e in MANIFEST_ECO:
        if m in root:
            return e
    return 'other'


def _archetype(root, pkg_text, pyproj_text):
    mono = any(m in root for m in MONO_MARKERS)
    cli = lib = app = False
    if 'package.json' in root and pkg_text:
        try:
            pj = json.loads(pkg_text)
            if pj.get('bin'):
                cli = True
            if pj.get('workspaces'):
                mono = True
            priv = pj.get('private') is True
            has_entry = any(k in pj for k in ('main', 'module', 'exports', 'types'))
            deps = {**(pj.get('dependencies') or {}), **(pj.get('devDependencies') or {})}
            web = any(d in deps for d in ('react', 'next', 'vue', '@angular/core', 'svelte', 'express',
                                          'koa', 'fastify', '@nestjs/core', 'gatsby', 'nuxt', 'remix'))
            if not cli and has_entry and not priv:
                lib = True
            if priv or web:
                app = True
        except Exception:
            pass
    if ('pyproject.toml' in root or 'setup.py' in root) and pyproj_text and not (cli or lib):
        low = pyproj_text.lower()
        if 'console_scripts' in low or '[project.scripts]' in low or '[tool.poetry.scripts]' in low:
            cli = True
        if '[project]' in low or 'build-system' in low or '[tool.poetry]' in low:
            lib = True
    if not (cli or lib or app):
        app = True
    return mono, cli, lib, app


def _record(repo, node, stars_hint):
    root = _entries(node, 'root')
    gh = _entries(node, 'gh')
    docs = _entries(node, 'docs')
    rgd = {**root, **gh, **docs}  # community-health files may live in any of the three
    pkg = (node.get('pkg') or {}).get('text') or ''
    pyproj = (node.get('pyproj') or {}).get('text') or ''
    mono, cli, lib, app = _archetype(root, pkg, pyproj)
    eco = _eco((node.get('primaryLanguage') or {}).get('name'), root)
    it_names = _names(node, 'it')
    forms = sum(1 for f in it_names if re.search(r'\.ya?ml$', f, re.I) and f.lower() not in ('config.yml', 'config.yaml'))
    md = sum(1 for f in it_names if f.lower().endswith('.md'))
    config = any(f.lower() in ('config.yml', 'config.yaml') for f in it_names)
    wf_names = _names(node, 'wf')
    n_wf = sum(1 for f in wf_names if f.lower().endswith(('.yml', '.yaml')))
    lic = node.get('licenseInfo') or {}
    coc_key = (node.get('codeOfConduct') or {}).get('key')
    has_issue_tmpl = (forms + md > 0) or _hit(gh, 'issue_legacy') or _hit(root, 'issue_legacy') \
        or (gh.get('issue_template') == 'tree')
    adr = (docs.get('adr') == 'tree' or docs.get('adrs') == 'tree' or docs.get('decisions') == 'tree'
           or docs.get('architecture') == 'tree' or root.get('adr') == 'tree' or root.get('adrs') == 'tree')
    return {
        'repo': repo, 'stars': node.get('stargazerCount') or stars_hint,
        'eco': eco, 'mono': mono, 'cli': cli, 'lib': lib, 'app': app,
        'primary_lang': (node.get('primaryLanguage') or {}).get('name'),
        'topics': [t['topic']['name'] for t in ((node.get('repositoryTopics') or {}).get('nodes') or [])
                   if t.get('topic')],
        'has_ci': n_wf > 0 or any(m in root for m in CI_ROOT_MARKERS), 'n_workflows': n_wf,
        # licensing
        'license': bool(lic.get('spdxId')) or _hit(rgd, 'license'),
        'license_recognized': bool(lic.get('spdxId')) and lic.get('spdxId') != 'NOASSERTION',
        'license_spdx': lic.get('spdxId'),
        # governance file set (root|.github|docs)
        'contributing': _hit(rgd, 'contributing'),
        'security': _hit(rgd, 'security'),
        'codeowners': _hit(rgd, 'codeowners'),
        'coc': bool(coc_key) or _hit(rgd, 'coc'),
        'coc_covenant': coc_key in ('contributor_covenant', 'contributor_covenant_v2'),
        'changelog': _hit(root, 'changelog') or _hit(docs, 'changelog'),
        'support': _hit(rgd, 'support'),
        'governance': _hit(rgd, 'governance'),
        'cla': _hit(rgd, 'cla'),
        # dx / config files (root convention)
        'editorconfig': _hit(root, 'editorconfig'),
        'gitattributes': _hit(root, 'gitattributes'),
        'env_example': _hit(root, 'env_example'),
        'precommit': _hit(root, 'precommit'),
        'gitignore': _hit(root, 'gitignore'),
        'readme': any(nm.startswith('readme') for nm in root),
        'has_lockfile': any(m in root for m in LOCKFILES),
        # supply-chain automation
        'dependabot': _hit(gh, 'dependabot'),
        'renovate': _hit(root, 'renovate') or _hit(gh, 'renovate'),
        'dep_update_bot': _hit(gh, 'dependabot') or _hit(root, 'renovate') or _hit(gh, 'renovate'),
        # ai-harness planning
        'agents_md': _hit(root, 'agents_md'),
        'claude_md': _hit(root, 'claude_md'),
        'adr_dir': adr,
        # collaboration surfaces
        'issue_forms': forms, 'issue_md': md, 'issue_config': config, 'has_issue_tmpl': has_issue_tmpl,
        'pr_template': _hit(gh, 'pr_template') or _hit(root, 'pr_template') or _hit(docs, 'pr_template'),
        'funding': bool(node.get('fundingLinks')) or _hit(gh, 'funding'),
        'discussions': bool(node.get('hasDiscussionsEnabled')),
        # merge policy (native)
        'squash_allowed': node.get('squashMergeAllowed'),
        'merge_commit_allowed': node.get('mergeCommitAllowed'),
        'rebase_allowed': node.get('rebaseMergeAllowed'),
    }


def _wait_for_reset(reset_at):
    from datetime import datetime, timezone
    secs = 65
    if reset_at:
        try:
            r = datetime.fromisoformat(reset_at.replace('Z', '+00:00'))
            secs = max(65, int((r - datetime.now(timezone.utc)).total_seconds()) + 5)
        except Exception:
            pass
    print(f'  GraphQL budget low — waiting {secs}s for reset ({reset_at})', file=sys.stderr)
    time.sleep(secs)


def _exists(path):
    try:
        open(path).close(); return True
    except OSError:
        return False


def harvest():
    pop = json.load(open(POP)) if _exists(POP) else build_pop()
    stars = {r['repo']: r['stars'] for r in pop}
    repos = [r['repo'] for r in pop]  # already star-ranked
    records, scanned, nonsoft = [], 0, 0
    t0 = time.time()
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
                root = _entries(node, 'root')
                if not _is_software(root):
                    nonsoft += 1
                    continue
                records.append(_record(repo, node, stars.get(repo)))
            rl = d.get('rateLimit') or {}
            if rl.get('remaining', 9999) is not None and rl.get('remaining', 9999) < 200:
                _wait_for_reset(rl.get('resetAt'))
        else:
            time.sleep(1)
        if (start // BATCH) % 20 == 0:
            json.dump(records, open(REC, 'w'))  # checkpoint
            rate = len(records) / max(1, time.time() - t0)
            print(f'...scanned {scanned}, software={len(records)}/{N}, dropped={nonsoft}, '
                  f'{rate:.1f} rec/s', file=sys.stderr)
    json.dump(records[:N], open(REC, 'w'))
    print(f'harvested {len(records[:N])} software repos (scanned {scanned}, dropped {nonsoft} non-software) -> {REC}',
          file=sys.stderr)
    stats()


def smoke():
    """Validate the query + parsers on known repos (fast, foreground) + print per-batch timing."""
    test = ['facebook/react', 'cli/cli', 'pallets/flask', 'vercel/turborepo', 'rust-lang/cargo',
            'sindresorhus/ky', 'django/django', 'nestjs/nest', 'kubernetes/kubernetes', 'denoland/deno']
    t = time.time()
    data = _gql(test)
    dt = time.time() - t
    if not data or not data.get('data'):
        print('SMOKE FAIL — no data', file=sys.stderr); return
    print(f'batch of {len(test)} took {dt:.1f}s', file=sys.stderr)
    keys = ['eco', 'mono', 'cli', 'lib', 'app', 'has_ci', 'n_workflows', 'license', 'license_spdx',
            'contributing', 'security', 'codeowners', 'coc', 'coc_covenant', 'changelog', 'funding',
            'discussions', 'editorconfig', 'precommit', 'dependabot', 'renovate', 'agents_md',
            'claude_md', 'adr_dir', 'has_issue_tmpl', 'issue_forms', 'issue_config', 'pr_template',
            'squash_allowed', 'gitignore', 'readme', 'has_lockfile']
    for i, repo in enumerate(test):
        node = data['data'].get(f'r{i}')
        if not node:
            print(f'{repo}: (null)'); continue
        r = _record(repo, node, None)
        print(f'\n=== {repo} (stars {r["stars"]}) ===')
        print('  ' + '  '.join(f'{k}={r[k]}' for k in keys))
    print('\nSMOKE OK', file=sys.stderr)


# ---- stats ---------------------------------------------------------------------------------------
GATED_ITEMS = ['license', 'contributing', 'security', 'codeowners', 'coc', 'changelog', 'support',
               'governance', 'cla', 'editorconfig', 'gitattributes', 'env_example', 'precommit',
               'dependabot', 'renovate', 'dep_update_bot', 'agents_md', 'claude_md', 'adr_dir',
               'has_issue_tmpl', 'issue_forms', 'issue_config', 'pr_template', 'funding', 'discussions',
               'readme', 'gitignore', 'has_lockfile', 'has_ci']


def stats():
    records = json.load(open(REC))
    n = len(records)

    def pct(sub, tot=None):
        tot = n if tot is None else tot
        return math.floor(100 * sub / tot + 0.5) if tot else 0

    def count(key, pred=lambda r: True):
        return sum(1 for r in records if pred(r) and r.get(key))

    def sub_pct(key, subpred):
        s = [r for r in records if subpred(r)]
        return {'pct': pct(sum(1 for r in s if r.get(key)), len(s)), 'n': len(s)} if s else {'pct': None, 'n': 0}

    eco_dist = Counter(r['eco'] for r in records)
    arch = {'monorepo': count('mono'), 'cli': count('cli'), 'library': count('lib'),
            'app_service': count('app')}
    overall = {k: pct(count(k)) for k in GATED_ITEMS}
    by_archetype = {}
    for k in ['coc', 'codeowners', 'contributing', 'security', 'changelog', 'funding', 'discussions',
              'agents_md', 'claude_md', 'editorconfig', 'precommit', 'dep_update_bot', 'adr_dir',
              'pr_template', 'issue_forms', 'governance', 'support', 'cla', 'gitattributes', 'env_example']:
        by_archetype[k] = {
            'overall': overall.get(k),
            'monorepo': sub_pct(k, lambda r: r['mono']),
            'not_monorepo': sub_pct(k, lambda r: not r['mono']),
            'library': sub_pct(k, lambda r: r['lib']),
            'cli': sub_pct(k, lambda r: r['cli']),
            'app_service': sub_pct(k, lambda r: r['app']),
        }
    lic_present = count('license')
    lic_recog = count('license_recognized')
    top_spdx = Counter(r['license_spdx'] for r in records if r.get('license_spdx')).most_common(12)
    mp = [r for r in records if r.get('squash_allowed') is not None]
    coc_cov = count('coc_covenant')
    star_vals = [r['stars'] for r in records if r.get('stars')]
    by_eco = {}
    for e in [e for e, _ in eco_dist.most_common(8)]:
        sub = [r for r in records if r['eco'] == e]
        by_eco[e] = {'n': len(sub),
                     **{k: pct(sum(1 for r in sub if r.get(k)), len(sub)) for k in
                        ['license', 'contributing', 'security', 'coc', 'codeowners', 'changelog',
                         'editorconfig', 'dep_update_bot', 'has_ci', 'pr_template', 'agents_md', 'claude_md']}}
    out = {
        'n': n,
        'source': 'global top-by-stars software repos, deeper per-language search (census-governance-floor/census.py)',
        'method': 'GraphQL native fields + directory-tree entry detection (root/.github/docs/ISSUE_TEMPLATE/workflows); archetype from manifest text',
        'star_range': [min(star_vals), max(star_vals)] if star_vals else None,
        'ecosystem_distribution': dict(eco_dist.most_common()),
        'archetype_counts': arch,
        'archetype_pct': {k: pct(v) for k, v in arch.items()},
        'overall_presence_pct': overall,
        'licensing': {
            'present_pct': pct(lic_present), 'recognized_pct': pct(lic_recog),
            'recognized_given_present_pct': pct(lic_recog, lic_present) if lic_present else None,
            'top_spdx': top_spdx,
        },
        'coc_covenant_share_of_all_pct': pct(coc_cov),
        'merge_policy': {
            'n_resolved': len(mp),
            'squash_allowed_pct': pct(sum(1 for r in mp if r.get('squash_allowed')), len(mp)) if mp else None,
            'merge_commit_allowed_pct': pct(sum(1 for r in mp if r.get('merge_commit_allowed')), len(mp)) if mp else None,
            'rebase_allowed_pct': pct(sum(1 for r in mp if r.get('rebase_allowed')), len(mp)) if mp else None,
        },
        'by_ecosystem': by_eco,
        'by_archetype': by_archetype,
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(json.dumps({k: out[k] for k in ('n', 'star_range', 'ecosystem_distribution', 'archetype_pct',
                                          'overall_presence_pct', 'licensing', 'coc_covenant_share_of_all_pct',
                                          'merge_policy')}, indent=2, ensure_ascii=False))
    print(f'\nwrote {OUT} (n={n})', file=sys.stderr)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'pop': build_pop, 'harvest': harvest, 'stats': stats, 'smoke': smoke}.get(cmd, stats)()
