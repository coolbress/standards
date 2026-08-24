#!/usr/bin/env python3
"""Issue/PR WRITING-CONVENTIONS census — the "작성법" depth the header/label censuses discarded.

census2k.py recorded WHICH sections exist (field labels, PR headers, issue-template types). It fetched the
full form/PR bodies but parsed only names out of them, so it cannot answer HOW each section is written — the
field TYPE (textarea/input/dropdown/checkboxes), whether it is REQUIRED, whether it carries help text
(description/placeholder), the CoC / preflight checkbox patterns, and — on the PR side — whether the checklist
ships empty `- [ ]` vs pre-checked, whether "Type of change" is a checkbox list vs free text, and how much
HTML-comment guidance is embedded. Those conventions are the evidence a TIERED template standard needs.

This re-harvests the form/PR bodies for the template-bearing subset of records-2k.json (repos with >=1 YAML
form OR a PR template) and parses field-level structure with PyYAML, storing RICH per-form/per-PR records so
the conventions can be re-analysed later WITHOUT another harvest (the census2k lesson: don't discard structure).

Reuses census2k's GraphQL-batched pattern + taskform's category classifier (bug/feature/task/...).

Run from repo root:
  python docs/research/census-data/census-issue-pr/conventions.py harvest   # -> conventions-records.json + conventions-stats.json
  python docs/research/census-data/census-issue-pr/conventions.py stats      # recompute from conventions-records.json
Out: census-issue-pr/{conventions-records.json, conventions-stats.json}
"""
import json, re, subprocess, sys, time
from collections import Counter, defaultdict

import yaml

DIR = 'docs/research/census-data/census-issue-pr'
SRC = f'{DIR}/records-2k.json'
REC = f'{DIR}/conventions-records.json'
OUT = f'{DIR}/conventions-stats.json'
# --- wide (N=6,582) confirmation pass: reuse the governance-floor pool, template-bearing subset ---
GOVFLOOR = 'docs/research/census-data/census-governance-floor/records.json'
REC_WIDE = f'{DIR}/conventions-6k-records.json'
OUT_WIDE = f'{DIR}/conventions-6k-stats.json'
# --- section-ROSTER pass: which canonical sections each form-category ships (re-harvest to capture LABELS) ---
REC_ROSTER = f'{DIR}/conventions-roster-records.json'
OUT_ROSTER = f'{DIR}/conventions-roster.json'
BATCH = 8

HEADER = re.compile(r'^#{1,6}\s+(.+?)\s*$', re.M)
NAME_RE = re.compile(r'^name:\s*(.+?)\s*$', re.M)

# taskform.py's taxonomy (filename-first classification) — kept in sync deliberately.
CATEGORIES = [
    ('bug',      ['bug', 'crash', 'defect', 'regression', 'problem', 'error report']),
    ('feature',  ['feature', 'enhancement', 'idea', 'proposal', 'request', 'suggestion', 'rfc']),
    ('task',     ['task', 'chore', 'maintenance', 'refactor', 'tech debt', 'tech-debt', 'techdebt',
                  'tracking', 'epic', 'work item', 'housekeeping', 'cleanup', 'to-do']),
    ('docs',     ['doc', 'documentation']),
    ('question', ['question', 'support', 'help', 'discussion', 'ask', 'how to', 'how-to']),
    ('security', ['security', 'vulnerab', 'cve']),
    ('perf',     ['perf', 'performance', 'slow']),
]
FIELD_TYPES = ('markdown', 'textarea', 'input', 'dropdown', 'checkboxes')
COC_RE = re.compile(r'code of conduct', re.I)
PREFLIGHT_RE = re.compile(r'existing issue|already (been )?(reported|filed|open)|searched', re.I)
TOC_RE = re.compile(r'type[s]? of change', re.I)

