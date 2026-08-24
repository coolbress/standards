#!/usr/bin/env python3
"""④ release/ops census — harvest (gh-api) + recency-weighted stats, in ONE file.

Usage (run from repo root):
  python docs/research/census-release-ops.py harvest [N]  # (re)collect records.json; N=limit (smoke)
  python docs/research/census-release-ops.py stats        # recompute stats.json + markdown (default)

Reuses census-dev-environment/records.json (repo→archetype/language) + /tmp/dates.json (createdAt).
HARVEST = mechanical facts only, no LLM judgment: GitHub Releases/Tags API + commit-message sampling +
file-tree globs. STATS = uniform vs recency-weighted (w=0.5^(age/2yr)) vs young, + by-archetype slice.
Backs `04-release-ops.md`. Raw: census-release-ops/records.json ; computed: census-release-ops/stats.json.
"""
import json, os, re, subprocess, sys, time
from datetime import datetime
from collections import defaultdict

ROOT = 'docs/research/census-data'
REC = f'{ROOT}/census-release-ops/records.json'
REF = datetime(2026, 6, 24)
H = 2.0

BOOL_FLAGS = ['has_releases', 'has_release_notes', 'semver_any', 'cc_adopted',
              'changelog', 'container', 'cd_deploy', 'iac', 'observability']
RELEASE_HALF = {'has_releases', 'has_release_notes', 'semver_any', 'cc_adopted', 'changelog'}

# ---------- HARVEST ----------
SEMVER = re.compile(r'^v?\d+\.\d+\.\d+')
CC = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]*\))?!?:\s', re.I)
IAC = re.compile(r'(\.tf$|\.tf\.json$|(^|/)Chart\.ya?ml$|(^|/)values\.ya?ml$|Pulumi\.ya?ml$|'
                 r'(^|/)(k8s|kubernetes|manifests|helm|charts|deploy|deployment)/|kustomization\.ya?ml$|'
                 r'(^|/)(terraform|infra|infrastructure)/)', re.I | re.M)
OBS = re.compile(r'(prometheus\.ya?ml|(^|/)grafana/|otel[-_]?col|opentelemetry|otel-collector|'
                 r'(^|/)sentry\.|(^|/)dashboards/.*\.json$|sloth|openslo|\.slo\.ya?ml$|'
                 r'(^|/)alertmanager|(^|/)alerts?\.ya?ml$|datadog|newrelic)', re.I | re.M)
CD = re.compile(r'\.github/workflows/.*(deploy|release|publish|cd|delivery)[^/]*\.ya?ml$', re.I | re.M)
CONTAINER = re.compile(r'(^|/)Dockerfile|(^|/)docker-compose|(^|/)compose\.ya?ml$', re.I | re.M)
CHANGELOG = re.compile(r'(^|/)CHANGELOG', re.I | re.M)


def gh(path, timeout=45):
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


