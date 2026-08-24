#!/usr/bin/env python3
"""Offline uncertainty and sensitivity checks for the writing-conventions census."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUTS = {
    "senior": HERE / "conventions-records.json",
    "wide": HERE / "conventions-6k-records.json",
}
OUTPUT = HERE / "robustness.json"
REPORT = HERE / "robustness-report.md"
BOOTSTRAPS = 2000
SEED = 20260711


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> list[float] | None:
    if not n:
        return None
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(100 * (centre - spread), 2), round(100 * (centre + spread), 2)]


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - pos) + values[hi] * (pos - lo)


def repo_metric(record: dict, metric: str) -> tuple[int, int]:
    forms = record.get("forms") or []
    pr = record.get("pr")
    if metric == "form_help_text":
        fields = [field for form in forms for field in form.get("fields", [])
                  if field.get("type") in {"textarea", "input", "dropdown", "checkboxes"}]
        return sum(bool(f.get("has_description") or f.get("has_placeholder")) for f in fields), len(fields)
    if metric == "form_preflight":
        return sum(bool(form.get("has_preflight")) for form in forms), len(forms)
    if metric == "pr_empty_checklist":
        return (int(pr.get("checklist_style") == "empty"), 1) if pr else (0, 0)
    if metric == "pr_html_guidance":
        return (int(pr.get("html_comment_count", 0) > 0), 1) if pr else (0, 0)
    if metric == "pr_type_of_change":
        return (int(bool(pr.get("type_of_change_present"))), 1) if pr else (0, 0)
    raise ValueError(metric)


def point(records: list[dict], metric: str) -> tuple[int, int, float | None]:
    pairs = [repo_metric(record, metric) for record in records]
    yes, n = sum(x for x, _ in pairs), sum(y for _, y in pairs)
    return yes, n, round(100 * yes / n, 2) if n else None


def cluster_bootstrap(records: list[dict], metric: str) -> list[float] | None:
    clusters: dict[str, list[dict]] = {}
    for record in records:
        owner = record["repo"].split("/", 1)[0].casefold()
        clusters.setdefault(owner, []).append(record)
    owners = sorted(clusters)
    pairs = {owner: tuple(sum(values) for values in zip(*(repo_metric(record, metric)
                                                         for record in group)))
             for owner, group in clusters.items()}
    rng = random.Random(f"{SEED}:{metric}:{len(records)}")
    values = []
    for _ in range(BOOTSTRAPS):
        sampled = [pairs[rng.choice(owners)] for _ in owners]
        yes, n = sum(x for x, _ in sampled), sum(y for _, y in sampled)
        pct = round(100 * yes / n, 2) if n else None
        if n:
            values.append(pct)
    if not values:
        return None
    return [round(percentile(values, 0.025), 2), round(percentile(values, 0.975), 2)]


def owner_equal(records: list[dict], metric: str) -> float | None:
    clusters: dict[str, list[dict]] = {}
    for record in records:
        clusters.setdefault(record["repo"].split("/", 1)[0].casefold(), []).append(record)
    owner_rates = []
    for group in clusters.values():
        _, n, pct = point(group, metric)
        if n:
            owner_rates.append(pct)
    return round(statistics.mean(owner_rates), 2) if owner_rates else None


def star_quartiles(records: list[dict], metric: str) -> list[dict]:
    ranked = sorted((r for r in records if isinstance(r.get("stars"), (int, float))), key=lambda r: r["stars"])
    rows = []
    for i in range(4):
        lo = len(ranked) * i // 4
        hi = len(ranked) * (i + 1) // 4
        group = ranked[lo:hi]
        yes, n, pct = point(group, metric)
        rows.append({
            "quartile": i + 1,
            "repo_n": len(group),
            "star_range": [group[0]["stars"], group[-1]["stars"]] if group else None,
            "successes": yes,
            "observations": n,
            "pct": pct,
        })
    return rows


def analyze(label: str, path: Path) -> dict:
    records = json.loads(path.read_text(encoding="utf-8"))
    metrics = {}
    for metric in ("form_help_text", "form_preflight", "pr_empty_checklist", "pr_html_guidance", "pr_type_of_change"):
        yes, n, pct = point(records, metric)
        equal = owner_equal(records, metric)
        metrics[metric] = {
            "unit": "input-like field" if metric == "form_help_text" else "form" if metric == "form_preflight" else "PR template",
            "successes": yes,
            "observations": n,
            "pct": pct,
            "wilson_95_pct": wilson(yes, n),
            "owner_cluster_bootstrap_95_pct": cluster_bootstrap(records, metric),
            "owner_equal_pct": equal,
            "owner_equal_minus_pooled_pp": round(equal - pct, 2) if equal is not None and pct is not None else None,
            "by_star_quartile": star_quartiles(records, metric),
        }
    owners = {r["repo"].split("/", 1)[0].casefold() for r in records}
    return {
        "input": path.name,
        "input_sha256": digest(path),
        "repo_n": len(records),
        "owner_cluster_n": len(owners),
        "metrics": metrics,
    }


def render(data: dict) -> str:
    names = {
        "form_help_text": "Help text on input-like issue-form fields",
        "form_preflight": "Preflight checkbox on issue forms",
        "pr_empty_checklist": "Empty checklist in PR templates",
        "pr_html_guidance": "HTML-comment guidance in PR templates",
        "pr_type_of_change": "Type-of-change section in PR templates",
    }
    lines = [
        "# Issue/PR conventions — uncertainty and sensitivity",
        "",
        "This report is derived entirely from the preserved normalized records. It adds uncertainty and",
        "sensitivity checks; it does not turn adoption frequency into a normative requirement.",
        "",
        "## Main estimates",
        "",
        "| Cohort | Metric | Estimate | Wilson 95% | Owner-cluster bootstrap 95% | Owner-equal delta |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for cohort, payload in data["cohorts"].items():
        for metric, row in payload["metrics"].items():
            w = row["wilson_95_pct"]
            b = row["owner_cluster_bootstrap_95_pct"]
            lines.append(
                f"| {cohort} | {names[metric]} | {row['pct']:.2f}% "
                f"| {w[0]:.2f}–{w[1]:.2f}% | {b[0]:.2f}–{b[1]:.2f}% "
                f"| {row['owner_equal_minus_pooled_pp']:+.2f} pp |"
            )
    lines += [
        "",
        "## Interpretation limits",
        "",
        "- Wilson intervals treat the stated observation unit as independent; the owner-cluster bootstrap is the preferred sensitivity check for shared ownership.",
        "- Issue-form field/form observations can still be correlated within a repository. The owner bootstrap resamples owner clusters and keeps all repositories and observations inside each sampled owner.",
        "- Star quartiles in `robustness.json` are descriptive strata, not causal estimates. The senior cohort is nested in the wide census, so their difference is not an independent replication test.",
        "- Neither preserved conventions dataset contains `createdAt`; recency weighting cannot be reconstructed honestly. These estimates are unweighted snapshots.",
        "- Selection remains conditional on repositories that publish issue forms or PR templates. It must not be read as prevalence across all GitHub repositories.",
        "- Census frequencies are evidence about exposed conventions, not a mandate. Literature, project context, and adequacy review remain separate decision axes.",
        "",
    ]
    return "\n".join(lines)


def build() -> dict:
    return {
        "schema_version": 1,
        "method": {
            "confidence_interval": "Wilson score, 95%, unweighted",
            "cluster_sensitivity": f"deterministic owner-cluster bootstrap, {BOOTSTRAPS} replicates, seed {SEED}",
            "stratification": "within-cohort star-count quartiles",
            "recency_weighting": "not applied: createdAt absent from preserved records",
        },
        "cohorts": {label: analyze(label, path) for label, path in INPUTS.items()},
    }


def verify(data: dict) -> None:
    actual = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if actual != data:
        raise SystemExit("robustness validation failed: output differs from deterministic recomputation")
    if REPORT.read_text(encoding="utf-8") != render(data):
        raise SystemExit("robustness validation failed: report differs from deterministic rendering")
    mappings = {
        "form_help_text": ("issue_form", "help_text_rate_input_fields_pct"),
        "form_preflight": ("issue_form", "preflight_checkbox_form_pct"),
        "pr_html_guidance": ("pr_template", "has_html_comment_guidance_pct"),
        "pr_type_of_change": ("pr_template", "type_of_change_present_pct"),
    }
    for cohort, suffix in (("senior", "conventions-stats.json"), ("wide", "conventions-6k-stats.json")):
        published = json.loads((HERE / suffix).read_text(encoding="utf-8"))
        for metric, keys in mappings.items():
            expected = published[keys[0]][keys[1]]
            observed = round(data["cohorts"][cohort]["metrics"][metric]["pct"], 1)
            if observed != expected:
                raise SystemExit(f"robustness validation failed: {cohort}/{metric} {observed} != {expected}")
    print("robustness validation passed: deterministic outputs and published headline estimates agree")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", choices=("build", "validate"), default="build")
    args = parser.parse_args()
    data = build()
    if args.command == "validate":
        verify(data)
        return
    OUTPUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"wrote {OUTPUT} and {REPORT}")


if __name__ == "__main__":
    main()
