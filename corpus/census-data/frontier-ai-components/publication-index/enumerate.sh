#!/usr/bin/env bash
# enumerate.sh — DETERMINISTIC publication-surface harvest (Phase C of the coverage census).
#
# Purpose: mechanically enumerate the Anthropic + OpenAI (+ MCP / CC docs / OpenAI dev docs)
# research/engineering/news/index/doc surfaces via XML sitemaps + the arXiv API, closing the
# Phase-A residual ("the human /research and /news index pages are JS-rendered, so Phase A
# enumerated them by topic-search and could not PROVE no paper was missed"). Sitemaps + arXiv
# are XML — they render without JS, so this is a deterministic, reproducible backdoor.
#
# Run date of the captured snapshot: 2026-06-27.
#
# NOTE on this environment: in the sandbox that produced the committed sitemap-*.txt snapshots,
# `curl` was permission-blocked, so the captures were taken via the agent's WebFetch tool on the
# raw .xml URLs (still deterministic — it parses the XML <loc> set, not JS-rendered prose). This
# script is the reproducible curl/xmllint equivalent: run it anywhere curl is available to
# regenerate the same raw lists. Re-run and diff against the committed snapshots to refresh.
#
# Deps: curl, xmllint (libxml2). Usage: ./enumerate.sh [outdir]   (default outdir = script dir)

set -euo pipefail
OUTDIR="${1:-$(cd "$(dirname "$0")" && pwd)}"
UA='gingoa-census/1.0 (publication-index Phase C; sitemap enumeration)'
fetch() { curl -fsSL --compressed -A "$UA" --max-time 60 "$1"; }

# Extract every <loc> URL from a sitemap or sitemap-index on stdin.
locs() { xmllint --xpath '//*[local-name()="loc"]/text()' - 2>/dev/null | tr ' ' '\n' | sed '/^$/d'; }

# ---- Anthropic: single flat sitemap (NOT an index) → bucket by path ----
echo "[*] anthropic.com/sitemap.xml"
fetch 'https://www.anthropic.com/sitemap.xml' | locs | sort -u > "$OUTDIR/sitemap-anthropic.txt"

# ---- OpenAI: sitemap.xml is an INDEX → fetch each child, union the page URLs ----
echo "[*] openai.com/sitemap.xml (index → children)"
{
  fetch 'https://openai.com/sitemap.xml' | locs | while read -r child; do
    fetch "$child" | locs || true
  done
} | sort -u > "$OUTDIR/sitemap-openai.txt"

# ---- OpenAI developer docs (separate host; robots → /sitemap-index.xml → /sitemap-0.xml) ----
echo "[*] developers.openai.com"
fetch 'https://developers.openai.com/sitemap-index.xml' | locs | while read -r child; do
  fetch "$child" | locs || true
done | sort -u > "$OUTDIR/sitemap-openai-devdocs.txt"

# ---- Claude Code docs + Anthropic platform docs + MCP (doc/changelog surfaces) ----
echo "[*] code.claude.com / platform.claude.com / modelcontextprotocol.io"
fetch 'https://code.claude.com/sitemap.xml'        | locs | grep '/docs/en/' | sort -u > "$OUTDIR/sitemap-codeclaude-en.txt"
fetch 'https://platform.claude.com/sitemap.xml'    | locs | grep '/docs/en/' | sort -u > "$OUTDIR/sitemap-platformclaude-en.txt"  # docs.claude.com 301→platform.claude.com
fetch 'https://modelcontextprotocol.io/sitemap.xml'| locs                    | sort -u > "$OUTDIR/sitemap-mcp.txt"

# ---- arXiv backstop (papers axis): NOISY (affiliation isn't reliable metadata) ----
echo "[*] arXiv API (Anthropic / OpenAI)"
fetch 'http://export.arxiv.org/api/query?search_query=all:Anthropic&max_results=100&sortBy=submittedDate&sortOrder=descending' \
  | xmllint --xpath '//*[local-name()="entry"]/*[local-name()="title"]/text()' - 2>/dev/null > "$OUTDIR/arxiv-anthropic.txt" || true
fetch 'http://export.arxiv.org/api/query?search_query=all:OpenAI&max_results=100&sortBy=submittedDate&sortOrder=descending' \
  | xmllint --xpath '//*[local-name()="entry"]/*[local-name()="title"]/text()' - 2>/dev/null > "$OUTDIR/arxiv-openai.txt" || true

echo "[done] raw lists written to $OUTDIR"
