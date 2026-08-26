# `project-template` · `workflows` 감사 — 현재 상태

> 감사 2026-08-26 · **이 판 2026-08-26(같은 날 처리분 반영)**.
> ⚠️ 감사 시점의 전체 서술은 로컬 `.scratch/` 에 남아 있으나 **추적되지 않는다**(`.gitignore`) —
> **하중을 지는 결론은 전부 이 문서와 [`ARSENAL`](ARSENAL.ko.md) 로 옮겼다.**
>
> **이 문서는 *현재 상태*를 진술한다.** 무엇이 어쩌다 그렇게 됐는지는 원본과 PR 이력이 갖는다 —
> `direction` 3단계 재도출에서 세운 원칙과 같다.

## 지금 이 이름이 정확하다

> **AI 에이전트와 함께 쓰는 Python 패키지형 프로젝트의 최소 전문 개발 베이스라인 v0.x**

아직 이렇게 부르면 안 된다 — *모든 프로젝트에 맞는 현업 표준* · *에이전트가 끌 수 없는 완전한 장벽* ·
*기획부터 운영까지 끝난 파이프라인*.

## 기계 판정은 네 층이 함께 있어야 성립한다

| 층 | 역할 |
|---|---|
| `project-template` | **무엇을 검사할지** 준비 (테스트 · ruff · mypy · `uv.lock` · CI 호출) |
| `workflows` | **검사를 실행** (공통 Python CI · 룰셋 설치) |
| GitHub 서버 설정 | **실패하면 머지를 막는다** (룰셋 · required checks · Actions 정책) |
| **권한과 자격증명** | **앞의 장벽을 누가 바꿀 수 있는지 정한다** |

> 세 문장은 서로 다르다 — 테스트가 **있다** / CI 가 테스트를 **실행한다** / 실패하면 GitHub 가 머지를 **거부한다**.
> 🔴 **그리고 에이전트가 룰셋을 지울 수 없어야 비로소 외부 장벽이다.** 네 번째 층이 남은 가장 큰 구멍이다.

## ✅ 2026-08-26 에 닫은 것 — 9건

