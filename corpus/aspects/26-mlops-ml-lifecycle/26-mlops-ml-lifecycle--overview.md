---
id: aspect-26-mlops-ml-lifecycle
title: "MLOps / ML Lifecycle"
group: "S — Specialized Archetype"
kind: gated
gated_archetypes: ["data-ml"]
cross_cutting: false
lifecycle_stages: ["all"]
anchors: ["ml-ops.org-Stack-Canvas", "MLOps-literature"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://ml-ops.org/content/mlops-principles"
  - "https://ml-ops.org/content/mlops-stack-canvas"
  - "https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning"
  - "https://research.google/pubs/pub46555/"
  - "https://artificialintelligenceact.eu/high-level-summary/"
claim: "Production ML treats data, code, and models as co-versioned first-class artifacts driven through automated CI/CD/CT pipelines with a metadata/registry backbone, ML-specific testing, and live drift monitoring that triggers retraining — escalating to data-governance, logging, and human-oversight controls when the system is regulated high-risk."
census_todo: "Literature-grounded aspect (lit-track); MLOps tooling is rare in general repo censuses. No real census % available — do NOT fabricate. If a data-ml-archetype repo survey is later run, widen census for DVC/MLflow/Feast/registry adoption."
maps_from: []
---

> **Standard (claim):** Production ML treats data, code, and models as co-versioned first-class artifacts driven through automated CI/CD/CT pipelines with a metadata/registry backbone, ML-specific testing, and live drift monitoring that triggers retraining — escalating to data-governance, logging, and human-oversight controls when the system is regulated high-risk.
> **Evidence:** [lit] (5 anchors) · **Confidence:** high (anchors) · **Kind:** gated[data-ml] · **Stage:** all

**Seed sub-aspects:** `data versioning (DVC / Delta)` · `experiment tracking (MLflow / W&B)` · `feature store (Feast)` · `model registry / governance` · `training orchestration (Kubeflow/Airflow)` · `serving (vLLM/TorchServe)` · `drift monitoring` · `ML security`

## What professional engineers do

- **Data versioning [lit].** Treat datasets as first-class DevOps citizens — version raw data, feature transforms, and snapshots so any training run is reproducible (ml-ops.org *Versioning* principle: ML scripts, models, and datasets are all tracked). Tooling: DVC / Delta Lake / lakeFS pinning data to a content hash referenced from the training pipeline.
- **Experiment tracking [lit].** Every run records params, code commit, dataset hash, metrics, and artifacts into a **metadata store** that "spans all previous elements" of the stack for reproducibility and governance (ml-ops.org Stack Canvas block 11). Tooling: MLflow Tracking / Weights & Biases. Reproducibility principle: identical input → identical result across data-prep, training, and deployment.
- **Feature store [lit].** A shared layer transforms raw data into feature vectors with consistent online/offline definitions, killing training/serving skew (Stack Canvas block 4 "Feature Store and Workflows"; Google pipeline component "feature store — standardized feature management"). Tooling: Feast / Tecton.
- **Model registry & governance [lit].** Trained models are versioned, staged (dev→staging→prod), and gated as essential assets (Stack Canvas block 7 "Model Registry and Versioning"; Google "model registry — trained model storage"). Registry holds lineage back to data + code + metrics; promotion is a governed transition, not a file copy.
- **Training orchestration / CI/CD/CT [lit].** Three maturity levels: **L0** manual notebooks, **L1** orchestrated pipeline with **Continuous Training** (auto-retrain on fresh data via triggers), **L2** CI/CD pipeline automation that builds/tests/deploys the *pipeline itself* (Google MLOps maturity model). **CT is the ML-unique third leg** beyond CI/CD: the model is retrained in production on live triggers (schedule, new data, performance decay, distribution shift). Tooling: Kubeflow Pipelines / Airflow / Vertex.
- **Serving [lit].** Models are containerized and exposed via REST (or batch vs. online prediction modes) to cloud/on-prem/edge using standard DevOps deploy practices (ml-ops.org *Deployment*; Stack Canvas blocks 8–9 deployment + prediction serving). Tooling: TorchServe / vLLM (LLM) / KServe / Triton.
- **Drift / decay monitoring [lit].** Monitor schema compliance, data/prediction distribution, and "model decay," measuring predictive quality on live data to **trigger retraining** (ml-ops.org *Monitoring*; Google triggers: performance degradation + concept-drift). Closes the CT loop.
- **ML-specific testing & security [lit].** Beyond unit tests, validate **features & data, model development, ML infrastructure, and monitoring** — the four categories of the Google **ML Test Score** (28 tests, Breck et al. 2017), a production-readiness + technical-debt rubric. Data/model validation in-pipeline detects schema and value skew before promotion.

## Evidence (lit + census)

- **[lit]** ml-ops.org **MLOps Principles** — Versioning (data/code/model as first-class), Testing (data, model, infra), Automation (3 levels incl. CI/CD), Reproducibility (identical input→output), Deployment (containerized/REST/edge), Monitoring (dependency + schema + model decay → retrain). https://ml-ops.org/content/mlops-principles
- **[lit]** ml-ops.org **MLOps Stack Canvas** — 11 building blocks incl. data sources & versioning, feature store, CI/CT/CD, model registry & versioning, deployment, prediction serving, monitoring, and a metadata store spanning all. https://ml-ops.org/content/mlops-stack-canvas
- **[lit]** Google Cloud **MLOps: CD & automation pipelines** — maturity L0/L1/L2; **Continuous Training (CT)** as the ML-specific addition to CI/CD; pipeline components = data+model validation, feature store, ML metadata store, model registry; triggers = on-demand/scheduled/new-data/decay/drift. https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- **[lit]** Breck et al. (2017) **The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction** — 28 tests across features/data, model development, infrastructure, monitoring. https://research.google/pubs/pub46555/
- **[lit]** **EU AI Act** (high-risk, Ch. III Art. 8–17) — data governance (representative, error-free datasets), automatic event logging/record-keeping over the lifecycle, technical documentation, human oversight, accuracy/robustness/cybersecurity, risk-management + post-market monitoring. https://artificialintelligenceact.eu/high-level-summary/
- **[census]** None. Literature-grounded; MLOps tooling rarely surfaces in general OSS censuses (see `census_todo`).

## Archetype variations

- **GATED → activates ONLY for `data-ml`.** This aspect fires when the project trains, serves, or continuously retrains models. The full stack (data versioning → experiment tracking → feature store → registry → CT pipeline → serving → drift monitoring) is the `data-ml` baseline.
- **Within `data-ml`, depth scales with maturity:** an offline/research model needs versioning + experiment tracking + reproducibility but can skip CT and a feature store; a production online-serving system needs the full L1/L2 pipeline, registry promotion gates, and live drift monitoring.
- **Regulated `data-ml` (high-risk under EU AI Act):** adds mandatory data-governance evidence, immutable event logging, technical documentation, human-oversight hooks, and post-market monitoring on top of the engineering baseline — these become acceptance gates, not nice-to-haves.
- **Non-`data-ml` archetypes (web, mobile, cli, ai-harness, library):** this aspect does **not** fire. A project that merely *calls* a hosted LLM API is application code, not an ML lifecycle — it falls under API-integration/observability aspects, not MLOps.

## Tradeoffs / what's ruled out

- **Full MLOps stack vs. project stage.** A feature store, CT loop, and L2 CI/CD are heavy infrastructure; standing them up for a one-off model or a pre-PMF prototype is over-engineering. Rule: start at L0 with reproducibility + experiment tracking, climb to L1/L2 only when retraining cadence or serving SLAs demand it.
- **CT auto-retrain vs. governance.** Continuous Training maximizes freshness but un-gated auto-promotion risks shipping a regressed or drifted model. Ruled out: retrain-and-deploy with no validation gate — CT must route through data/model validation + registry promotion, and in regulated contexts through human oversight.
- **Build vs. buy.** Each Stack Canvas block is a tool decision; ruled out is hand-rolling versioning/registry/tracking when DVC/MLflow/Feast cover it — reinventing the metadata backbone is the classic ML technical-debt trap (Breck et al.).
- **Not in scope here:** general data-pipeline/ETL engineering, model *architecture* selection, and generic LLM-app prompt engineering — those are separate aspects; this aspect is the *operational lifecycle* around a trained model.

## Sources

- https://ml-ops.org/content/mlops-principles
- https://ml-ops.org/content/mlops-stack-canvas
- https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- https://research.google/pubs/pub46555/
- https://artificialintelligenceact.eu/high-level-summary/