# --- section-ROSTER clustering: map a free-text field label to a canonical section bucket ---
# Order = match priority (specific → generic; first hit wins). 'other' = the unclustered tail (reported so
# the taxonomy can be refined). Labels are free text → this clustering carries JUDGMENT; the tail report +
# per-bucket required cross-check keep it honest. Raw labels are stored, so re-bucketing needs no re-harvest.
SECTION_BUCKETS = [
    ('preflight',       ['existing issue', 'already been', 'already exist', 'is there an existing',
                         'searched', 'search the', 'search before', 'duplicate', 'before submitting',
                         'before you', 'prerequisite', 'checklist', 'acknowledg', 'have you',
                         'self check', 'self-check']),
    ('code_of_conduct', ['code of conduct']),
    ('repro_steps',     ['reproduc', 'steps to', 'to trigger', 'minimal repro', 'how do you trigger',
                         'how to trigger', '复现', '重现']),
    ('expected',        ['expect', 'should happen', 'should have happen', 'should occur',
                         'desired behav', '预期']),
    ('actual',          ['actual', 'current behav', 'what actually', 'happens instead',
                         'what went wrong', 'observed behav', '实际']),
    ('environment',     ['version', 'environment', 'operating system', 'platform', 'browser',
                         'device', 'runtime', 'system info', 'your os', 'os:', 'dependencies',
                         'installation', 'configuration', '操作系统']),
    ('logs',            ['log', 'stack trace', 'traceback', 'screenshot', 'screen shot', 'recording',
                         'error message', 'error output', 'relevant output', 'console']),
    ('proposed',        ['solution', 'proposal', 'propose', 'suggest', 'desired', 'like to see',
                         'want to happen', 'feature you', 'describe the feature', 'what you want']),
    ('alternatives',    ['alternativ', 'workaround', 'other approach', 'considered']),
    ('problem',         ['problem', 'motivation', 'use case', 'pain point', 'why do you',
                         'related to a problem', 'what are you trying']),
    ('acceptance',      ['acceptance', 'definition of done', 'success crit', 'requirements',
                         'expected outcome', 'done when']),
    ('scope',           ['scope', 'deliverable', 'subtask', 'sub-task', 'implementation',
                         'to-do', 'to do', 'tasks']),
    ('goal',            ['goal', 'objective', 'summary of', 'what needs to']),
    ('description',     ['describe', 'description', 'summary', 'what happened', 'the bug',
                         'the problem', 'overview', 'issue', '问题描述', '描述']),
    ('context',         ['context', 'additional', 'anything else', 'other info',
                         'other information', 'notes', 'misc', 'more info', 'details',
                         'references', '补充']),
]


def bucketize(label):
    """Map a raw field label to a canonical section key (or 'other' / None for empty)."""
    l = (label or '').lower()
    if not l:
        return None
    for key, kws in SECTION_BUCKETS:
        if any(k in l for k in kws):
            return key
    return 'other'


def classify(filename, form_name):
    fn = filename.lower()
    for cat, terms in CATEGORIES:
        if any(t in fn for t in terms):
            return cat
    nm = (form_name or '').lower()
    for cat, terms in CATEGORIES:
        if any(t in nm for t in terms):
            return cat
    return 'other'


# ---- parsers ------------------------------------------------------------------------------------
def parse_form(fn, text):
    """Parse ONE GitHub issue FORM yaml into {file,name,category,n_fields,fields[],has_coc,has_preflight}.
    A field = {type, required, has_label, has_description, has_placeholder, has_options, render}.
    Non-form YAML / jinja-broken YAML → returns a minimal record flagged parse_ok=False."""
    rec = {'file': fn, 'name': '', 'category': 'other', 'parse_ok': False,
           'n_fields': 0, 'fields': [], 'has_coc': False, 'has_preflight': False}
    m = NAME_RE.search(text)
    if m:
        rec['name'] = m.group(1).strip().strip('"\'')
    rec['category'] = classify(fn, rec['name'])
    try:
        doc = yaml.safe_load(text)
    except Exception:
        return rec
    if not isinstance(doc, dict):
        return rec
    body = doc.get('body')
    if not isinstance(body, list):
        # a valid form must have a body list; markdown-template-as-yaml won't
        rec['parse_ok'] = isinstance(doc.get('name'), str)
        return rec
    rec['parse_ok'] = True
    for el in body:
        if not isinstance(el, dict):
            continue
        ftype = el.get('type')
        if ftype not in FIELD_TYPES:
            continue
        attrs = el.get('attributes') or {}
        vals = el.get('validations') or {}
        label = attrs.get('label') or ''
        options = attrs.get('options')
        field = {
            'type': ftype,
            'required': bool(vals.get('required')),
            'has_label': bool(label),
            'label': (label or '').strip()[:120],   # raw label kept → section-roster clustering is re-analysable offline
            'has_description': bool(attrs.get('description')),
            'has_placeholder': bool(attrs.get('placeholder')),
            'has_options': bool(options),
            'render': attrs.get('render') or None,
        }
        rec['fields'].append(field)
        # CoC / preflight are almost always a `checkboxes` block whose label/options mention it
        blob = label
        if isinstance(options, list):
            blob += ' ' + ' '.join(str((o or {}).get('label', '')) for o in options if isinstance(o, dict))
        if ftype == 'checkboxes':
            if COC_RE.search(blob):
                rec['has_coc'] = True
            if PREFLIGHT_RE.search(blob):
                rec['has_preflight'] = True
    rec['n_fields'] = len(rec['fields'])
    return rec