| | 무엇 | 실측 |
|---|---|---|
| **B-2** | required check 출처를 **GitHub Actions App(`15368`)** 에 고정 | 3/3 · PR 머지로 확인(`mergeStateStatus: CLEAN`) |
| **B-1** | **서버** SHA 강제 | `sha_pinning_required: true` 3/3 · CI 재실행으로 검증 |
| **B-3** | 머지 방법 정합 | squash 전용 + 브랜치 자동 삭제 3/3 |
| **B-4** | **drift 감사** — 읽기 전용, 대상 저장소 **밖**에서 돈다 | [`tools/repo_audit.py`](../tools/repo_audit.py) · 현재 `CLEAN findings=0` |
| **C-1** | Dependabot 취약점 경보 + 보안 업데이트 | 404 → **204** · `enabled` 3/3 |
| **E-2** | `new-project.sh` **전체 fail-closed** | `trap` 으로 전 단계 — 실패 시 원격을 남기지 않는다 |
| **E-3** | 생성 시 **서버 바닥까지** 설치 | Dependabot · SHA 강제 · 머지 설정을 생성 직후 건다 |
| **E-5** | *"로직 9줄"* 주장 삭제 | **책임 서술로 교체** — 저장소 생성 + 서버 바닥, 그 밖은 신호 |
| **D-1** | 템플릿 이름 치환 | [`bootstrap.sh`](https://github.com/coolbress/project-template/blob/main/bootstrap.sh) · 치환 후 `uv sync`+`pytest` 통과 |

🔴 **drift 감사가 첫 실행에서 진짜 결함을 잡았다** — `standards` 의 시크릿 탐지·푸시 보호가 꺼져 있었다
(`new-project.sh` 가 **새 저장소에만** 켜주는데 `standards` 는 그걸로 만든 게 아니었다). 켰다.

⚠️ **B-1 의 절반은 못 했다** — Actions **allowlist** 는 `standards`·`project-template` 만 걸었다.
`workflows` 는 `docker://rhysd/actionlint` 가 allowlist 패턴에 들어가지 않아 `startup_failure` 가 났고,
**되돌려 SHA 강제만 유지**했다. 고치려면 actionlint 를 일반 Action 으로 바꿔야 한다.

🔴 **그리고 같은 선택이 두 번째 값을 치른다** — `docker://` Action 은 **의존성 그래프에도 안 잡힌다**
([`DEPENDENCY-GRAPH-SCOPE`](DEPENDENCY-GRAPH-SCOPE.ko.md)). 경보도 갱신 PR 도 오지 않는다.
**핀이 되어 있다는 것과 지켜보고 있다는 것은 다른 문장이다.** 일반 Action 으로 바꾸면 두 구멍이 같이 닫힌다.

## 남은 것 — **종류를 먼저 가른다**

*"남았다"* 를 전부 같은 칸에 넣으면 **실행을 미루는 핑계가 리서치가 된다.** 셋으로 가른다.

### 🔧 실행 — ✅ **일곱 건 전부 처리, 서버 초록만 남았다** (2026-08-26)

⚠️ **GitHub Actions major outage 중이라 서버 검증은 대기**다. 아래 실측은 **로컬**이다.

| | 무엇 | 결과 |
|---|---|---|
| **E-1** | `workflows` 자기 CI 가 `actionlint` 만 돈다 | ✅ **다섯으로** — `bash -n` · `shellcheck` · **룰셋 불변식 10/10** · **실패 경로 10/10**([PR #10](https://github.com/coolbress/workflows/pull/10)) |
| **E-1b** | 중앙 workflow 배포 전 **consumer canary** | ✅ **`canary/` 가 `python-ci.yml` 을 실제로 호출**한다. 선택 입력 `working-directory` 추가(기존 호출부 무변경) |
| **D-3** | Python 실행 버전 미고정 | ✅ **`.python-version`(3.12) 하나** — uv 가 읽으므로 **워크플로에 또 적지 않는다**([PR #7](https://github.com/coolbress/project-template/pull/7)) |
| **D-4** | 빌드만 하고 **설치를 시험하지 않는다** | ✅ wheel·sdist 를 **깨끗한 venv 에 설치하고 import 까지** |
| **D-7** | 빈 파일이 *"준비 완료"* 로 보인다 | ✅ `SECURITY.md` 의 3일/60일을 **목표로 정정**(1인 대응 체계 명시) · `.env.example` 에 **검사를 붙였다**(`test_env_example.py` 가 소스의 `os.environ` 키를 전부 찾는다). ⚠️ **CHANGELOG 는 프로필 결정(D-2)에 걸린다** |
| **D-8** | 배포 메타데이터 부족 | ✅ `readme`·`license`(SPDX)·`license-files`·`authors`·`urls` · **bootstrap 이 이름·라이선스를 치환**. ⚠️ public library 전용 항목은 **D-2** 에 걸린다 |
| — | CI **timeout** · 오래된 실행 취소 | ✅ 잡마다 `timeout-minutes: 10` · PR 은 `cancel-in-progress` |

> 🔴 **만들다가 진짜 결함을 하나 잡았다** — `bootstrap.sh` 가 이름을 바꾸면 **`uv.lock` 의 `name` 도 달라지는데
> 다시 잠그지 않았다.** CI 첫 줄이 `uv sync --locked` 이므로 **새 저장소는 첫 PR 부터 실패**했을 것이고,
> 벽이 서 있으니 **그대로 잠겼을 것**이다. 못 본 이유가 방법론이다 —
> **이전 검증이 `--locked` 없이 `uv sync` 를 돌렸다. 검증 명령이 CI 와 달랐다.**

### 🔶 결정 — 소유자가 정해야 실행이 정해진다

| | 무엇 | 왜 결정인가 |
|---|---|---|
| **A-1** | **권한 분리** — 에이전트에서 admin·Actions설정·Secrets 를 뺀다 | **당신 계정 자격증명 운용**이다. 이것 없이는 *"에이전트가 못 끄는 벽"* 이 성립하지 않는다 |
| **A-2** | `workflows` 는 **중앙 공급망인데 사람 승인 0** | 승인을 요구하면 솔로가 자기 PR 을 못 승인한다 — 트레이드오프 |
| **D-2** | **app 인가 library 인가** | 프로필을 둘로 가르는 결정. `bootstrap.sh` 는 **이름만** 바꿨다 |
| **E-4** | `kickoff` 가 저장소 역할을 섞는다 | 어디에 살아야 하는가의 결정 |
| **D-5** | 문서 규칙끼리 충돌 | 어느 쪽을 살릴지 |

### 🔬 리서치 — 근거가 실제로 없거나 얇다

**여기가 *"리서치로 채운다"* 가 성립하는 유일한 칸이다.**

| | 질문 | 왜 리서치인가 |
|---|---|---|
| **E-6** | **4잡(lint·typecheck·test·build) vs 1잡(`ci / verify`)** | 우리 4검사는 **`C50-12` 가 *"4종이 보편"* 을 기각**한 상태다(🔵 프로젝트 선택). 어느 쪽이 나은지는 **대표 작업 측정**으로만 답한다 — wall time · runner time · 실패 진단성 · 변경 비용 |
| **C-2** | **CodeQL vs Semgrep** | 🟢 **제약은 이미 확인**됐다(`FFA-008` — 비공개는 `GitHub Code Security` 라이선스 필요). **탐지율·오탐 비교는 미조사** |
| **C-3** | secret 도구를 **겹칠 것인가** | gitleaks + push protection 이 겹친다. **겹침이 값을 하는지** 재본 적 없다 |
| ~~**C-4**~~ | ✅ **종료 2026-08-26** — [`DEPENDENCY-GRAPH-SCOPE`](DEPENDENCY-GRAPH-SCOPE.ko.md) | `uv.lock` 은 **전이 의존성까지** 보인다(선언 3 → 그래프 15) · 재사용 워크플로 참조도 보인다. 🔴 **`docker://` Action 과 `[build-system] requires` 는 안 보인다** — actionlint 가 **allowlist(B-1)와 그래프 양쪽에서 구멍**을 낸다 |

⚠️ **나머지는 리서치 문제가 아니다.** *"근거가 없어서 못 한다"* 와 *"안 했다"* 를 구별한다 —
[`evidence-holes-register`](../corpus/methods/evidence-holes-register.md) 가 같은 이유로 존재한다.

## 생성 방식 — 다시 발명하지 않는다

**규칙 1**(*만들기 전에 먼저 찾는다*)을 스캐폴딩에 그대로 적용한 결정이다. 순서가 있다.

1. **`uv init --app` / `--package` / `--lib` 가 만드는 표준 골격을 쓴다.** 우리가 Python 구조를 발명하지 않는다.
2. 우리에게만 필요한 것(CI 호출 · 룰셋 · Brief)을 **얇게 덧씌운다**.
3. 이름 치환과 선택지가 몇 개뿐이면 **작은 bootstrap adapter 로 끝낸다** — ✅ 지금이 여기다(`bootstrap.sh`).
4. 🔶 **Copier 는 *"템플릿 갱신을 여러 프로젝트에 반복 적용"* 문제가 실제로 생길 때만 검토한다.**

**왜 이 순서인가**: GitHub template repository 는 **파일 복사는 되지만 변수 치환도 update 채널도 없다**.
Copier 는 답을 기록하고 update 를 주지만 **관리할 도구가 하나 는다** — 대전제 2(*작고 가볍게*)에 걸린다.
**아직 겪지 않은 문제를 위해 도구를 먼저 들이지 않는다.**

## 이 감사에서 배운 것 — 방법론

- **로컬 `origin/main` 이 서버보다 뒤였다.** 감사는 **먼저 `git fetch` 또는 API 로 서버 최신 SHA 를 확인**하고 시작한다.
- **파일과 서버 설정을 같이 봐야 한다.** 파일이 Action 을 SHA 로 핀해도 **서버가 태그를 막지 않으면** 습관일 뿐이다.
- **감사자가 감사 대상 안에 있으면 안 된다**(B-4). `repo_audit.py` 를 `standards` 에 둔 이유다.
