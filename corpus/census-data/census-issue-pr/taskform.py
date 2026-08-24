#!/usr/bin/env python3
"""Issue-FORM TYPE enrichment — does the real world ship a "task"-class issue form?

The N=2000 census (census2k.py) recorded issue-form *field labels* but discarded the form FILE NAMES and
each form's top-level `name:` title — so it cannot answer "beyond bug_report + feature_request, what third
forms do repos actually ship, and is a task/chore/maintenance form a real pattern?". This enrichment re-reads
the `.github/ISSUE_TEMPLATE/` directory for every repo that has ≥1 YAML form (population from records-2k.json)
and classifies each form by filename + `name:` into a small taxonomy, so the "task form" question is answered
from evidence rather than asserted.

Reuses census2k's GraphQL-batched pattern (itdir tree + blob text). REST-core budget; hourly-reset aware.

Run from repo root:
  python docs/research/census-data/census-issue-pr/taskform.py harvest   # → taskform-records.json + taskform-stats.json
  python docs/research/census-data/census-issue-pr/taskform.py stats      # recompute from taskform-records.json
Out: census-issue-pr/{taskform-records.json, taskform-stats.json}
"""
import json, re, subprocess, sys, time
from collections import Counter

DIR = 'docs/research/census-data/census-issue-pr'
SRC = f'{DIR}/records-2k.json'
REC = f'{DIR}/taskform-records.json'
OUT = f'{DIR}/taskform-stats.json'
BATCH = 8

NAME_RE = re.compile(r'^name:\s*(.+?)\s*$', re.M)  # top-level `name:` of a GitHub issue FORM (YAML)

# Classification taxonomy — matched against (filename + form `name:` title), lowercased, first hit wins.
# Order matters: bug/feature first (the two defaults), then the task-class we are testing, then the rest.
CATEGORIES = [
    ('bug',        ['bug', 'crash', 'defect', 'regression', 'problem', 'error report']),
    ('feature',    ['feature', 'enhancement', 'idea', 'proposal', 'request', 'suggestion', 'rfc']),
    ('task',       ['task', 'chore', 'maintenance', 'refactor', 'tech debt', 'tech-debt', 'techdebt',
                    'tracking', 'epic', 'work item', 'housekeeping', 'cleanup', 'to-do']),
    ('docs',       ['doc', 'documentation']),
    ('question',   ['question', 'support', 'help', 'discussion', 'ask', 'how to', 'how-to']),
    ('security',   ['security', 'vulnerab', 'cve']),
    ('perf',       ['perf', 'performance', 'slow']),
]


def classify(filename, form_name):
    # Filename is the more reliable signal (a "Documentation problem" form is filed as documentation.yaml,
    # but its `name:` contains "problem" → would mis-hit bug). So classify by FILENAME first, then fall
    # back to the form `name:` only when the filename is uninformative.
    fn = filename.lower()
    for cat, terms in CATEGORIES:
        if any(t in fn for t in terms):
            return cat
    nm = form_name.lower()
    for cat, terms in CATEGORIES:
        if any(t in nm for t in terms):
            return cat
    return 'other'


def _gql(batch):
    parts = []
    for i, repo in enumerate(batch):
        if '/' not in repo:
            continue
        owner, name = repo.split('/', 1)
        o, n = json.dumps(owner), json.dumps(name)
        parts.append(
            f'r{i}: repository(owner: {o}, name: {n}) {{ '
            f'itdir: object(expression: "HEAD:.github/ISSUE_TEMPLATE") '
            f'{{ ... on Tree {{ entries {{ name object {{ ... on Blob {{ text }} }} }} }} }} }}')
    query = '{\n' + '\n'.join(parts) + '\n  rateLimit { remaining resetAt }\n}'
    try:
        p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'],
                           capture_output=True, text=True, timeout=120)
        return json.loads(p.stdout) if p.stdout else None
    except Exception:
        return None


def _wait_for_reset(reset_at):
    if not reset_at:
        time.sleep(60); return
    try:
        target = time.mktime(time.strptime(reset_at, '%Y-%m-%dT%H:%M:%SZ'))
        wait = max(0, target - time.time()) + 15
    except Exception:
        wait = 60
    print(f'  rate-limit: sleeping {int(wait)}s to resetAt {reset_at}', file=sys.stderr)
    time.sleep(wait)


