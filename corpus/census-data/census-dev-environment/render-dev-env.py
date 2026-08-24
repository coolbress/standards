#!/usr/bin/env python3
"""Render the dev-environment census result JSON -> writeup.md (stats + Unicode bars).

Deterministic: every number comes straight from the census result file, never hand-typed.
Usage: python3 render-dev-env.py <workflow_result.json> <out_dir>
The workflow result file is the wf_*.json under .../workflows/ ; we read its .result object.
"""
import json
import sys
from pathlib import Path

# 35 component flags -> the 8 포석 topics (writeup organization). Some flags cross-reference
# (lockfile/dep_bot touch supply-chain too) — noted in prose, counted once under their home topic.
TOPICS = [
    ("1. Dev environment & toolchain", ["manifest", "runtime_pin", "pkg_manager_pin", "lockfile", "build_config"]),
    ("2. Code-quality gates", ["linter", "formatter", "typechecker", "editorconfig", "precommit_hooks"]),
    ("3. Testing", ["test_framework", "coverage_config"]),
    ("4. VCS & collaboration", ["gitignore", "gitattributes", "commit_convention", "codeowners", "issue_template", "pr_template"]),
    ("5. CI/CD & automation", ["ci", "pr_title_check", "dep_bot", "release_automation"]),
    ("6. Dependencies & supply-chain", ["supply_chain_security"]),
    ("7. Documentation & governance", ["readme", "license", "contributing", "security_md", "code_of_conduct", "changelog", "docs_dir"]),
    ("8. Reproducible onboarding", ["devcontainer", "dockerfile", "env_example", "task_runner", "editor_recommendations"]),
]

# Components the census measures as archetype-conditional (spread across archetypes is the signal).
CONDITIONAL = ["build_config", "release_automation", "devcontainer", "dockerfile", "env_example",
               "coverage_config", "precommit_hooks", "contributing", "security_md", "code_of_conduct",
               "docs_dir", "editor_recommendations", "gitattributes", "codeowners", "issue_template", "pr_template"]


def bar(pct, width=30):
    filled = round((pct / 100) * width)
    return "█" * filled + "·" * (width - filled)


def tier(pct):
    # Data-derived tier (NOT an a-priori assertion): high adoption => universal-core candidate.
    if pct >= 80:
        return "🟩 core"
    if pct >= 50:
        return "🟨 common"
    return "🟦 cond."


def main():
    res_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = json.loads(res_path.read_text())
    r = raw.get("result", raw)  # accept either the wf wrapper or a bare result

    software = r.get("software", 0)
    non_sw = r.get("nonSoftware", 0)
    inspected = r.get("inspected", 0)
    adopt = r.get("adoptionPctOverall", {}) or {}
    arch_dist = r.get("archetypeDistribution", {}) or {}
    tools = r.get("toolWinners", {}) or {}
    cond = r.get("conditionalByArchetype", {}) or {}

    # Persist raw data alongside the writeup.
    (out_dir / "data.json").write_text(json.dumps(r, indent=2, ensure_ascii=False))

    L = []
    L.append("# 포석 Topic 01 — Development environment & toolchain (census results)\n")
    L.append("> **Auto-generated** from the top-starred-repo census by `render-dev-env.py` — every number is\n"
             "> straight from `data.json` (no hand-transcription). Method + evidence tags: see `00-project-lifecycle.md` §7.\n"
             "> All figures here are `[census]` (current-state file presence) unless tagged otherwise.\n")
    L.append(f"\n**Sample:** {software} software repos analysed "
             f"({non_sw} non-software dropped, {inspected} inspected total). n = {software}.\n")

    # Archetype distribution
    L.append("\n## Archetype distribution `[census]`\n")
    total_arch = sum(arch_dist.values()) or 1
    for a, c in sorted(arch_dist.items(), key=lambda kv: -kv[1]):
        pct = round(c / total_arch * 100)
        L.append(f"- `{a:<16}` {bar(pct)} {pct:>3}%  (n={c})")

    # Adoption by topic
    L.append("\n\n## Adoption % by 포석 topic `[census]`\n")
    L.append("Tier is **data-derived** (≥80% 🟩 core · 50–79% 🟨 common · <50% 🟦 conditional), not asserted.\n")
    for title, keys in TOPICS:
        L.append(f"\n### {title}\n")
        rows = sorted(((k, adopt.get(k, 0)) for k in keys), key=lambda kv: -kv[1])
        for k, pct in rows:
            L.append(f"- `{k:<20}` {bar(pct)} {pct:>3}%  {tier(pct)}")

    # Tool winners
    L.append("\n\n## Tool winners (among repos that have the tool) `[census]`\n")
    for field, counts in tools.items():
        if not counts:
            continue
        ranked = sorted(counts.items(), key=lambda kv: -kv[1])
        line = " · ".join(f"{t} ({n})" for t, n in ranked)
        L.append(f"- **{field}**: {line}")

    # Conditional spread by archetype — proves the 🟩/🟦 split with variance.
    L.append("\n\n## Archetype-conditional spread `[census]`\n")
    L.append("For each conditional component, adoption per archetype (sorted). **Wide spread = genuinely\n"
             "archetype-conditional; flat-high = actually universal-core regardless of type.**\n")
    archetypes = [a for a in cond.keys()]
    for comp in CONDITIONAL:
        pairs = []
        for a in archetypes:
            row = cond.get(a, {})
            if row.get("count", 0) >= 3:  # ignore tiny archetype samples
                pairs.append((a, row.get(comp, 0)))
        if not pairs:
            continue
        pairs.sort(key=lambda kv: -kv[1])
        spread = (pairs[0][1] - pairs[-1][1]) if len(pairs) > 1 else 0
        cells = " | ".join(f"{a} {p}%" for a, p in pairs)
        flag = "⟵ wide" if spread >= 40 else ("⟵ flat" if spread <= 15 else "")
        L.append(f"- `{comp:<20}` {cells}  {flag}")

    L.append("\n\n## Reading notes\n")
    L.append("- `[census]` = file-presence in current `HEAD` tree; does **not** measure config quality/depth\n"
             "  (that's `[lit]` — see `02-foundation-standard.md` §6) nor non-file foundation (branch protection, required\n"
             "  checks, secret-scanning toggles live in repo *settings*, invisible to the tree).\n")
    L.append("- Accretion caveat: these are mature repos' *current* state. The born-vs-accreted split needs\n"
             "  the initial-commit + young-cohort passes (`[census-init]` / `[census-young]`), not yet run.\n")

    out = out_dir / "writeup.md"
    out.write_text("\n".join(L) + "\n")
    print(f"wrote {out} ({software} software repos) + {out_dir/'data.json'}")


if __name__ == "__main__":
    main()
