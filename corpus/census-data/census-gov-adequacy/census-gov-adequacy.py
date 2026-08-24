#!/usr/bin/env python3
"""Governance-floor files: PRESENCE vs ADEQUACY — the Tier-1 method pilot.

A simple presence census answers "does the repo HAVE a CONTRIBUTING/SECURITY/CoC/CODEOWNERS/LICENSE?".
gingoa's own thesis (ADR-0008/0014) is **presence ≠ adequacy** — a senior engineer knows a stub file
that merely exists is not the same as a substantive, enforced one. This pilot measures BOTH: for each
governance file it detects presence AND parses the CONTENT to score whether it actually does its job,
then reports the **adequacy gap** (present but inadequate) — the quantity a presence-only census hides.

Population: the same top-2000-by-stars software repos as census-issue-pr (`records-2k.json`).
Harvest: GraphQL-batched content fetch at the standard governance-file locations (root · `.github/` ·
`docs/`; CODEOWNERS is exact-case per GitHub, others uppercase-conventional). Adequacy = content-parsed.

Run from repo root:
  python docs/research/census-data/census-gov-adequacy/census-gov-adequacy.py harvest
  python docs/research/census-data/census-gov-adequacy/census-gov-adequacy.py stats
Out: census-gov-adequacy/{records.json, stats.json}
"""
import json, math, re, subprocess, sys, time

ROOT = 'docs/research/census-data'
POP = f'{ROOT}/census-issue-pr/records-2k.json'   # reuse the 2000-repo software population
DIR = f'{ROOT}/census-gov-adequacy'
REC = f'{DIR}/records.json'
OUT = f'{DIR}/stats.json'
BATCH = 8

# candidate paths per governance file (first non-null wins); GraphQL blob lookups are case-sensitive, so
# we enumerate the conventional casings/locations. CODEOWNERS is exact-case (GitHub requires it).
PATHS = {
    'contributing': ['CONTRIBUTING.md', '.github/CONTRIBUTING.md', 'docs/CONTRIBUTING.md', 'CONTRIBUTING.rst', 'CONTRIBUTING'],
    'security': ['SECURITY.md', '.github/SECURITY.md', 'docs/SECURITY.md', 'SECURITY.rst', 'SECURITY'],
    'coc': ['CODE_OF_CONDUCT.md', '.github/CODE_OF_CONDUCT.md', 'docs/CODE_OF_CONDUCT.md', 'CODE_OF_CONDUCT'],
    'codeowners': ['CODEOWNERS', '.github/CODEOWNERS', 'docs/CODEOWNERS'],
    'license': ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENCE', 'LICENSE.rst', 'COPYING'],
}
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.\w{2,}')
CMD = re.compile(r'(npm |pnpm |yarn |make\b|cargo |go test|go build|pytest|python |pip install|bundle |gradle|mvn |composer |dotnet |`[^`]+`|```)', re.I)
LICENSE_SIG = re.compile(r'MIT License|Apache License|GNU (GENERAL|LESSER) PUBLIC|BSD \d|Mozilla Public License|ISC License|The Unlicense|Boost Software License|Creative Commons|SPDX-License-Identifier|Eclipse Public License|zlib License', re.I)


# ---- adequacy scorers (content-parsed — the substance of the pilot) ------------------------------
def score_contributing(t):
    tl = t.lower()
    has_devflow = bool(re.search(r'\b(test|build|install|lint|develop|setup)\b', tl)) and bool(CMD.search(t))
    has_prflow = bool(re.search(r'pull request|\bpr\b|\bfork\b|feature branch|submit .* change|open .* (pr|pull)', tl))
    substantive = len(t) >= 400
    return {'present': True, 'len': len(t), 'has_devflow': has_devflow, 'has_prflow': has_prflow,
            'adequate': has_devflow and has_prflow and substantive}


def score_security(t):
    tl = t.lower()
    has_channel = (bool(EMAIL.search(t)) or 'security advisor' in tl or 'privately' in tl
                   or bool(re.search(r'report.{0,40}(vulnerab|security)', tl))
                   or bool(re.search(r'do not (open|file|create|report|use).{0,40}(public )?(issue|github)', tl))
                   or any(k in tl for k in ('hackerone', 'bugcrowd', 'huntr', 'tidelift')))
    return {'present': True, 'len': len(t), 'has_channel': has_channel,
            'adequate': has_channel and len(t) >= 150}


def score_coc(t):
    tl = t.lower()
    covenant = 'contributor covenant' in tl
    has_contact = bool(EMAIL.search(t)) or 'enforcement' in tl or bool(re.search(r'report.{0,30}(behavior|conduct|abuse)', tl))
    return {'present': True, 'len': len(t), 'covenant': covenant, 'has_contact': has_contact,
            'adequate': covenant or (len(t) >= 600 and has_contact)}