def _parse_repo(node):
    """Return list of {file, name, category} for each YAML form (config.yml excluded)."""
    forms = []
    itdir = node.get('itdir') or {}
    for e in itdir.get('entries', []) or []:
        fn = e.get('name', '')
        if not fn.lower().endswith(('.yml', '.yaml')):
            continue
        if fn.lower() == 'config.yml' or fn.lower() == 'config.yaml':
            continue
        text = ((e.get('object') or {}).get('text')) or ''
        m = NAME_RE.search(text)
        form_name = m.group(1).strip().strip('"\'') if m else ''
        forms.append({'file': fn, 'name': form_name, 'category': classify(fn, form_name)})
    return forms


def harvest():
    src = json.load(open(SRC))
    pop = [r['repo'] for r in src if r.get('issue_forms', 0) > 0]
    print(f'population (repos with >=1 YAML form): {len(pop)}', file=sys.stderr)
    records = []
    i = 0
    while i < len(pop):
        batch = pop[i:i + BATCH]
        data = _gql(batch)
        if not data or 'data' not in data:
            _wait_for_reset(None); continue
        d = data['data']
        for j, repo in enumerate(batch):
            node = d.get(f'r{j}')
            if not node:
                continue
            forms = _parse_repo(node)
            records.append({'repo': repo, 'forms': forms})
        rl = d.get('rateLimit') or {}
        if rl.get('remaining', 1) is not None and rl.get('remaining', 1) < 20:
            _wait_for_reset(rl.get('resetAt'))
        i += BATCH
        if i % 80 == 0:
            print(f'  {i}/{len(pop)}', file=sys.stderr)
            json.dump(records, open(REC, 'w'), indent=2)
    json.dump(records, open(REC, 'w'), indent=2)
    print(f'wrote {REC} ({len(records)} repos)', file=sys.stderr)
    stats()


def stats():
    records = json.load(open(REC))
    n = len(records)
    # per-repo: does it ship >=1 of each category (beyond bug/feature)?
    repo_has = Counter()
    cat_form_total = Counter()          # total forms per category (form-level)
    extra_forms = Counter()             # non-bug/feature/config forms by category
    task_names = Counter()              # the actual `name:`/file of task-class forms
    n_forms_dist = Counter()
    repos_with_extra = 0                # ships >=1 form that is NOT bug/feature
    repos_with_task = 0                 # ships >=1 task-class form
    for rec in records:
        cats = set()
        n_forms_dist[len(rec['forms'])] += 1
        has_extra = False
        has_task = False
        for f in rec['forms']:
            c = f['category']
            cat_form_total[c] += 1
            cats.add(c)
            if c not in ('bug', 'feature'):
                extra_forms[c] += 1
                has_extra = True
            if c == 'task':
                has_task = True
                key = (f['name'] or f['file'])
                task_names[key] += 1
        for c in cats:
            repo_has[c] += 1
        if has_extra:
            repos_with_extra += 1
        if has_task:
            repos_with_task += 1

    def pct(x):
        return round(x * 100 / n, 1) if n else 0.0

    out = {
        'n_form_repos': n,
        'source': 'repos with >=1 YAML issue form from records-2k.json; ISSUE_TEMPLATE dir re-harvested via GraphQL (taskform.py)',
        'repos_shipping_ge1_task_class_form_pct': pct(repos_with_task),
        'repos_shipping_ge1_task_class_form_n': repos_with_task,
        'repos_shipping_any_extra_beyond_bug_feature_pct': pct(repos_with_extra),
        'repo_pct_by_category': {c: pct(repo_has[c]) for c, _ in CATEGORIES + [('other', None)]},
        'repo_n_by_category': {c: repo_has[c] for c, _ in CATEGORIES + [('other', None)]},
        'extra_forms_by_category (form-level, excl bug/feature)': dict(extra_forms.most_common()),
        'form_count_distribution': dict(sorted(n_forms_dist.items())),
        'top_task_class_form_names': task_names.most_common(30),
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f'\nwrote {OUT} (n={n})', file=sys.stderr)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'harvest': harvest, 'stats': stats}.get(cmd, stats)()