def parse_pr(text):
    """Parse a PR template markdown into checklist-style + type-of-change-style + comment-guidance stats."""
    if not text:
        return None
    empty = len(re.findall(r'^\s*[-*]\s+\[ \]', text, re.M))
    checked = len(re.findall(r'^\s*[-*]\s+\[[xX]\]', text, re.M))
    headers = [h.strip().lower() for h in HEADER.findall(text)]
    # Type-of-change style: find the "type of change" line, look at the ~15 lines after it for checkboxes
    toc_style = 'none'
    tm = TOC_RE.search(text)
    if tm:
        after = text[tm.end():tm.end() + 600]
        if re.search(r'^\s*[-*]\s+\[[ xX]\]', after, re.M):
            toc_style = 'checkbox'
        elif re.search(r'^\s*[-*]\s+\S', after, re.M):
            toc_style = 'bullet'
        else:
            toc_style = 'freetext'
    return {
        'n_sections': len(headers),
        'sections': headers,
        'checklist_empty': empty,
        'checklist_checked': checked,
        'checklist_style': ('empty' if empty and empty >= checked else
                            'pre-checked' if checked else 'none'),
        'html_comment_count': text.count('<!--'),
        'type_of_change_present': bool(tm),
        'type_of_change_style': toc_style,
        'n_chars': len(text),
    }


# ---- GraphQL harvest (itdir text + PR text only — lean) -----------------------------------------
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
            f'{{ ... on Tree {{ entries {{ name object {{ ... on Blob {{ text }} }} }} }} }} '
            f'pr1: object(expression: "HEAD:.github/PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }} '
            f'pr2: object(expression: "HEAD:PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }} '
            f'pr3: object(expression: "HEAD:docs/PULL_REQUEST_TEMPLATE.md") {{ ... on Blob {{ text }} }} }}')
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


def _parse_node(repo, stars, node):
    forms = []
    itdir = node.get('itdir') or {}
    for e in itdir.get('entries', []) or []:
        fn = e.get('name', '')
        if not fn.lower().endswith(('.yml', '.yaml')):
            continue
        if fn.lower() in ('config.yml', 'config.yaml'):
            continue
        text = ((e.get('object') or {}).get('text')) or ''
        forms.append(parse_form(fn, text))
    pr = node.get('pr1') or node.get('pr2') or node.get('pr3')
    pr_text = pr.get('text') if pr else None
    return {'repo': repo, 'stars': stars, 'forms': forms, 'pr': parse_pr(pr_text)}


def _run_harvest(pop, stars, rec_path, out_path, analyze=None):
    print(f'population (form OR pr-template repos): {len(pop)}', file=sys.stderr)
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
            records.append(_parse_node(repo, stars.get(repo), node))
        rl = d.get('rateLimit') or {}
        if rl.get('remaining', 9999) is not None and rl.get('remaining', 9999) < 50:
            _wait_for_reset(rl.get('resetAt'))
        i += BATCH
        if i % 80 == 0:
            print(f'  {i}/{len(pop)}', file=sys.stderr)
            json.dump(records, open(rec_path, 'w'))
        time.sleep(0.2)
    json.dump(records, open(rec_path, 'w'))
    print(f'wrote {rec_path} ({len(records)} repos)', file=sys.stderr)
    (analyze or stats)(rec_path, out_path)


