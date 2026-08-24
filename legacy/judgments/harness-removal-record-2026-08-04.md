> ## ⚠️ 이관 (2026-08-24) — 이것은 **선례**다
>
> 원본 `~/Archive/goppi-removal-2026-08-04/REMOVAL-RECORD.md`. 구 goppi를 로컬에서 제거할 때
> 남긴 기록이며, **지금 예정된 하네스 제거(2026-08-24)의 직접적 선례**다.
>
> **가장 값어치 있는 부분은 §"문서 가정과 실제의 차이"** — 인계 문서가 전제한 설치 형태
> (`--plugin-dir` + 셸 alias)와 **실제 설치 형태**(마켓플레이스 플러그인)가 달랐다.
> 제거 절차를 문서만 보고 짜면 안 되고 **실제 상태를 먼저 조회해야 한다**는 실측이다.
>
> 백업 실물(설정 4종·plugin-remnants·doctor BEFORE/AFTER·SHA256SUMS, 44MB)은
> `~/Archive/goppi-removal-2026-08-04/`에 **로컬로만** 남아 있다.

---


> 실행: goppi_final 실행 세션 (Claude Code / Opus 5 1M) · 사용자 단계별 승인 후 실행
> 절차 근거: `/Users/coolbress/goppi_final/HANDOFF.md` §2 (다만 실제 설치 형태가 문서 가정과 달라 아래처럼 조정)

## 문서 가정과 실제의 차이

HANDOFF §2는 `claude --plugin-dir ~/goppi` 사용 경로와 셸 alias 제거를 전제했으나, 실제 설치는
**marketplace 플러그인**(CC: `enabledPlugins`/`extraKnownMarketplaces`, Codex: `[plugins]`/`[marketplaces]`)
이었다. 셸 설정(`.zshrc`/`.zprofile`/`.zshenv`/`.bashrc`/`.bash_profile`)에는 goppi 언급이 **없었다**.
또한 Codex `config.toml`에 `:root=deny` 권한 프로필은 **존재하지 않았고**, `.codex/rules/default.rules`는
`prefix_rule(pattern=["gh","issue","edit"], decision="allow")` 한 줄로 goppi 귀속이 아니어서 유지했다.
스킬 루트(`~/.codex/skills`, `~/.agents/skills`)에도 goppi 스킬은 없었다.

## 백업 (이 디렉토리)

