---
id: aspect-14-data-management-migrations
title: "Data Management & Migrations"
group: "Q — Quality Attributes"
kind: gated
gated_archetypes: ["backend", "data-ml"]
cross_cutting: false
lifecycle_stages: ["③"]
anchors: ["expand-contract", "Flyway", "Alembic", "PostgreSQL-PITR"]
evidence_track: lit
status: review-needed
last_updated: "2026-06-25"
sources:
  - "https://martinfowler.com/bliki/ParallelChange.html"
  - "https://documentation.red-gate.com/fd/flyway-documentation-138346877.html"
  - "https://alembic.sqlalchemy.org/en/latest/tutorial.html"
  - "https://www.postgresql.org/docs/current/continuous-archiving.html"
claim: "Senior teams evolve persistent schema only through versioned, forward-only, source-controlled migrations applied via the expand-contract pattern for zero downtime, and back it with WAL-based point-in-time recovery against explicit RPO/RTO targets."
maps_from: []
census_todo: "Literature-grounded (gated, net-new): no repo-survey adoption number is cited because schema-migration / PITR posture rarely surfaces as a measurable file in generic repo censuses. If a future survey measures migration-tool or backup/PITR presence per archetype, append to census-data/ and widen here."
---

> **Standard (claim):** Persistent schema evolves only through versioned, forward-only, source-controlled migrations applied via expand-contract for zero downtime, backed by WAL/PITR recovery against explicit RPO/RTO.
> **Evidence:** [lit] (expand-contract, Flyway, Alembic, PostgreSQL PITR) · **Confidence:** High · **Kind:** gated[backend/data-ml] · **Stage:** ③

**Seed sub-aspects** (expand during collection): `schema / data migrations (Flyway/Alembic)` · `zero-downtime / expand-contract` · `data modeling` · `backup / restore + PITR` · `retention / archival` · `multi-tenant data`

## What professional engineers do
<!-- The reference: how senior engineers handle Data Management & Migrations. One pass per seed sub-aspect, evidence-tagged. -->

- **Schema/data migrations as versioned, source-controlled artifacts** [lit]. Every schema change is a numbered, immutable migration file committed alongside application code, applied by a tool that records what ran in a tracking table — Flyway's `flyway_schema_history` or Alembic's `alembic_version` — so any environment converges to the same schema deterministically. Flyway distinguishes *versioned* migrations (`V`-prefix, run once, in order) from *repeatable* migrations (`R`-prefix, re-run when their checksum changes); Alembic chains each revision to a `down_revision` pointer and can *autogenerate* a candidate migration by diffing live SQLAlchemy models against the DB.
- **Forward-only in production** [lit]. Even where tooling offers `downgrade()` (Alembic) or undo scripts, senior teams treat production migrations as forward-only: a bad migration is fixed with a new forward migration, not a rollback, because down-migrations rarely round-trip data losslessly. Migrations are tested in CI against a disposable copy of the schema before they touch prod.
- **Zero-downtime via expand-contract (parallel change)** [lit]. Backward-incompatible schema changes are split into three deploys: **expand** (add the new column/table/index so old *and* new code both work), **migrate** (backfill data and cut clients over incrementally), **contract** (drop the old structure only once nothing reads it). Because the schema is compatible with both the running and the next app version at every step, deploys need no maintenance window and roll back safely. This is the cornerstone of evolutionary database design.
- **Deliberate data modeling** [lit]. Normalize for write-side integrity (foreign keys, constraints, not-null, unique) by default; denormalize only against a measured read path. Treat the schema as a long-lived contract and evolve it only through reviewed, versioned migrations. The former ISO/IEC/IEEE 12207:2017 process-detail attribution was removed because that edition is withdrawn and the licensed ISO/IEC/IEEE 12207:2026 text was not available for clause-level verification.
- **Backup + restore + PITR** [lit]. A backup is not proven until a restore is rehearsed. The production-grade pattern is a periodic **base backup** plus **continuous WAL (write-ahead log) archiving**: replaying WAL on top of a base backup restores the database to *any* point in time (e.g. the instant before an accidental `DROP TABLE`). This sets the achievable **RPO** (data-loss window ≈ time since last archived WAL segment, minutes/seconds with frequent archiving) and **RTO** (restore time ≈ base-backup size + WAL-replay speed). WAL archiving must be enabled *before* the first base backup.
- **Retention & archival** [lit/inferred]. Hot data stays in the primary store; aged data is moved to cheaper tiers or cold archive on an explicit retention policy, and PITR/backup retention windows are set to match recovery and (where applicable) legal/compliance needs rather than left at a tool default.
- **Multi-tenant data isolation** [inferred]. Tenant boundary is a design decision made up front: shared-schema with a tenant-id discriminator (+ row-level security) for density, schema-per-tenant for stronger isolation, or database-per-tenant for the strongest blast-radius containment — each trading isolation against operational and migration cost (a shared schema means one migration fans out to all tenants atomically; database-per-tenant means N migration runs).