def harvest():
    """Top-2000 pass — the template-bearing subset of records-2k.json (star floor 8.2k)."""
    src = json.load(open(SRC))
    stars = {r['repo']: r.get('stars') for r in src}
    pop = [r['repo'] for r in src if r.get('issue_forms', 0) > 0 or r.get('has_pr_tmpl')]
    _run_harvest(pop, stars, REC, OUT)


def harvest_wide():
    """N=6,582 confirmation pass — the template-bearing subset of the governance-floor pool (star floor 29).
    Reaches the less-governed long tail top-2000 excludes → tests whether the conventions hold at wider N or
    are a top-repo artifact (mirrors the governance-floor presence-fell-at-wider-N check). Append-only: writes
    a SEPARATE conventions-6k-* dataset; the top-2000 conventions-records.json is preserved untouched."""
    src = json.load(open(GOVFLOOR))
    stars = {r['repo']: r.get('stars') for r in src}
    pop = [r['repo'] for r in src if r.get('issue_forms') or r.get('pr_template')]
    _run_harvest(pop, stars, REC_WIDE, OUT_WIDE)


def harvest_roster():
    """Section-ROSTER pass — re-harvest the top-2000 template-bearing subset CAPTURING field labels (the
    writing-method pass stored only has_label booleans), so labels cluster into canonical sections per
    form-category. Answers 'which sections does a bug/feature/task form ship' — the roster layer the
    writing-method census left open. Writes SEPARATE conventions-roster-* files (append-only: the
    writing-method conventions-records.json is untouched). Uses the SENIOR reference class (top-2000) —
    the class gingoa emulates — and conventions were already wide-confirmed stable across N."""
    src = json.load(open(SRC))
    stars = {r['repo']: r.get('stars') for r in src}
    pop = [r['repo'] for r in src if r.get('issue_forms', 0) > 0 or r.get('has_pr_tmpl')]
    _run_harvest(pop, stars, REC_ROSTER, OUT_ROSTER, analyze=roster)


def _round(x, d=1):
    return round(x, d) if x is not None else None


def stats(rec_path=REC, out_path=OUT):
    records = json.load(open(rec_path))
    # ---- issue-form conventions ----
    all_fields = []                      # (category, field)
    form_cats = Counter()
    fields_per_form = defaultdict(list)  # category -> [n_fields]
    coc_forms = preflight_forms = form_total = parse_ok = 0
    for rec in records:
        for f in rec['forms']:
            form_total += 1
            if f.get('parse_ok'):
                parse_ok += 1
            cat = f['category']
            form_cats[cat] += 1
            fields_per_form[cat].append(f['n_fields'])
            if f['has_coc']:
                coc_forms += 1
            if f['has_preflight']:
                preflight_forms += 1
            for fld in f['fields']:
                all_fields.append((cat, fld))

    n_fields = len(all_fields)
    type_dist = Counter(fld['type'] for _, fld in all_fields)
    # required-rate over INPUT fields (markdown blocks are never "required")
    input_like = [(c, f) for c, f in all_fields if f['type'] in ('textarea', 'input', 'dropdown', 'checkboxes')]
    n_input = len(input_like)
    req = sum(1 for _, f in input_like if f['required'])
    help_have = sum(1 for _, f in input_like if f['has_description'] or f['has_placeholder'])
    # required-rate by field-type
    req_by_type = {}
    for t in ('textarea', 'input', 'dropdown', 'checkboxes'):
        sub = [f for _, f in input_like if f['type'] == t]
        req_by_type[t] = _round(100 * sum(bool(f['required']) for f in sub) / len(sub)) if sub else None
    # required-rate by category (input-like)
    req_by_cat = {}
    for cat in ('bug', 'feature', 'task', 'docs', 'question', 'other'):
        sub = [f for c, f in input_like if c == cat]
        req_by_cat[cat] = _round(100 * sum(bool(f['required']) for f in sub) / len(sub)) if sub else None

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    # ---- PR conventions ----
    prs = [r['pr'] for r in records if r.get('pr')]
    n_pr = len(prs)
    with_checklist = [p for p in prs if p['checklist_empty'] or p['checklist_checked']]
    toc_present = [p for p in prs if p['type_of_change_present']]

    out = {
        'source': 'writing-conventions re-harvest of the template-bearing subset of records-2k.json (conventions.py)',
        'n_repos': len(records),
        # ---------- ISSUE FORMS ----------
        'issue_form': {
            'n_forms': form_total,
            'parse_ok_pct': _round(100 * parse_ok / form_total) if form_total else None,
            'forms_by_category': dict(form_cats.most_common()),
            'n_fields': n_fields,
            'field_type_distribution_pct': {t: _round(100 * type_dist[t] / n_fields) for t in FIELD_TYPES} if n_fields else {},
            'required_rate_input_fields_pct': _round(100 * req / n_input) if n_input else None,
            'help_text_rate_input_fields_pct': _round(100 * help_have / n_input) if n_input else None,
            'required_rate_by_field_type_pct': req_by_type,
            'required_rate_by_category_pct': req_by_cat,
            'coc_checkbox_form_pct': _round(100 * coc_forms / form_total) if form_total else None,
            'preflight_checkbox_form_pct': _round(100 * preflight_forms / form_total) if form_total else None,
            'median_fields_per_form_by_category': {c: med(v) for c, v in fields_per_form.items()},
            'render_shell_field_n': sum(1 for _, f in all_fields if f.get('render')),
        },
        # ---------- PR TEMPLATE ----------
        'pr_template': {
            'n_pr_templates': n_pr,
            'checklist_style_pct': {
                s: _round(100 * sum(1 for p in prs if p['checklist_style'] == s) / n_pr)
                for s in ('empty', 'pre-checked', 'none')
            } if n_pr else {},
            'median_checklist_items': med([p['checklist_empty'] + p['checklist_checked'] for p in with_checklist]),
            'has_html_comment_guidance_pct': _round(100 * sum(1 for p in prs if p['html_comment_count'] > 0) / n_pr) if n_pr else None,
            'median_sections': med([p['n_sections'] for p in prs]),
            'type_of_change_present_pct': _round(100 * len(toc_present) / n_pr) if n_pr else None,
            'type_of_change_style_pct_among_present': {
                s: _round(100 * sum(1 for p in toc_present if p['type_of_change_style'] == s) / len(toc_present))
                for s in ('checkbox', 'bullet', 'freetext', 'none')
            } if toc_present else {},
        },
    }
    json.dump(out, open(out_path, 'w'), indent=2)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f'\nwrote {out_path}', file=sys.stderr)


