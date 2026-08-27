# CodeQL vs Semgrep OSS — C-2 실측

> 측정 2026-08-27 · `coolbress/workflows` 브랜치 `research/c2-sast` ·
> **같은 코퍼스 · 같은 run · 결과는 저장소 경보로 올리지 않음**(`upload: false`)
>
> [`TEMPLATE-WORKFLOWS-AUDIT`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) **C-2** 를 닫는다.
>
> **왜 재야 했나**: 🟢 **제약은 이미 확인**됐다 — 비공개 저장소의 CodeQL 은
> `GitHub Code Security` 라이선스가 필요하다(`FFA-008`). 🔴 **하지만 *"그러니 Semgrep"* 은
> 근거가 아니라 소거법**이었다. **탐지율·오탐을 잰 적이 없었다.**

## ⚠️ 먼저 한정 — 이건 **마이크로 벤치마크**다

- **n=9 부류.** 내가 골라서 심었다 — **두 도구가 규칙을 가지고 있을 법한 부류**로 기울어 있다
- 코드가 **아주 작다.** 큰 코드베이스의 오탐률·스캔 시간은 여기서 알 수 없다
- CodeQL `security-extended` · Semgrep OSS `p/python` + `p/secrets` 로 1회씩
- **답하는 질문은 하나뿐**: ***"뻔한 부류를 잡는가"*** — *"어느 도구가 더 낫다"* 가 아니다

## 🔴 1차 측정이 도구를 오해할 뻔했다

처음에는 함수만 있는 `vulnerable.py` 로 쟀고 **CodeQL 1건 · Semgrep 4건**이 나왔다.
**CodeQL 이 못 잡은 게 아니다** — CodeQL 의 주력 질의는 **데이터흐름 추적**이라
***"이 값이 밖에서 왔다"*** 가 성립해야 경보를 낸다. **출발점이 없으면 침묵하는 것이 설계다.**

> **이 차이를 만들어 놓지 않고 비교했다면 숫자는 맞고 결론은 틀렸을 것이다.**
> 그래서 같은 9종을 `flask.request` 에서 흘려보낸 `web.py` 를 추가해 다시 쟀다.

## 결과

### ① 진입점이 있을 때 (`web.py` — 실제 웹앱 모양)

| 심은 부류 | CodeQL | Semgrep OSS |
|---|:--:|:--:|
| SQL 주입 | ✅ `py/sql-injection` | ✅ |
| 명령 주입 | ✅ `py/command-line-injection` | ✅ |
| **역직렬화(pickle)** | ✅ `py/unsafe-deserialization` | 🔴 **놓침** |
| 경로 순회 | ✅ `py/path-injection` | ✅ |
| 약한 해시(md5) | ✅ | ✅ |
| SSRF | ✅ `py/full-ssrf` | ✅ |
| 안전하지 않은 YAML | ✅ | ✅ |
| eval 주입 | ✅ `py/code-injection` | ✅ |
| **합** | **8 / 8** | **7 / 8** |

🟢 **CodeQL 은 심지 않은 부류도 찾았다** — `py/reflective-xss` **3건**(오염된 값을 응답에 그대로 되돌림).
**오탐이 아니라 진짜 문제**다. 내가 코퍼스를 만들면서 못 본 것을 도구가 봤다.

### ② 진입점이 없을 때 (`vulnerable.py` — 라이브러리 모양)

| | 잡은 부류 |
|---|---|
| CodeQL | **1 / 9** (약한 해시만) |
| Semgrep | **3 / 9** (명령·해시·YAML — 패턴만으로 서는 것들) |

> **둘 다 급락한다.** 이건 도구의 결함이 아니라 **오염 추적의 성질**이다.
> 🔴 **함의**: *"SAST 를 켜 뒀으니 안전하다"* 는 **진입점이 모델링될 때만** 참이다.

### ③ 오탐 · 시간

| | 안전한 쌍둥이(`safe.py`) 경보 | 스캔 시간 |
|---|:--:|---:|
| CodeQL | **0** | 41s |
| Semgrep | **0** | 15s |

**둘 다 오탐 0**이다(이 크기에서는). Semgrep 은 **한 문제에 규칙 여러 개가 겹쳐 울린다**(7부류 → 13건) — 틀린 건 아니지만 **읽는 사람이 세어야 한다.**

### ④ 🔴 **둘 다 하드코딩 자격증명을 놓쳤다**

`DB_PASSWORD = "correct-horse-battery-staple"` — **CodeQL도 Semgrep도 안 잡았다.**

> **SAST 는 시크릿 탐지를 대체하지 않는다.** 층이 다르다.

## 🔬 덤 — **C-3 의 실측이 사고로 하나 나왔다**

코퍼스에 공급자 형식 키(`sk_live_…`)를 넣었더니 **`git push` 가 서버에서 거부됐다**:

```
remote: — GITHUB PUSH PROTECTION —
remote:   locations: research/make-c2-corpus.sh:26
remote: (?) To push, remove secret from commit(s) …
```

🟢 **푸시 보호는 실제로 막는다** — 경보가 아니라 **차단**이고, **커밋 전에** 선다.
이건 SAST 도 CI 도 아니고 **서버 층**이다. [`C-3`](TEMPLATE-WORKFLOWS-AUDIT.ko.md) 의 절반이 여기서 답해진다 —
남은 질문은 *"push protection 이 있는데 **gitleaks 를 더할 값이 있나**"* 뿐이다.

## 그래서 무엇을 고르나 — **권고**(결정은 소유자)

| 저장소 | 권고 | 왜 |
|---|---|---|
| **공개** | **CodeQL default setup** | **무료** · **8/8** · 유지할 워크플로가 **없다**(설정 한 번) · 심지 않은 부류까지 |
| **비공개** | **Semgrep OSS** | 라이선스 없이 **7/8** · 15s · `python-ci.yml` 에 잡 하나 |

**둘 다 켤 이유는 약하다** — 겹치는 부류가 대부분이고, 잡는 것도 겹친다.
*"이유 없이 CodeQL 과 Semgrep 을 함께 돌리는 것"* 은 [`ARSENAL`](ARSENAL.ko.md) §덜어낼 것에 이미 올라 있다.

🔴 **어느 쪽을 고르든 시크릿 층은 따로 있어야 한다** — ④ 가 그것을 보였다.
현재 세 저장소는 **secret scanning + push protection 이 켜져 있고**(`repo_audit` 이 검사한다),
**gitleaks 를 더할지는 C-3 에 남는다.**

## 다시 재는 법

```bash
git push origin research/<이름>        # research/** 푸시가 measure-sast.yml 을 돌린다
```

코퍼스는 **커밋되지 않는다** — `research/make-c2-corpus.sh` 가 런타임에 만든다.
⚠️ **공급자 형식 시크릿을 코퍼스에 넣지 마라.** 푸시 보호가 막는다(위 §C-3).