| 파일 | 원 위치 |
|---|---|
| `claude-CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `claude-settings.json` | `~/.claude/settings.json` |
| `codex-config.toml` | `~/.codex/config.toml` |
| `codex-AGENTS.md` | `~/.codex/AGENTS.md` |
| `claude-plugins-installed_plugins.json` | `~/.claude/plugins/installed_plugins.json` |
| `claude-plugins-known_marketplaces.json` | `~/.claude/plugins/known_marketplaces.json` |
| `plugin-remnants/claude-marketplaces-goppi/` | `~/.claude/plugins/marketplaces/goppi/` |
| `plugin-remnants/claude-cache-goppi/` | `~/.claude/plugins/cache/goppi/` |
| `plugin-remnants/codex-cache-goppi/` | `~/.codex/plugins/cache/goppi/` |

`SHA256SUMS.txt`는 최초 4개 설정 파일의 제거 **전** 해시다. `doctor-BEFORE.txt` / `doctor-AFTER.txt`는
`~/goppi/hosts/goppi-doctor.sh` 출력이다.

## 수행한 변경

### Claude Code
1. `~/.claude/CLAUDE.md` **삭제** — 내용은 `@/Users/coolbress/goppi/GOPPI.md` 한 줄뿐이었다 (사용자 결정: 빈 파일로 남기지 않고 삭제).
2. `~/.claude/settings.json` — `enabledPlugins["goppi@goppi"]`와 `extraKnownMarketplaces.goppi`만 제거.
   **permissions(G7)·model·orca hooks·skillOverrides는 손대지 않았다.**
3. `~/.claude/plugins/installed_plugins.json` — `goppi@goppi` 항목 제거.
4. `~/.claude/plugins/known_marketplaces.json` — `goppi` 항목 제거.
5. `marketplaces/goppi`, `cache/goppi` → 이 백업의 `plugin-remnants/`로 **이동**(삭제 아님).

### Codex
1. `~/.codex/AGENTS.md` **삭제** — 전체가 `hosts/sync-agents.sh`가 GOPPI.md에서 생성한 인라인 계약이었다.
2. `~/.codex/config.toml` — `[marketplaces.goppi]`, `[hooks.state."goppi@goppi:…"]` 3개, `[plugins."goppi@goppi"]` 제거.
   `[projects."/Users/coolbress/goppi"] trust_level`은 저장소를 보존하므로 유지.
3. `~/.codex/plugins/cache/goppi` → `plugin-remnants/`로 이동.

### 보존한 것 (의도적)
- **`~/goppi` 저장소 전체** — prior art 참조용. 삭제하지 않았다.
- **G7 안전 세트** (사용자 결정) — deny 6개 / ask 12개. goppi 이전부터의 개인 선호이며,
  vanilla arm의 host safety floor에 포함되는 것이 정직하다.
- `~/.claude/projects/-Users-coolbress-goppi/memory/` 6개 — 그 저장소 세션에서만 로드되므로 오염 없음.

### 정리한 것
- `~/.claude/projects/-Users-coolbress/memory/harness-redesign-2026-07.md` — "goppi를 지금 만드는 중"이라는
  철 지난 내용을 현행 상태(goppi_final, 구 goppi 제거됨)로 갱신. 사용자 상수 6가지는 보존.

## 검증

| 검사 | 결과 |
|---|---|
| `goppi-doctor.sh` 제거 전 | `critical controls PRESENT ✓` + warning 5 (exit 0) |
| `goppi-doctor.sh` 제거 후 | **`FAIL contract missing or incomplete` · `a CRITICAL control is missing ✗` (exit 1)** — 계약 부재 확인 |
| 파일 부재 | `~/.claude/CLAUDE.md` · `~/.codex/AGENTS.md` · 3개 플러그인 디렉토리 모두 부재 |
| 설정 문자열 | `settings.json` 0건 · `installed_plugins.json` 0건 · `known_marketplaces.json` 0건 |
| `config.toml` | goppi 문자열 6건 잔존 — **전부 `[projects.*] trust_level`** (하네스 설정 아님) |
| JSON/TOML 유효성 | `json.load` / `tomllib.load` 모두 OK |
| G7 보존 | deny 6 / ask 12 |

### 아직 검증하지 않은 것 (UNVERIFIED)

- **새 세션 런타임 부재**: 이 제거를 수행한 세션은 시작 시점에 이미 GOPPI.md를 컨텍스트에 로드한 상태였다.
  "새 Claude Code 세션에서 계약이 주입되지 않는다 / 훅이 발화하지 않는다", "새 Codex 세션의 AGENTS.md
  렌더에 계약이 없다"는 **다음 세션에서 직접 확인해야 한다.** 파일·설정 수준의 부재만 위 표로 증명됐다.

## 후속 권고 (미실행 — 사용자 판단)

`~/.codex/config.toml`에 이제는 존재하지 않는 임시 경로 4개가 `trust_level = "trusted"`로 남아 있다
(`/private/tmp/goppi-codex-pair.PuB2b6/{isolation-probe,harness,vanilla}`,
`/private/tmp/claude-501/-Users-coolbress-goppi/…/codex-probe-iso`). 같은 경로가 재생성되면 자동으로
신뢰되므로 정리를 권한다. goppi 제거 범위 밖이라 이번에는 손대지 않았다.

## 복구 방법

1. 위 표대로 파일을 원 위치로 복사/이동.
2. 또는 저장소가 그대로 있으므로 마켓플레이스에서 재설치: `/plugin marketplace add coolbress/goppi`.
