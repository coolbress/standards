#!/usr/bin/env python3
"""Squash-merge commit-body convention census — default-branch commit messages.

Question: when a repo squash-merges to its default branch, what is the standard for the landed commit's
*body* — does it carry a summary body, issue-closing keywords, a Conventional-Commits subject, co-author
trailers? Population: census-expanded top-N (manifest-filtered top-starred software). GitHub's squash default
appends ' (#N)' to the subject, so subjects ending in '(#N)' are the squash-merge signal.

Run from repo root:  python docs/research/census-data/census-commit-body/census.py harvest | stats
Out: census-commit-body/records.json (harvest) + stats.json (stats).
"""
import json, re, subprocess, sys
from collections import Counter

ROOT = 'docs/research/census-data'
REC = f'{ROOT}/census-commit-body/records.json'
OUT = f'{ROOT}/census-commit-body/stats.json'
N = 250
CC = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?:\s.+')
SQUASH = re.compile(r'\(#\d+\)\s*$')                                  # GitHub squash subject suffix
CLOSES = re.compile(r'(?im)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#\d+')
COAUTHOR = re.compile(r'(?im)^Co-Authored-By:\s')


def gh(path):
    try:
        return json.loads(subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=60).stdout)
    except Exception:
        return None


def harvest():
    repos = [r['repo'] for r in json.load(open(f'{ROOT}/census-expanded/records.json'))[:N]]
    records = []
    for i, repo in enumerate(repos, 1):
        commits = gh(f'repos/{repo}/commits?per_page=30') or []
        squash = []
        for c in commits:
            msg = (c.get('commit') or {}).get('message', '')
            subj = msg.split('\n', 1)[0]
            if SQUASH.search(subj):
                body = msg.split('\n', 1)[1].strip() if '\n' in msg else ''
                squash.append({
                    'cc_subject': bool(CC.match(subj)),
                    'has_body': len(body) > 0,
                    'body_len': len(body),
                    'has_closes': bool(CLOSES.search(msg)),
                    'has_coauthor': bool(COAUTHOR.search(msg)),
                })
        records.append({'repo': repo, 'n_commits': len(commits), 'n_squash': len(squash), 'squash': squash})
        if i % 50 == 0:
            print(f'...{i}/{len(repos)}', file=sys.stderr)
    json.dump(records, open(REC, 'w'))
    print(f'harvested {len(records)} → {REC}', file=sys.stderr)
    stats()


def stats():
    records = json.load(open(REC))
    repos_with_commits = [r for r in records if r['n_commits'] > 0]
    repos_squashing = [r for r in repos_with_commits if r['n_squash'] > 0]
    sq = [s for r in records for s in r['squash']]
    n = len(sq)

    def pct(field):
        return round(100 * sum(1 for s in sq if s[field]) / n) if n else None

    bodied = sorted(s['body_len'] for s in sq if s['has_body'])
    out = {
        'n_repos': len(records),
        'n_repos_with_commit_data': len(repos_with_commits),
        'repos_using_squash_pct': round(100 * len(repos_squashing) / len(repos_with_commits)) if repos_with_commits else None,
        'n_squash_commits_sampled': n,
        'squash_cc_subject_pct': pct('cc_subject'),
        'squash_has_body_pct': pct('has_body'),
        'squash_has_closes_pct': pct('has_closes'),
        'squash_has_coauthor_pct': pct('has_coauthor'),
        'median_body_len_chars': bodied[len(bodied) // 2] if bodied else 0,
    }
    json.dump(out, open(OUT, 'w'), indent=2)
    print(json.dumps(out, indent=2), file=sys.stderr)


if __name__ == '__main__':
    (harvest if (len(sys.argv) > 1 and sys.argv[1] == 'harvest') else stats)()
