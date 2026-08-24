#!/usr/bin/env python3
"""Issue/PR convention census — deterministic, gh-API.

Population: top-starred manifest-filtered software repos reused from census-expanded (same methodology as
the other censuses). Measures the signals the corpus lacked: PR-title Conventional-Commits adoption,
issue-title style, issue-form (YAML) vs legacy (.md), and PR/issue template shape.

Run from repo root:  python docs/research/census-data/census-issue-pr/census.py harvest | stats
Out: census-issue-pr/records.json (harvest) + census-issue-pr/stats.json (stats).
"""
import json, math, re, subprocess, sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP

ROOT = 'docs/research/census-data'
REC = f'{ROOT}/census-issue-pr/records.json'
OUT = f'{ROOT}/census-issue-pr/stats.json'
N = 500
CC = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?:\s.+')
PREFIX = re.compile(r'^\[[^\]]+\]|^[A-Za-z0-9_-]+:')  # [area] or word: lead


def gh(path):
    try:
        out = subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=60).stdout
        return json.loads(out)
    except Exception:
        return None


def ghraw(path):
    try:
        out = subprocess.run(['gh', 'api', path, '-H', 'Accept: application/vnd.github.raw'],
                             capture_output=True, text=True, timeout=60).stdout
        return out or None
    except Exception:
        return None


def ratio(hits, total):
    return float(Decimal(hits / total).quantize(Decimal('0.01'), ROUND_HALF_UP)) if total else None


def harvest():
    repos = [r['repo'] for r in json.load(open(f'{ROOT}/census-expanded/records.json'))[:N]]
    records = []
    for i, repo in enumerate(repos, 1):
        it = gh(f'repos/{repo}/contents/.github/ISSUE_TEMPLATE')
        forms = md = 0
        config = False
        form_labels, md_headers = [], []
        if isinstance(it, list):
            for f in it:
                n = f.get('name', '')
                if n in ('config.yml', 'config.yaml'):
                    config = True
                elif re.search(r'\.ya?ml$', n):
                    forms += 1
                elif n.endswith('.md'):
                    md += 1
            for f in [x for x in it if re.search(r'\.ya?ml$', x['name']) and not re.match(r'^config\.ya?ml$', x['name'])][:4]:
                raw = ghraw(f"repos/{repo}/contents/{f['path']}")
                if raw:
                    form_labels += [m.group(1).strip(' "\'').lower() for m in re.finditer(r'^\s*label:\s*(.+?)\s*$', raw, re.M)]
            for f in [x for x in it if x['name'].endswith('.md')][:2]:
                raw = ghraw(f"repos/{repo}/contents/{f['path']}")
                if raw:
                    md_headers += [h.strip().lower() for h in re.findall(r'^#{1,4}\s+(.+)$', raw, re.M)]
        pr_raw = (ghraw(f'repos/{repo}/contents/.github/PULL_REQUEST_TEMPLATE.md')
                  or ghraw(f'repos/{repo}/contents/PULL_REQUEST_TEMPLATE.md')
                  or ghraw(f'repos/{repo}/contents/docs/PULL_REQUEST_TEMPLATE.md'))
        pr_headers = [h.strip().lower() for h in re.findall(r'^#{1,4}\s+(.+)$', pr_raw, re.M)] if pr_raw else []
        prs = gh(f'repos/{repo}/pulls?state=all&per_page=30') or []
        pr_titles = [p['title'] for p in prs if p.get('title')]
        iss = [x for x in (gh(f'repos/{repo}/issues?state=all&per_page=30') or []) if not x.get('pull_request')]
        iss_titles = [x['title'] for x in iss if x.get('title')]
        records.append({
            'repo': repo,
            'issue_forms': forms, 'issue_md': md, 'issue_config': config,
            'has_issue_tmpl': forms + md > 0, 'issue_form_labels': form_labels, 'issue_md_headers': md_headers,
            'has_pr_tmpl': bool(pr_raw), 'pr_tmpl_n_headers': len(pr_headers), 'pr_tmpl_headers': pr_headers,
            'pr_tmpl_has_checklist': bool(pr_raw and '- [ ]' in pr_raw),
            'pr_n': len(pr_titles), 'pr_cc': ratio(sum(bool(CC.match(t)) for t in pr_titles), len(pr_titles)),
            'iss_n': len(iss_titles), 'iss_cc': ratio(sum(bool(CC.match(t)) for t in iss_titles), len(iss_titles)),
            'iss_prefix': ratio(sum(bool(PREFIX.match(t)) for t in iss_titles), len(iss_titles)),
            'iss_avg_len': round(sum(len(t) for t in iss_titles) / len(iss_titles)) if iss_titles else None,
        })
        if i % 50 == 0:
            print(f'...{i}/{len(repos)}', file=sys.stderr)
    json.dump(records, open(REC, 'w'))
    print(f'harvested {len(records)} → {REC}', file=sys.stderr)
    stats()


def stats():
    records = json.load(open(REC))
    n = len(records)

    def pct(count):
        return math.floor(100 * count / n + 0.5)  # Math.round parity

    def mean(vals):
        v = [x for x in vals if x is not None]
        return float(Decimal(sum(v) / len(v)).quantize(Decimal('0.01'), ROUND_HALF_UP)) if v else None

    def top(key, k):
        c = Counter(h for r in records for h in (r.get(key) or []))
        return [[name, cnt] for name, cnt in c.most_common(k)]

    pr_data = [r for r in records if r['pr_cc'] is not None]
    out = {
        'n': n,
        'source': 'census-expanded top-500 (manifest-filtered top-starred software)',
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
        'pr_template_top_headers': top('pr_tmpl_headers', 20),
        'issue_form_top_field_labels': top('issue_form_labels', 20),
        'issue_md_top_headers': top('issue_md_headers', 15),
        'repos_with_pr_data': len(pr_data),
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(f'wrote {OUT}', file=sys.stderr)


if __name__ == '__main__':
    (harvest if (len(sys.argv) > 1 and sys.argv[1] == 'harvest') else stats)()
