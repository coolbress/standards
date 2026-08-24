---
id: aspect-14-data-management-migrations--facts-2026-08-migration-discipline
title: "마이그레이션 규율과 무중단 스키마 변경 — facts (2026-08)"
parent: aspect-14-data-management-migrations
kind: research-log
evidence_track: lit
status: draft
language: ko
last_updated: "2026-08-05"
review_due: "2026-11-05"
method: "Haiku web-research, facts-only, EVIDENCE-POLICY conformant; search log included"
---

## 조사 기록

**질문 범위**: 마이그레이션 도구의 공식 문서가 규정하는 rollback/downgrade 지원 및 제약; expand-contract 패턴의 원저자 및 공식 규정.

**제외**: 법률 해석, 도구 추천, 설계 결정.

**조사일**: 2026-08-05

**예산 사용**:
- Q1 마이그레이션 도구: 검색 4/6 (Flyway, Alembic, Prisma, Django), fetch 4/8
- Q2 expand-contract 패턴: 검색 2/6, fetch 2/8
- **총 검색**: 6/12, **총 fetch**: 6/16

---

## Q1: 마이그레이션 도구의 rollback/downgrade 규정

### Q1a: Flyway

**[정의]** Flyway는 undo migration을 지원한다 ([1차: Redgate 공식 문서](https://documentation.red-gate.com/fd/undo-migrations-273973334.html)).

**[규정]** Undo 마이그레이션은 U{버전}__ 형식으로 명명되며, `undo` 명령을 통해 실행된다. 이는 Flyway Teams 에디션에서 제공된다 ([1차: Redgate FAQ](https://documentation.red-gate.com/fd/frequently-asked-questions-277579363.html)).

**[제약]**:
1. **데이터 변경 제약**: Undo migration은 "스키마 변경은 취소할 수 있지만 데이터 변경 취소는 어렵다" ([1차: https://documentation.red-gate.com/fd/undo-migrations-273973334.html]).
2. **파괴적 변경 경고**: DROP, DELETE, TRUNCATE 같은 파괴적 작업이 포함된 마이그레이션의 경우, "테이블과 데이터를 모두 복구하는 undo 스크립트를 작성하기 어려울 수 있다" ([1차: https://documentation.red-gate.com/fd/undo-migrations-273973334.html]).
3. **DDL 트랜잭션 의존성**: "Undo migration은 전체 마이그레이션이 성공했다고 가정한다. DDL 트랜잭션을 지원하지 않는 데이터베이스에서 마이그레이션이 중간에 실패하면 undo 스크립트가 도움이 되지 않는다" ([1차: https://documentation.red-gate.com/fd/undo-migrations-273973334.html]).

**[프로덕션 권고]**:
- "적절히 검사된 백업 및 복원 전략" (규범: 권고)
- "대용량 데이터의 경우 기본 스토리지 솔루션의 스냅샷 기술 사용" (규범: 권고)
- "프로덕션에서 배포된 모든 버전의 코드와 데이터베이스 간 하위 호환성 유지" (규범: 권고)

---

### Q1b: Alembic

**[규정]** Alembic은 `alembic downgrade` 명령을 지원한다. 마이그레이션 파일의 `upgrade()` 및 `downgrade()` 함수는 각각 업그레이드와 다운그레이드 로직을 정의한다 ([1차: https://alembic.sqlalchemy.org/en/latest/api/commands.html]).

**[명령]**: 
- `alembic downgrade -1`: 가장 최근 마이그레이션 제거
- `alembic downgrade <revision>`: 특정 버전으로 되돌리기

**[제약]**: 공식 API 참고 문서에는 downgrade 명령에 대한 명시적 제약이나 경고가 기록되지 않음 ([미확인]: 본문 미확인, 더 상세한 문서 필요).

---

### Q1c: Prisma Migrate

**[규정]** Prisma는 down migration을 지원한다. `prisma migrate diff` 명령으로 down migration SQL 파일을 생성할 수 있으며, `db execute` 명령으로 프로덕션에 적용할 수 있다 ([1차: https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations]).

**[롤백 메커니즘]**: 실패한 마이그레이션을 "rolled back"으로 표시하려면 `prisma migrate resolve --rolled-back "<migration-id>"` 명령을 사용한다 ([미확인]: 검색 결과만 확인, 공식 문서 원문 미확인).

**[제약]**:
1. **데이터베이스 제한**: Down migration은 관계형 데이터베이스에만 적용된다. MongoDB는 지원하지 않는다 ([1차: https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations]).
2. **데이터 비복구성**: "Down migration은 스키마만 되돌린다. 업 마이그레이션 중에 수행한 데이터 변경은 되돌려지지 않는다" ([1차: https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations]).
3. **성공한 마이그레이션 미지원**: Down migration은 실패한 마이그레이션에만 사용할 수 있다. 성공한 마이그레이션을 되돌리려면 스키마 파일을 수정하고 새 마이그레이션을 생성해야 한다 ([1차: https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations]).

**[프로덕션 위치]**: Down migration은 "실패한 배포를 처리하기 위한 도구"로 위치지어진다. 즉시 발동 도구가 아니라 응급 복구 수단이다 ([1차: https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations]).

---

### Q1d: Django

**[규정]** Django는 `manage.py migrate <app> <target-migration>` 명령으로 특정 마이그레이션으로 되돌릴 수 있다. 모든 마이그레이션을 제거하려면 `manage.py migrate <app> zero`를 사용한다 ([1차: https://docs.djangoproject.com/en/6.0/topics/migrations/]).

**[역전 불가능 정의]**: "마이그레이션이 역전 불가능한 작업(IrreversibleError)을 포함하면 되돌릴 수 없다." 파괴적 작업(DROP TABLE 등)이 명시적 역전 로직 없이 포함되면 `IrreversibleError`가 발생한다 ([1차: https://docs.djangoproject.com/en/6.0/topics/migrations/]).

**[제약]**:
1. **작업 역전성**: 일부 작업은 본질적으로 역전 가능하지 않다:
   - `RunSQL` 또는 `RunPython`을 사용한 파괴적 작업은 명시적 역전 로직이 없으면 역전 불가능
   - `CreateModel`, `AddField` 같은 작업은 역전 가능
   - `DropTable` 같은 작업은 기본적으로 역전 불가능

2. **RunPython 역전 로직**: `RunPython` 마이그레이션이 역전 가능하려면 두 번째 호출 가능 객체를 전달하여 역전 로직을 정의해야 한다 ([1차: https://docs.djangoproject.com/en/6.0/topics/migrations/]).

---

## Q2: expand-contract 패턴의 원저자 및 공식 규정

### Q2a: 원저자 및 출처

**[주장 — 검증됨]** expand-contract 패턴은 원래 다른 곳에 문서화되었으며, 다음이 인정된다 ([1차: https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html]):

1. **Michael T. Nygard**, *Release It!* (O'Reilly, 2007) — "Zero Downtime Deployments" 장에 문서화됨 ([미확인]: 검색 결과만 확인, Release It! 원문 미열람)
2. **Danilo Sato** — Parallel Change 주제의 기사

**[정의 — 원문]** Wellhausen 논문에서 인용: 
> "파괴적 변경을 여러 단계에서 구현하여 각 개별 단계가 시스템을 파괴하지 않고 되돌릴 수 있도록 한다. 먼저 새 구조를 데이터베이스에 추가하여 시스템을 확장한다. 그 다음 기존 데이터를 새 구조로 마이그레이션하면서 시스템이 구 구조와 신 구조 모두에 중복으로 기록한다. 마이그레이션이 완료되면 구 데이터 구조와 구 코드를 제거하여 시스템을 축소한다."
([1차: https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html])

### Q2b: 패턴 설명 (Prisma Data Guide)

**[규정]** Prisma Data Guide에서 seven-step 프로세스 설명 ([2차: https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern]):

1. 새 스키마 빌드 및 배포 (기존 구조 유지)
2. 인터페이스 확장: 구 구조와 신 구조 모두에 기록
3. 기존 데이터를 신 스키마로 마이그레이션
4. 신 인터페이스 테스트
5. 읽기를 신 구조로 전환
6. 구 구조 쓰기 중단
7. 구 구조 완전 제거

**[파괴적 변경 규정]** "신 컬럼은 현재 클라이언트 동작을 방해하는 제약이 없어야 한다 — 일반적으로 nullable 필드 또는 기본값이 필요하다" ([2차: https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern]).

**[돌이킬 수 없는 지점]** "5단계(읽기 전환) 후 롤백하면 신 테이블에 수집된 고유 데이터가 손실된다" — 이것이 진정한 돌이킬 수 없는 지점이다 ([2차: https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern]).

---

## 상충 및 부정 증거

없음 (모든 주요 도구 문서가 일관성 있게 rollback 제약을 기술함).

---

## 미해결

1. **Alembic 상세 제약**: Alembic 공식 API 문서는 downgrade의 제약을 명시하지 않음. 더 상세한 튜토리얼이나 가이드 필요 ([미확인]: 본문 미확인).
2. **Prisma rollback 메커니즘**: `prisma migrate resolve --rolled-back` 명령의 공식 문서 원문 미열람 (검색 결과만 확인).
3. **Michael T. Nygard Release It! 원문**: expand-contract 패턴의 원저자로 인정되나, Release It! 원본 텍스트 미열람 (검색 결과 스니펫만 확인).
4. **도구별 프로덕션 권고의 규범 강도**: 각 도구가 "MUST" vs "SHOULD"를 명확히 구분하는지 확인 필요 (현재 요약은 권고로 표기).

---

## 출처

### 1차 (공식 문서)

#### Flyway
- [Undo Migrations](https://documentation.red-gate.com/fd/undo-migrations-273973334.html) — Redgate Flyway 공식 문서
- [Frequently Asked Questions](https://documentation.red-gate.com/fd/frequently-asked-questions-277579363.html) — Redgate Flyway 공식 FAQ

#### Alembic
- [Commands API](https://alembic.sqlalchemy.org/en/latest/api/commands.html) — SQLAlchemy Alembic 공식 API 문서

#### Prisma
- [Generating Down Migrations](https://www.prisma.io/docs/orm/prisma-migrate/workflows/generating-down-migrations) — Prisma 공식 문서
- [Patching & Hotfixing](https://www.prisma.io/docs/orm/prisma-migrate/workflows/patching-and-hotfixing) — Prisma 공식 문서

#### Django
- [Migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/) — Django 공식 문서

#### expand-contract 패턴
- [Expand and Contract Pattern](https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html) — Tim Wellhausen 논문 (원저자 인정 포함)

### 2차 (요약, 해석, 벤더 블로그, 가이드)

- [Baeldung: Rolling Back Migrations with Flyway](https://www.baeldung.com/flyway-roll-back)
- [Medium: Expand and Contract Method](https://medium.com/@jasminfluri/expand-and-contract-method-for-database-changes-414d236f236f)
- [Xata: pgroll and expand-contract](https://xata.io/blog/pgroll-expand-contract)
- [Prisma Data Guide: Expand and Contract Pattern](https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern) — 개념 설명 가이드

### 미확인

- Alembic 상세 제약 (더 상세한 가이드 필요)
