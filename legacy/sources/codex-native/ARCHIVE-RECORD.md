# codex-native — 아카이브 기록 (여섯 번째 하네스)

**2026-08-24에 `~/plugins/codex-native`에서 발견됐다.** 그전까지 이 저장소는
*"codex-native 시도는 별도 하네스가 아니라 goppi 안의 결정이었다"* 고 적고 있었다 — **틀렸다.**
실물 플러그인이 디스크에 있었고, 그 시점은 goppi보다 **9일 앞선다.**

## 무엇인가

`.codex-plugin/plugin.json`을 가진 **Codex 플러그인**. 자기 서술:

> *"A native-first adaptive Codex workflow with proportional verification, independent review,
> reviewed improvement, and evidence-aware GitHub delivery."*

스킬 2종(`codex-native-harness` · `github-workflow`) · 레퍼런스 8종 · 평가 하네스(`evals/` + 스크립트 5종).

## 언제 — 계보의 빈 구간을 메운다

| 시각 | 사건 |
|---|---|
| 2026-07-11 | **gingoa 마지막 커밋** (범위 폭발로 종료) |
| 2026-07-12 20:51 | codex-native 파일 15개 생성 — *gingoa가 죽은 다음 날* |
| 2026-07-14 13:13~13:19 | SKILL 2종 개정 · `evals/` 정비 |
| **2026-07-14 13:23:39** | **`plugin.json` v0.3.1 스탬프** (`0.3.1+codex.20260714042339`) |
| **2026-07-14 16:08:30** | **claudeck-v1 마지막 커밋** — *"final settings state before v1 retirement"* |
| 2026-07-21 | goppi 첫 커밋 |

**같은 날 오후, 3시간 차로 v1이 은퇴했다.** LINEAGE §1은 그 07-14 커밋을 *"마무리이지 병행 개발이
아니다"* 라고 판정했는데 — 판정 자체는 맞다(v1에 새 개발은 없었다). 다만 **왜 그날 은퇴시켰는지**는
이제 보인다: 소유자는 이미 Codex 네이티브 플러그인으로 옮겨가 있었다.

## goppi ADR-0023과의 관계 — 별개다

goppi ADR-0023(*"Full codex-native replacement"*)은 **07-21 이후**의 결정이다.
이 플러그인은 그보다 **9일 먼저** 존재했다. 따라서 순서는:

**codex-native 플러그인(07-12~14) → goppi 시작(07-21) → ADR-0023 → goppi_final에서 호스트를
Claude Code 하나로 좁힘(08-03)**

ADR-0023은 이 플러그인의 *설계 결정*이 아니라, 이미 만들어봤던 것을 goppi 안에서 다시 시도한 것이다.

## 이 폴더에 무엇이 있나

| 파일 | 무엇 |
|---|---|
| `FILE-MANIFEST.tsv` (23행) | 전 파일 경로·크기·mtime·SHA-256 — **원본이 사라져도 인용이 검증된다** |
| `.codex-plugin/plugin.json` | 정체·버전·자기 서술 |
| `skills/codex-native-harness/` | SKILL + 레퍼런스 5종 (routing · governed · verification · independent-review · evaluation) |
| `skills/github-workflow/` | SKILL + 레퍼런스 3종 (evidence-baseline · codex-native-settings · merge-execution) |

**바이트 수정 없는 사본이다.** 상호 참조 링크가 살아 있도록 원본 트리 구조를 그대로 유지했다.

## 옮기지 않은 것

- `scripts/` 5종 (`eval_loop.py` 706줄 · `fixture_runner.py` 300줄 · 테스트 3종) — 2026-08-24 처분
  원칙 *"소스코드는 버린다"*. 존재는 `FILE-MANIFEST.tsv`가 기록한다.
- `evals/{cases,fixtures,manifest}.json` · `evals/results/2026-07-12.json` — **폐기**.
  결과는 3케이스 × **n=1**이고 스스로 `"traceability": "legacy-untraceable"` · `"status": "partial"`
  이라고 적는다. goppi eval 결과(n=1)에 적용한 처분과 같다(`DISPOSITION.md` 참조).
- `agents/openai.yaml` 2종 — 모델 라우팅 설정. `corpus/aspects/27-…/multi-agent-orchestration-standard.md`
  가 다루는 주제이며, 이 스냅샷은 2026-07 시점 값이라 현행 근거가 아니다.

## 원본

`~/plugins/codex-native` — **2026-08-24에 제거**(휴지통 `~/.Trash/codex-native-uninstall-2026-08-24`).
git 저장소가 아니었다(커밋 이력 없음). 따라서 **커밋 수는 계보 총계 436건에 더해지지 않는다** —
세대 수만 5 → **6**으로 정정된다.
