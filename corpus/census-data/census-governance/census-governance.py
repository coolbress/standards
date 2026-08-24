#!/usr/bin/env python3
"""Re-examination census — turn two "[lit]-only" claims into real statistics.

(A) NON-FILE FOUNDATION (we said census-blind): OpenSSF Scorecard public API gives per-repo scores for
    Branch-Protection, Code-Review, CI-Tests, Pinned-Dependencies, Token-Permissions, SAST, Signed-Releases…
(B) ① PLANNING ARTIFACTS (we said not censusable): detect ADR / RFC / design-doc directories in the tree.

Reuses census-dev-environment/records.json (repo→archetype) + /tmp/dates.json (createdAt) — the SAME 429 set,
so results are directly comparable + recency-weightable.
Usage (repo root):  python docs/research/census-governance.py harvest [N] | stats
Out: census-governance/records.json (raw) + stats.json (computed).
"""
import json, os, re, subprocess, sys, time
from datetime import datetime
from collections import defaultdict

ROOT = 'docs/research/census-data'
REC = f'{ROOT}/census-governance/records.json'
REF = datetime(2026, 6, 24)
H = 2.0

# Scorecard checks relevant to the foundation/non-file blind spot (others stored too)
SC_CHECKS = ['Branch-Protection', 'Code-Review', 'CI-Tests', 'Pinned-Dependencies', 'Token-Permissions',
             'Dangerous-Workflow', 'Security-Policy', 'SAST', 'Dependency-Update-Tool', 'Maintained',
             'Signed-Releases', 'Vulnerabilities', 'Binary-Artifacts', 'License', 'Fuzzing']
PLANNING_FLAGS = ['adr_dir', 'rfc_dir', 'design_doc']

ADR = re.compile(r'(^|/)(docs?/)?(adr|adrs|architecture[-_]?decisions?|decisions?)/.+\.md$|(^|/)\d{3,4}-[\w-]+\.md$.*adr|\.adr\.md$', re.I | re.M)
ADR2 = re.compile(r'(^|/)(docs?/)?(adr|adrs)/', re.I | re.M)  # an adr/ dir at all
RFC = re.compile(r'(^|/)(docs?/)?rfcs?/', re.I | re.M)
DESIGN = re.compile(r'(^|/)(docs?/)?design([-_]docs?)?/|(^|/)DESIGN\.md$|(^|/)docs?/design/', re.I | re.M)


def gh(path, timeout=60):
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
            time.sleep(20); continue
        return None


def scorecard(repo, timeout=25):
    try:
        p = subprocess.run(['curl', '-s', '--max-time', str(timeout),
                            f'https://api.securityscorecards.dev/projects/github.com/{repo}'],
                           capture_output=True, text=True, timeout=timeout + 5)
        d = json.loads(p.stdout)
        if not isinstance(d, dict) or 'checks' not in d:
            return None
        return d
    except Exception:
        return None


def harvest(limit=None):
    recs = json.load(open(f'{ROOT}/census-dev-environment/records.json'))
    dates = {d['fullName']: d for d in json.load(open('/tmp/dates.json'))}
    sw = [r for r in recs if r.get('is_software')]
    if limit:
        sw = sw[:limit]
    out, total = [], len(sw)
    for i, r in enumerate(sw, 1):
        repo = r['repo']
        rec = {'repo': repo, 'archetype': r.get('archetype'),
               'created': (dates.get(repo) or {}).get('createdAt', '')[:10] or None}
        # (A) Scorecard
        sc = scorecard(repo)
        if sc:
            checks = {c['name']: c.get('score') for c in sc.get('checks', [])}
            rec['sc_overall'] = sc.get('score')
            rec['sc'] = {k: checks.get(k) for k in SC_CHECKS}
            rec['sc_data'] = True
        else:
            rec['sc_overall'] = None
            rec['sc'] = {k: None for k in SC_CHECKS}
            rec['sc_data'] = False
        # (B) planning artifacts from tree
        tree = gh(f'repos/{repo}/git/trees/HEAD?recursive=1')
        if isinstance(tree, dict) and 'tree' in tree:
            blob = '\n'.join(t.get('path', '') for t in tree['tree'])
            rec['adr_dir'] = bool(ADR2.search(blob) or ADR.search(blob))
            rec['rfc_dir'] = bool(RFC.search(blob))
            rec['design_doc'] = bool(DESIGN.search(blob))
            rec['tree_ok'] = True
        else:
            rec['adr_dir'] = rec['rfc_dir'] = rec['design_doc'] = None
            rec['tree_ok'] = False
        out.append(rec)
        if i % 20 == 0 or i == total:
            print(f'[{i}/{total}] {repo}  sc={rec["sc_overall"]} adr={rec["adr_dir"]} rfc={rec["rfc_dir"]}', flush=True)
        time.sleep(0.1)
    os.makedirs(f'{ROOT}/census-governance', exist_ok=True)
    dest = REC if not limit else f'{ROOT}/census-governance/records-smoke.json'
    json.dump(out, open(dest, 'w'), indent=2)
    print(f'\nDONE: {len(out)} repos -> {dest}')


