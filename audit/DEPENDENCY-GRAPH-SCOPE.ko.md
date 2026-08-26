# 의존성 그래프는 우리 저장소에서 **무엇까지 보는가** — C-4 실측

> 측정 2026-08-26 · 대상 `coolbress/{standards, workflows, project-template}` ·
> 수단 `GET /repos/{o}/{r}/dependency-graph/sbom` (GitHub 이 스스로 만든 SBOM 을 그대로 읽는다)
>
> [`TEMPLATE-WORKFLOWS-AUDIT`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) **C-4** 를 닫는다.
> 질문은 *"`uv.lock` 을 GitHub 이 어디까지 읽는가"* 였다. **읽는 범위보다 *안 읽는* 범위가 중요했다.**

## 결론

| 무엇 | 보이나 | 근거 |
|---|---|---|
| **`uv.lock`** — 직접 의존성 | 🟢 **보인다** | `ruff` · `mypy` · `pytest` |
| **`uv.lock`** — **전이 의존성** | 🟢 **보인다** | `iniconfig` · `pluggy` · `pathspec` · `packaging` · `colorama` · `typing-extensions` … **선언은 3개인데 그래프는 15개**다 |
| `uses:` **Action** (SHA 핀) | 🟢 보인다 | `pkg:githubactions/actions/checkout@3d3c42e…` |
| **재사용 워크플로 참조** | 🟢 **보인다** | `coolbress/workflows/.github/workflows/python-ci.yml` — **중앙 공급망 링크가 그래프 안에 있다** |
| 🔴 **`docker://` Action** | 🔴 **안 보인다** | `docker://rhysd/actionlint@sha256:…` 가 SBOM 에 **없다** |
| 🔴 **`[build-system] requires`** | 🔴 **안 보인다** | `hatchling` 이 SBOM 에 **없다** — 빌드 백엔드는 그래프 밖이다 |

현재 Dependabot 경보: 세 저장소 모두 **0건**.

## 🔴 `docker://` actionlint 는 **두 번 값을 치른다**

같은 선택이 서로 다른 두 층에서 구멍을 낸다:

| | 무엇이 안 되나 |
|---|---|
| **Actions allowlist**(감사 **B-1**) | 패턴에 `docker://` 가 들어가지 않아 `workflows` 만 allowlist 를 못 걸었다(`startup_failure`). **되돌려 SHA 강제만 유지**했다 |
| **의존성 그래프**(여기) | SBOM 에 없다 → **취약점 경보도, Dependabot 갱신 PR 도 오지 않는다.** 우리가 손으로 다이제스트를 올리지 않으면 영원히 그 자리다 |

> **핀이 되어 있다는 것과 지켜보고 있다는 것은 다른 문장이다.**
> `sha256:` 다이제스트 핀은 **바뀌지 않음**을 보장하지 실패 사실을 알려주지 않는다.

**따라서 actionlint 를 일반 Action(또는 핀된 바이너리 설치)으로 바꾸면 두 구멍이 같이 닫힌다.**
이건 리서치가 아니라 실행 항목이다 — 감사 **B-1** 잔여분에 붙인다.

## `[build-system] requires` 가 그래프 밖이라는 것

`hatchling` 은 **빌드할 때 실행되는 코드**인데 경보 대상이 아니다.
바닥이 *"의존성 갱신 봇"* 을 MUST 로 두는 이유(공급망)를 생각하면 **빈칸이 맞다** —
다만 **크지 않다**: 빌드는 CI 안에서만 돌고, 산출물에 섞이지 않는다.
지금은 **기록만 하고 조치하지 않는다.** 조치하려면 `uv.lock` 이 아니라 별도 잠금이 필요하다.

## 측정 방법 — 다시 재고 싶으면

```bash
gh api repos/coolbress/<repo>/dependency-graph/sbom \
  --jq '.sbom.packages[] | .name + "  " + ((.externalRefs//[])|map(.referenceLocator)|join(","))'
```

⚠️ **SBOM 은 기본 브랜치 기준이다.** 브랜치의 변경은 머지 전에는 안 보인다 —
그래서 *"canary 의 하위 디렉터리 `uv.lock` 도 읽는가"* 는 **머지 후에만 답할 수 있다**(열어 둔다).