def _median(xs):
    xs = sorted(xs); n = len(xs)
    if not n: return None
    return xs[n // 2] if n % 2 else round((xs[n // 2 - 1] + xs[n // 2]) / 2, 1)


def _dt(s):
    try: return datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S')
    except (ValueError, TypeError): return None


def harvest(limit=None):
    recs = json.load(open(f'{ROOT}/census-dev-environment/records.json'))
    dates = {d['fullName']: d for d in json.load(open('/tmp/dates.json'))}
    sw = [r for r in recs if r.get('is_software')]
    if limit: sw = sw[:limit]
    out, total = [], len(sw)
    for i, r in enumerate(sw, 1):
        repo = r['repo']
        rec = {'repo': repo, 'archetype': r.get('archetype'), 'language': r.get('language'),
               'created': (dates.get(repo) or {}).get('createdAt', '')[:10] or None}
        rel = gh(f'repos/{repo}/releases?per_page=100')
        if isinstance(rel, list) and rel:
            ts = sorted([t for t in (_dt(x.get('published_at') or '') for x in rel) if t], reverse=True)
            gaps = [(ts[j] - ts[j + 1]).days for j in range(len(ts) - 1)]
            rec.update(has_releases=True, n_releases=len(rel),
                       has_release_notes=any((x.get('body') or '').strip() for x in rel), cadence_days=_median(gaps))
        else:
            rec.update(has_releases=False, n_releases=0, has_release_notes=False, cadence_days=None)
        tags = gh(f'repos/{repo}/tags?per_page=100')
        if isinstance(tags, list) and tags:
            names = [t.get('name', '') for t in tags]; hits = sum(1 for n in names if SEMVER.match(n))
            rec.update(semver_any=hits > 0, semver_ratio=round(hits / len(names), 2), n_tags=len(names))
        else:
            rec.update(semver_any=False, semver_ratio=0.0, n_tags=0)
        commits = gh(f'repos/{repo}/commits?per_page=30')
        if isinstance(commits, list) and commits:
            msgs = [(c.get('commit', {}).get('message', '') or '').split('\n')[0] for c in commits if c.get('commit')]
            nm = [m for m in msgs if not m.startswith('Merge ')]; hits = sum(1 for m in nm if CC.match(m))
            ratio = round(hits / len(nm), 2) if nm else 0.0
            rec.update(cc_ratio=ratio, cc_adopted=ratio >= 0.3, n_commits_sampled=len(nm))
        else:
            rec.update(cc_ratio=0.0, cc_adopted=False, n_commits_sampled=0)
        tree = gh(f'repos/{repo}/git/trees/HEAD?recursive=1', timeout=60)
        if isinstance(tree, dict) and 'tree' in tree:
            blob = '\n'.join(t.get('path', '') for t in tree['tree'])
            rec.update(iac=bool(IAC.search(blob)), observability=bool(OBS.search(blob)), cd_deploy=bool(CD.search(blob)),
                       container=bool(CONTAINER.search(blob)), changelog=bool(CHANGELOG.search(blob)),
                       tree_truncated=bool(tree.get('truncated')))
        else:
            rec.update(iac=None, observability=None, cd_deploy=None, container=None, changelog=None, tree_truncated=None)
        out.append(rec)
        if i % 20 == 0 or i == total:
            print(f'[{i}/{total}] {repo}  rel={rec["has_releases"]} svmr={rec["semver_any"]} '
                  f'cc={rec["cc_ratio"]} iac={rec["iac"]}', flush=True)
        time.sleep(0.1)
    os.makedirs(f'{ROOT}/census-release-ops', exist_ok=True)
    dest = REC if not limit else f'{ROOT}/census-release-ops/records-smoke.json'  # smoke never clobbers full set
    json.dump(out, open(dest, 'w'), indent=2)
    print(f'\nDONE: {len(out)} repos -> {dest}')


# ---------- STATS ----------
def stats():
    recs = json.load(open(REC))
    rows = []
    for r in recs:
        c = r.get('created')
        try: c = datetime.strptime(c[:10], '%Y-%m-%d') if c else None
        except ValueError: c = None
        if not c: continue
        rows.append((r, c, 0.5 ** (((REF - c).days / 365.25) / H)))
    n = len(rows); Wt = sum(w for _, _, w in rows)
    young = [(r, c, w) for (r, c, w) in rows if c >= datetime(2021, 1, 1)]; ny = len(young)

    def adopt(f):
        ud = [(r, w) for r, _, w in rows if r.get(f) is not None]
        wd = sum(w for _, w in ud)
        yd = [r for r, _, _ in young if r.get(f) is not None]
        return {'uniform': round(100 * sum(1 for r, _ in ud if r.get(f)) / len(ud)) if ud else 0,
                'weighted': round(100 * sum(w for r, w in ud if r.get(f)) / wd) if wd else 0,
                'young': round(100 * sum(1 for r in yd if r.get(f)) / len(yd)) if yd else 0,
                'delta': (round(100 * sum(w for r, w in ud if r.get(f)) / wd) if wd else 0)
                         - (round(100 * sum(1 for r, _ in ud if r.get(f)) / len(ud)) if ud else 0),
                'coverage': round(100 * len(ud) / n) if n else 0}

    flags = {f: adopt(f) for f in BOOL_FLAGS}

    def wmean(field):
        num = den = 0.0
        for r, _, w in rows:
            v = r.get(field)
            if v is not None: num += w * v; den += w
        return round(num / den, 2) if den else None

    cad = sorted(r.get('cadence_days') for r, _, _ in rows if r.get('cadence_days') is not None)
    numeric = {'semver_ratio_wmean': wmean('semver_ratio'), 'cc_ratio_wmean': wmean('cc_ratio'),
               'cadence_days_median': cad[len(cad) // 2] if cad else None, 'n_with_cadence': len(cad)}
    arche = defaultdict(list)
    for r, _, _ in rows: arche[r.get('archetype') or 'unknown'].append(r)
    by_arch = {}
    for a, rs in sorted(arche.items(), key=lambda kv: -len(kv[1])):
        row = {'n': len(rs)}
        for f in BOOL_FLAGS:
            d = [x for x in rs if x.get(f) is not None]
            row[f] = round(100 * sum(1 for x in d if x.get(f)) / len(d)) if d else None
        by_arch[a] = row
    out = {'n': n, 'young_count': ny, 'young_pct': round(100 * ny / n), 'ref': REF.strftime('%Y-%m-%d'),
           'half_life_yr': H, 'median_created_year': sorted(c.year for _, c, _ in rows)[n // 2],
           'effective_weight_sum': round(Wt, 1), 'tree_truncated': sum(1 for r, _, _ in rows if r.get('tree_truncated')),
           'tree_fetch_failed': sum(1 for r, _, _ in rows if r.get('container') is None),
           'flags': flags, 'numeric': numeric, 'by_archetype': by_arch}
    json.dump(out, open(f'{ROOT}/census-release-ops/stats.json', 'w'), indent=2)
    print(f"n={n} | young={ny} ({out['young_pct']}%) | median created={out['median_created_year']} | "
          f"Weff={Wt:.1f} | tree-fail={out['tree_fetch_failed']} trunc={out['tree_truncated']}\n")
    print("FLAG                 uni  wgt  young   Δ   cov  half")
    for f in BOOL_FLAGS:
        s = flags[f]; arrow = '↑' if s['delta'] > 3 else ('↓' if s['delta'] < -3 else ' ')
        print(f"{f:<20} {s['uniform']:>3} {s['weighted']:>4} {s['young']:>5}  {s['delta']:>+3}{arrow} {s['coverage']:>3}%  "
              f"{'REL' if f in RELEASE_HALF else 'OPS'}")
    print(f"\nNUMERIC: semver_ratio(wgt)={numeric['semver_ratio_wmean']} | cc_ratio(wgt)={numeric['cc_ratio_wmean']} | "
          f"cadence median={numeric['cadence_days_median']}d (n={numeric['n_with_cadence']})")
    print("\nBY ARCHETYPE (uniform % within):")
    print("archetype       n   rel notes svmr  cc chlg | cont  cd iac obs")
    for a, row in by_arch.items():
        g = lambda k: (f"{row.get(k):>3}" if row.get(k) is not None else "  -")
        print(f"{a:<14} {row['n']:>3}  {g('has_releases')} {g('has_release_notes')} {g('semver_any')} "
              f"{g('cc_adopted')} {g('changelog')} | {g('container')} {g('cd_deploy')} {g('iac')} {g('observability')}")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if mode == 'harvest':
        harvest(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    else:
        stats()