def roster(rec_path=REC_ROSTER, out_path=OUT_ROSTER):
    """Per form-category (bug/feature/task), the canonical-section ROSTER: for each section bucket, the %
    of that category's forms carrying >=1 field in it (form-level presence, not field-count) + the
    required-rate of that section when present. Plus an unbucketed-label tail so the taxonomy can be
    refined by re-running roster() alone (labels are stored → no re-harvest)."""
    records = json.load(open(rec_path))
    cat_forms = Counter()                        # category -> #parse_ok forms
    cat_bucket = defaultdict(Counter)            # category -> bucket -> #forms containing it
    cat_bucket_req = defaultdict(Counter)        # category -> bucket -> #forms where it is required
    cat_sizes = defaultdict(list)                # category -> [#distinct buckets per form]
    unbucketed = Counter()                       # raw label -> count (the 'other' tail)
    for rec in records:
        for f in rec['forms']:
            if not f.get('parse_ok'):
                continue
            cat = f['category']
            cat_forms[cat] += 1
            in_form, req_in_form = set(), set()
            for fld in f['fields']:
                b = bucketize(fld.get('label'))
                if b is None:
                    continue
                if b == 'other':
                    unbucketed[(fld.get('label') or '')[:48]] += 1
                    continue
                in_form.add(b)
                if fld.get('required'):
                    req_in_form.add(b)
            for b in in_form:
                cat_bucket[cat][b] += 1
            for b in req_in_form:
                cat_bucket_req[cat][b] += 1
            cat_sizes[cat].append(len(in_form))

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    rosters = {}
    for cat in ('bug', 'feature', 'task'):       # the three forms gingoa ships
        nf = cat_forms[cat]
        if not nf:
            continue
        rows = [{
            'section': b,
            'present_pct': _round(100 * cnt / nf),
            'n_forms': cnt,
            'required_pct_of_present': _round(100 * cat_bucket_req[cat][b] / cnt) if cnt else None,
        } for b, cnt in cat_bucket[cat].most_common()]
        rosters[cat] = {'n_forms': nf, 'median_sections_per_form': med(cat_sizes[cat]), 'sections': rows}

    total_labels = sum(sum(1 for fld in f['fields'] if fld.get('label'))
                       for r in records for f in r['forms'] if f.get('parse_ok'))
    other_n = sum(unbucketed.values())
    out = {
        'source': 'section-roster clustering of issue-form field labels (conventions.py roster — top-2000 senior class)',
        'n_repos': len(records),
        'bucket_taxonomy': [k for k, _ in SECTION_BUCKETS],
        'unbucketed_label_pct': _round(100 * other_n / total_labels) if total_labels else None,
        'rosters': rosters,
        'top_unbucketed_labels': unbucketed.most_common(30),
    }
    json.dump(out, open(out_path, 'w'), indent=2)
    printable = {k: v for k, v in out.items() if k != 'top_unbucketed_labels'}
    print(json.dumps(printable, indent=2, ensure_ascii=False))
    print(f'\n-- unbucketed tail ({other_n}/{total_labels} labels = '
          f'{out["unbucketed_label_pct"]}%) — refine SECTION_BUCKETS from these, then re-run `roster` --',
          file=sys.stderr)
    for lbl, c in unbucketed.most_common(30):
        print(f'  {c:4}  {lbl}', file=sys.stderr)
    print(f'\nwrote {out_path}', file=sys.stderr)