def score_codeowners(t):
    rules = [ln for ln in t.splitlines()
             if ln.strip() and not ln.strip().startswith('#') and ('@' in ln or EMAIL.search(ln))]
    return {'present': True, 'len': len(t), 'rules': len(rules), 'adequate': len(rules) >= 1}


def score_license(t):
    return {'present': True, 'len': len(t), 'recognized': bool(LICENSE_SIG.search(t)),
            'adequate': bool(LICENSE_SIG.search(t)) and len(t) >= 150}


SCORERS = {'contributing': score_contributing, 'security': score_security, 'coc': score_coc,
           'codeowners': score_codeowners, 'license': score_license}


# ---- GraphQL batch content fetch -----------------------------------------------------------------
def _repo_query(alias, owner, name):
    o, n = json.dumps(owner), json.dumps(name)
    fields = []
    for key, paths in PATHS.items():
        for j, p in enumerate(paths):
            fields.append(f'{key}_{j}: object(expression: "HEAD:{p}") {{ ... on Blob {{ text }} }}')
    body = '\n    '.join(fields)
    return f'{alias}: repository(owner: {o}, name: {n}) {{\n    {body}\n  }}'


def _gql(batch):
    parts = [_repo_query(f'r{i}', *repo.split('/', 1)) for i, repo in enumerate(batch) if '/' in repo]
    query = '{\n' + '\n'.join(parts) + '\n  rateLimit { remaining resetAt }\n}'
    try:
        p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'],
                           capture_output=True, text=True, timeout=120)
        return json.loads(p.stdout) if p.stdout else None
    except Exception:
        return None


def _first_text(node, key):
    for j in range(len(PATHS[key])):
        o = node.get(f'{key}_{j}')
        if o and o.get('text'):
            return o['text']
    return None


def harvest():
    repos = [r['repo'] for r in json.load(open(POP))]
    records = []
    for start in range(0, len(repos), BATCH):
        batch = repos[start:start + BATCH]
        data = _gql(batch)
        if data and data.get('data'):
            d = data['data']
            for i, repo in enumerate(batch):
                node = d.get(f'r{i}')
                if not node:
                    continue
                rec = {'repo': repo}
                for key, scorer in SCORERS.items():
                    text = _first_text(node, key)
                    rec[key] = scorer(text) if text else {'present': False, 'adequate': False}
                records.append(rec)
            rl = d.get('rateLimit') or {}
            if rl.get('remaining', 9999) < 200:
                time.sleep(65)
        if (start // BATCH) % 15 == 0:
            json.dump(records, open(REC, 'w'))
            print(f'...{start + len(batch)}/{len(repos)} harvested={len(records)}', file=sys.stderr)
        time.sleep(0.3)
    json.dump(records, open(REC, 'w'))
    print(f'harvested {len(records)} -> {REC}', file=sys.stderr)
    stats()


def stats():
    records = json.load(open(REC))
    n = len(records)

    def pct(c):
        return math.floor(100 * c / n + 0.5)

    out = {'n': n, 'source': 'top-2000-by-stars software repos (reused from census-issue-pr); PRESENCE vs ADEQUACY (content-parsed)'}
    files = {}
    for key in SCORERS:
        present = sum(1 for r in records if r[key].get('present'))
        adequate = sum(1 for r in records if r[key].get('adequate'))
        files[key] = {
            'present_pct': pct(present),
            'adequate_pct': pct(adequate),
            'adequate_given_present_pct': round(100 * adequate / present) if present else None,
            'adequacy_gap_pp': pct(present) - pct(adequate),   # present-but-inadequate, percentage-points
            'present_n': present, 'adequate_n': adequate,
        }
    out['files'] = files
    # per-file signal breakdowns (why things fail adequacy)
    out['signals'] = {
        'contributing_has_devflow_pct': pct(sum(1 for r in records if r['contributing'].get('has_devflow'))),
        'contributing_has_prflow_pct': pct(sum(1 for r in records if r['contributing'].get('has_prflow'))),
        'security_has_channel_pct': pct(sum(1 for r in records if r['security'].get('has_channel'))),
        'coc_covenant_pct': pct(sum(1 for r in records if r['coc'].get('covenant'))),
        'codeowners_median_rules': _median([r['codeowners'].get('rules', 0) for r in records if r['codeowners'].get('present')]),
        'license_recognized_pct': pct(sum(1 for r in records if r['license'].get('recognized'))),
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(f'wrote {OUT} (n={n})', file=sys.stderr)


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    return xs[len(xs) // 2] if xs else None


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'harvest': harvest, 'stats': stats}.get(cmd, stats)()
