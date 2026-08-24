# Issue/PR conventions — uncertainty and sensitivity

This report is derived entirely from the preserved normalized records. It adds uncertainty and
sensitivity checks; it does not turn adoption frequency into a normative requirement.

## Main estimates

| Cohort | Metric | Estimate | Wilson 95% | Owner-cluster bootstrap 95% | Owner-equal delta |
|---|---|---:|---:|---:|---:|
| senior | Help text on input-like issue-form fields | 87.12% | 86.40–87.81% | 85.52–88.68% | -0.60 pp |
| senior | Preflight checkbox on issue forms | 22.36% | 20.39–24.46% | 18.75–25.81% | +1.69 pp |
| senior | Empty checklist in PR templates | 62.03% | 57.71–66.16% | 57.66–66.48% | +0.99 pp |
| senior | HTML-comment guidance in PR templates | 69.78% | 65.63–73.63% | 65.66–73.99% | -0.72 pp |
| senior | Type-of-change section in PR templates | 11.53% | 9.03–14.62% | 8.82–14.32% | +0.61 pp |
| wide | Help text on input-like issue-form fields | 87.20% | 86.70–87.68% | 86.09–88.31% | -0.20 pp |
| wide | Preflight checkbox on issue forms | 22.29% | 20.89–23.75% | 19.97–24.71% | +1.20 pp |
| wide | Empty checklist in PR templates | 63.23% | 60.31–66.06% | 59.57–66.54% | +1.19 pp |
| wide | HTML-comment guidance in PR templates | 63.79% | 60.87–66.60% | 60.47–66.89% | -0.85 pp |
| wide | Type-of-change section in PR templates | 11.88% | 10.09–13.95% | 9.88–13.90% | +1.08 pp |

## Interpretation limits

- Wilson intervals treat the stated observation unit as independent; the owner-cluster bootstrap is the preferred sensitivity check for shared ownership.
- Issue-form field/form observations can still be correlated within a repository. The owner bootstrap resamples owner clusters and keeps all repositories and observations inside each sampled owner.
- Star quartiles in `robustness.json` are descriptive strata, not causal estimates. The senior cohort is nested in the wide census, so their difference is not an independent replication test.
- Neither preserved conventions dataset contains `createdAt`; recency weighting cannot be reconstructed honestly. These estimates are unweighted snapshots.
- Selection remains conditional on repositories that publish issue forms or PR templates. It must not be read as prevalence across all GitHub repositories.
- Census frequencies are evidence about exposed conventions, not a mandate. Literature, project context, and adequacy review remain separate decision axes.
