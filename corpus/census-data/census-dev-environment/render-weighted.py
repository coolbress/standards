#!/usr/bin/env python3
"""Compute uniform vs recency-weighted vs young-cohort adoption from recovered per-repo records.

Inputs:  census-dev-environment/records.json (per-repo components+tools, recovered from census transcripts)
         /tmp/dates.json (gh search repos -> fullName, createdAt, pushedAt)
Method:  recency weight w = 0.5^(age_years / H), H=2yr half-life, age from createdAt vs REF date.
         young cohort = createdAt >= 2021-01-01 (simple mean within).  Weight by TIME, never stars.
Output:  census-dev-environment/weighted-stats.json + a markdown summary to stdout.
"""
import json
from datetime import datetime
from collections import defaultdict

REF = datetime(2026, 6, 23)
H = 2.0  # half-life years

COMP_KEYS = ['manifest','license','runtime_pin','pkg_manager_pin','lockfile','build_config','linter',
    'formatter','typechecker','editorconfig','precommit_hooks','test_framework','coverage_config','gitignore',
    'gitattributes','commit_convention','codeowners','issue_template','pr_template','ci','pr_title_check',
    'dep_bot','release_automation','supply_chain_security','readme','contributing','security_md',
    'code_of_conduct','changelog','docs_dir','devcontainer','dockerfile','env_example','task_runner',
    'editor_recommendations']
TOOL_FIELDS = ['linter','formatter','typechecker','test','pkg_manager','ci','dep_bot']

recs = json.load(open('docs/research/census-dev-environment/records.json'))
dates = {d['fullName']: d for d in json.load(open('/tmp/dates.json'))}

def created(repo):
    d = dates.get(repo)
    if not d or not d.get('createdAt'): return None
    return datetime.strptime(d['createdAt'][:10], '%Y-%m-%d')

sw = [r for r in recs if r.get('is_software')]
rows = []
for r in sw:
    c = created(r['repo'])
    if not c: continue
    age = (REF - c).days / 365.25
    w = 0.5 ** (age / H)
    rows.append((r, c, w))

n = len(rows)
matched_dates = n
W = sum(w for _, _, w in rows)
young = [(r, c, w) for (r, c, w) in rows if c >= datetime(2021, 1, 1)]
ny = len(young)

def has(rec, k):
    comps = rec.get('components') or {}
    return bool(comps.get(k))

stats = {}
for k in COMP_KEYS:
    uni = round(100 * sum(1 for r, _, _ in rows if has(r, k)) / n)
    wgt = round(100 * sum(w for r, _, w in rows if has(r, k)) / W)
    yng = round(100 * sum(1 for r, _, _ in young if has(r, k)) / ny) if ny else 0
    stats[k] = {'uniform': uni, 'weighted': wgt, 'young': yng, 'delta': wgt - uni}

def tally(field, weighted):
    t = defaultdict(float)
    for r, _, w in rows:
        v = (r.get('tools') or {}).get(field)
        if v and v not in ('none', ''):
            t[v] += w if weighted else 1
    return sorted(t.items(), key=lambda kv: -kv[1])[:6]

tools = {}
for f in TOOL_FIELDS:
    uni = [(t, round(c)) for t, c in tally(f, False)]
    wgt = [(t, round(c, 1)) for t, c in tally(f, True)]
    tools[f] = {'uniform': uni, 'weighted': wgt}

# age distribution sanity
med_year = sorted(c.year for _, c, _ in rows)[n // 2]
out = {'n_software': len(sw), 'n_with_dates': matched_dates, 'half_life_yr': H, 'ref': REF.strftime('%Y-%m-%d'),
       'young_count': ny, 'young_pct_of_pop': round(100 * ny / n), 'median_created_year': med_year,
       'effective_weight_sum': round(W, 1), 'components': stats, 'tools': tools}
json.dump(out, open('docs/research/census-dev-environment/weighted-stats.json', 'w'), indent=2)

# --- markdown summary ---
print(f"n={n} software w/ dates | young(2021+)={ny} ({out['young_pct_of_pop']}%) | median created year={med_year} | Weff={W:.1f}\n")
print("COMPONENT            uni  wgt  young  Δ(wgt-uni)")
movers = sorted(COMP_KEYS, key=lambda k: -abs(stats[k]['delta']))
for k in movers:
    s = stats[k]
    arrow = '↑' if s['delta'] > 3 else ('↓' if s['delta'] < -3 else ' ')
    print(f"{k:<20} {s['uniform']:>3} {s['weighted']:>4} {s['young']:>5}   {s['delta']:>+3} {arrow}")
print("\nTOOL WINNERS (uniform top  ||  recency-weighted top):")
for f in TOOL_FIELDS:
    u = ' '.join(f"{t}:{c}" for t, c in tools[f]['uniform'])
    w = ' '.join(f"{t}:{c}" for t, c in tools[f]['weighted'])
    print(f"  {f:<12} U[{u}]\n               W[{w}]")