def compare():
    """Side-by-side top-2000 (star floor 8.2k) vs wide N=6,582 (star floor 29) — does each convention HOLD?"""
    a = json.load(open(OUT))
    b = json.load(open(OUT_WIDE))
    print(f'{"metric":48} {"top-2000":>10} {"wide-6k":>10}   Δ')
    def row(label, va, vb):
        d = '' if va is None or vb is None else f'{vb - va:+.1f}'
        print(f'{label:48} {str(va):>10} {str(vb):>10}   {d}')
    fa, fb = a['issue_form'], b['issue_form']
    print('-- repos / forms --')
    row('n_repos', a['n_repos'], b['n_repos'])
    row('n_forms', fa['n_forms'], fb['n_forms'])
    row('n_fields', fa['n_fields'], fb['n_fields'])
    print('-- issue-form field types (%) --')
    for t in FIELD_TYPES:
        row(f'  {t}', fa['field_type_distribution_pct'].get(t), fb['field_type_distribution_pct'].get(t))
    print('-- issue-form quality rates (%) --')
    row('  required_rate_input_fields', fa['required_rate_input_fields_pct'], fb['required_rate_input_fields_pct'])
    row('  help_text_rate_input_fields', fa['help_text_rate_input_fields_pct'], fb['help_text_rate_input_fields_pct'])
    row('  preflight_checkbox_form', fa['preflight_checkbox_form_pct'], fb['preflight_checkbox_form_pct'])
    row('  coc_checkbox_form', fa['coc_checkbox_form_pct'], fb['coc_checkbox_form_pct'])
    for t in ('textarea', 'input', 'dropdown', 'checkboxes'):
        row(f'  required[{t}]', fa['required_rate_by_field_type_pct'].get(t), fb['required_rate_by_field_type_pct'].get(t))
    pa, pb = a['pr_template'], b['pr_template']
    print('-- PR template --')
    row('  n_pr_templates', pa['n_pr_templates'], pb['n_pr_templates'])
    row('  checklist empty %', pa['checklist_style_pct'].get('empty'), pb['checklist_style_pct'].get('empty'))
    row('  html_comment_guidance %', pa['has_html_comment_guidance_pct'], pb['has_html_comment_guidance_pct'])
    row('  type_of_change_present %', pa['type_of_change_present_pct'], pb['type_of_change_present_pct'])
    row('  toc_checkbox %(of present)', pa['type_of_change_style_pct_among_present'].get('checkbox'),
        pb['type_of_change_style_pct_among_present'].get('checkbox'))
    row('  toc_freetext %(of present)', pa['type_of_change_style_pct_among_present'].get('freetext'),
        pb['type_of_change_style_pct_among_present'].get('freetext'))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'harvest': harvest, 'harvest_wide': harvest_wide, 'harvest_roster': harvest_roster,
     'stats': stats, 'roster': roster, 'compare': compare}.get(cmd, stats)()