def stats():
    recs = json.load(open(REC))
    rows = []
    for r in recs:
        c = r.get('created')
        try:
            c = datetime.strptime(c[:10], '%Y-%m-%d') if c else None
        except ValueError:
            c = None
        if not c:
            continue
        rows.append((r, c, 0.5 ** (((REF - c).days / 365.25) / H)))
    n = len(rows)
    young = [(r, c, w) for (r, c, w) in rows if c >= datetime(2021, 1, 1)]
    ny = len(young)

    # Scorecard: among repos WITH data, coverage + %>=7 (strong) uniform/weighted + mean score
    sc_cov = [(r, w) for r, _, w in rows if r.get('sc_data')]
    cov_pct = round(100 * len(sc_cov) / n) if n else 0
    sc_stats = {}
    for k in SC_CHECKS:
        vals = [(r['sc'].get(k), w) for r, w in sc_cov if r['sc'].get(k) is not None and r['sc'].get(k) >= 0]
        if not vals:
            sc_stats[k] = {'n': 0}
            continue
        wd = sum(w for _, w in vals)
        sc_stats[k] = {
            'n': len(vals),
            'mean': round(sum(v for v, _ in vals) / len(vals), 1),
            'wmean': round(sum(v * w for v, w in vals) / wd, 1),
            'pct_strong_uni': round(100 * sum(1 for v, _ in vals if v >= 7) / len(vals)),
            'pct_strong_wgt': round(100 * sum(w for v, w in vals if v >= 7) / wd),
        }

    # planning artifacts: adoption among tree_ok
    def adopt(f):
        d = [(r, w) for r, _, w in rows if r.get(f) is not None]
        wd = sum(w for _, w in d)
        yd = [r for r, _, _ in young if r.get(f) is not None]
        return {'uniform': round(100 * sum(1 for r, _ in d if r.get(f)) / len(d)) if d else 0,
                'weighted': round(100 * sum(w for r, w in d if r.get(f)) / wd) if wd else 0,
                'young': round(100 * sum(1 for r in yd if r.get(f)) / len(yd)) if yd else 0}
    plan = {f: adopt(f) for f in PLANNING_FLAGS}
    # any planning artifact
    for r, _, _ in rows:
        r['_any_plan'] = any(r.get(f) for f in PLANNING_FLAGS) if r.get('tree_ok') else None
    plan['any_planning_artifact'] = adopt('_any_plan')

    # by archetype: adr adoption + scorecard overall mean
    arche = defaultdict(list)
    for r, _, _ in rows:
        arche[r.get('archetype') or 'unknown'].append(r)
    by_arch = {}
    for a, rs in sorted(arche.items(), key=lambda kv: -len(kv[1])):
        scs = [x['sc_overall'] for x in rs if x.get('sc_overall') is not None]
        adrs = [x for x in rs if x.get('adr_dir') is not None]
        by_arch[a] = {'n': len(rs),
                      'sc_overall_mean': round(sum(scs) / len(scs), 1) if scs else None,
                      'adr_pct': round(100 * sum(1 for x in adrs if x['adr_dir']) / len(adrs)) if adrs else None,
                      'anyplan_pct': round(100 * sum(1 for x in rs if x.get('_any_plan')) / len([x for x in rs if x.get('tree_ok')])) if [x for x in rs if x.get('tree_ok')] else None}

    out = {'n': n, 'young_count': ny, 'scorecard_coverage_pct': cov_pct, 'ref': REF.strftime('%Y-%m-%d'),
           'scorecard': sc_stats, 'planning': plan, 'by_archetype': by_arch}
    json.dump(out, open(f'{ROOT}/census-governance/stats.json', 'w'), indent=2)

    print(f"n={n} | young={ny} | Scorecard data coverage = {cov_pct}% of repos\n")
    print("=== (A) NON-FILE FOUNDATION via OpenSSF Scorecard (among repos w/ a score) ===")
    print("CHECK                  n   mean  wmean  %strong(uni/wgt)")
    for k in SC_CHECKS:
        s = sc_stats[k]
        if s['n'] == 0:
            print(f"{k:<22} (no data)")
        else:
            print(f"{k:<22} {s['n']:>3}  {s['mean']:>4}  {s['wmean']:>4}   {s['pct_strong_uni']:>3}/{s['pct_strong_wgt']}")
    print("\n=== (B) ① PLANNING ARTIFACTS (tree presence) ===")
    print("FLAG                    uni  wgt  young")
    for f in PLANNING_FLAGS + ['any_planning_artifact']:
        s = plan[f]
        print(f"{f:<22} {s['uniform']:>3} {s['weighted']:>4} {s['young']:>5}")
    print("\n=== BY ARCHETYPE (scorecard overall mean | ADR% | any-plan%) ===")
    for a, row in by_arch.items():
        print(f"{a:<16} n={row['n']:>3}  sc={row['sc_overall_mean']}  adr={row['adr_pct']}%  anyplan={row['anyplan_pct']}%")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if mode == 'harvest':
        harvest(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    else:
        stats()