## Evidence (lit + census)
<!-- [lit] named papers/standards (cite URL) · [census] repo-survey numbers. Track: lit. -->

- **expand-contract / parallel change** — Fowler, *ParallelChange*: three phases (expand → migrate → contract); "a key component to evolutionary database design," lowering risk by migrating and testing clients incrementally with no coordinated cutover. [lit]
- **Flyway** — Redgate Flyway docs: versioned vs. repeatable migrations, schema-history tracking, "extends DevOps to your databases … from version control to continuous delivery." [lit]
- **Alembic** — SQLAlchemy/Alembic tutorial: revision chain via `down_revision`, `upgrade()`/`downgrade()`, autogenerate by diffing models vs. DB, `alembic_version` tracking table. [lit]
- **PITR** — PostgreSQL *Continuous Archiving and Point-in-Time Recovery*: base backup + WAL replay → restore to any point in time; RPO/RTO governed by archive frequency and replay speed; archiving must precede the first base backup. [lit]
- **[census]** No repo-survey adoption number cited; this aspect is literature-grounded (gated, net-new — rarely surfaced as a measurable file in generic repo censuses).

## Archetype variations
<!-- How this differs across archetypes (gated to: backend, data-ml). -->

This aspect **fires only for the `backend` and `data-ml` archetypes** — i.e. projects that own a persistent datastore. It does not activate for pure-frontend, CLI, or library archetypes.

- **backend** — Full weight: relational schema under Flyway/Alembic-style versioned migrations, expand-contract for every breaking change, PITR-backed backups, tenant-isolation decision. The OLTP store is the system of record; correctness and zero-downtime dominate.
- **data-ml** — Adds dataset/feature versioning and reproducibility concerns: training data and feature tables need lineage and immutable snapshots, not just live schema; "migrations" extend to schema-on-read/lake table formats and backfills of derived features. Backup/PITR still applies to the metadata/feature stores; large object data leans on object-store versioning and retention tiers rather than WAL.

## Tradeoffs / what's ruled out

- **Ruled out: ad-hoc / hand-applied DDL** in production. Untracked `ALTER` statements break environment parity and reproducibility — the schema-history table is non-negotiable.
- **Ruled out: single-deploy breaking schema changes** under load. They require downtime or risk dual-version app failures; expand-contract is the cost paid to avoid a maintenance window.
- **Ruled out: production down-migrations as a rollback strategy** — they rarely restore data losslessly; forward-fix instead.
- **Ruled out: a backup that has never been restored.** Recovery is a tested procedure with measured RTO, not a cron job assumed to work.
- **Tradeoff: expand-contract triples deploy count** for a breaking change (extra latency, more coordination) in exchange for zero downtime and safe rollback — justified for live multi-instance services, overkill for a single-user dev DB.
- **Tradeoff: multi-tenant isolation vs. density** — stronger isolation (db-per-tenant) multiplies migration and ops cost; shared-schema is cheapest to migrate but widest blast radius.

## Sources

- https://martinfowler.com/bliki/ParallelChange.html
- https://documentation.red-gate.com/fd/flyway-documentation-138346877.html
- https://alembic.sqlalchemy.org/en/latest/tutorial.html
- https://www.postgresql.org/docs/current/continuous-archiving.html

## Sub-documents
- [`facts-2026-08-migration-discipline.md`](facts-2026-08-migration-discipline.md) — *research-log (ko)* — 2026-08 facts-only pass (R2-4): 마이그레이션 도구별 rollback/downgrade 규정과 제약(Flyway·Alembic·Prisma·Django) · **expand-contract의 원저자 귀속**(Nygard 2007) 확인.
