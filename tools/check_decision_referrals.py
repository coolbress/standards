#!/usr/bin/env python3
"""요구 ③ — **회부가 로그에 남는가**를 잰다 (`GAPS` R5-37).

## 왜 이게 있나

`direction/04` §판정 기준이 요구 ③ 의 기록 수단을 못박아 뒀다:
*"회부를 **이슈 코멘트**로 남긴다 — 결정을 구두로 하지 않고 **해당 이슈**에 *선택지/근거/위험* 을
적고 **답을 단다**. 그러면 분모(회부 건수)와 ⓑ(재요청)가 로그에 남는다."*

🔴 **그런데 2026-08-29 실측: 세 저장소 이슈 18건 중 코멘트 3개이고 그마저 진행 보고였다.**
회부는 **대화 · PR 본문 18건 · `GAPS` 대장**에 흩어져 있었다 — **사전등록된 곳에는 0건.**
*수단은 적어뒀는데 아무것도 그걸 발화시키지 않는* 상태였고, 그게 이 저장소가 오늘 하루 종일
고친 결함의 형태다. 그래서 **행동을 바꾸기 전에 계기부터 단다.**

## 구현 — 결정당 이슈 하나 (`decision` 라벨)

규정은 *"해당 이슈에 적고 답을 단다"* 이지 *"기존 작업 이슈에"* 가 아니다.
**결정 자체가 이슈면 그게 해당 이슈**이고, 답과 재요청이 같은 스레드에 코멘트로 붙는다.

🔵 **이건 기준 완화가 아니라 강화다** — 판정은 *"수단이 달라졌는가"* 가 아니라
*"기준이 느슨해지는가"* 로 한다. 넷 다 **더 잡히는** 쪽이다:
분모는 더 잘 보이고 · ⓑ 는 그대로 · ⓒ 는 스레드가 통째로 남아 찾기 쉽고 · 작업량은 더 든다.

| 지표 | 어떻게 세나 |
|---|---|
| **분모** | `decision` 라벨 이슈 수 |
| **ⓐ** | 닫힌 회부 중 `needs-simpler` 가 **안 붙은** 비율 |
| **ⓑ** | `needs-simpler` 라벨이 붙은 회부 수 |

## 🔄 2026-09-01 — 수단을 **하나 더** 연다: **PR 본문의 `회부:` 표시** (`GAPS` R5-37 ⓑ)

🔴 **실측이 또 먼저다**: 결정당 이슈로 바꾼 뒤 **사흘에 회부 4건**이 쌓였다. 계기는 움직였다 —
그런데 **같은 기간의 PR 은 스무 건이 넘고, 그 안에서 오간 판단이 이슈로는 안 올라온다.**
이슈를 여는 값이 *"PR 안에서 이미 묻고 답한 것"* 에는 과했다. **분모가 여전히 실물보다 작다.**

**표시 하나로 센다** — PR 본문에 이 꼴의 줄을 둔다:

    회부: decision:input — 어휘를 A 로 갈까 B 로 갈까 → 답: A (채널: 대화)

🔴 **네 축을 정직하게 적는다 — 이번엔 넷이 다 강해지지 않는다.**

| | 이슈 → 이슈 **+** PR 표시 |
|---|---|
| **분모** | 이슈는 그대로 세고 PR 표시가 **더해진다** — 순증 |
| **ⓑ 재요청** | PR 표시에도 `needs-simpler` 를 적을 수 있다 — **동일** |
| **ⓒ *"그때 뭘 승인한 거지"*** | 🔴 **정정 2026-09-01(제3자 리뷰 P1)** — 처음엔 *"머지 커밋에 인용된다"* 고 적었는데 **사실이 아니다.** PR 본문은 **저장소 밖**이고 머지 뒤에도 고쳐지고 지워진다 — 이슈와 **같은 약점**이다. 리뷰 시점에 읽힌다는 것만 낫다. **그래서 이슈에 걸었던 다리를 PR 에도 건다**: 표시를 단 머지된 PR 이 `direction/`·`audit/` 에 인용되지 않으면 검사가 **실패**한다 |
| **작업량** | 🔴 **줄어든다.** 표시 한 줄이 이슈 하나보다 싸다 |

⚠️ **그러니 이건 "네 축 다 강해진다" 가 아니다.** 2026-08-29 의 변경과 다르다 — **그때는 넷 다
더 잡히는 쪽이었고, 이번은 셋만 그렇다.** 값이 싸진 것이 *기준 완화* 인지 *기록이 실제로
일어나게 만드는 것* 인지는 **눈금이 답한다**: 분모가 안 늘면 완화였고, 늘면 수단이 맞은 것이다.
🔴 **바꾸는 것은 수단이지 임계가 아니다** — ⓐ·ⓑ·ⓒ 의 판정선은 `direction/04` 그대로다.

🚫 **이슈 수단을 걷어내지 않는다.** PR 이 없는 회부(권한 없음 · 착수 전 취향)는 여전히 이슈다.
`AGENTS.md` §ASK FIRST 가 둘을 다 적는다 — **행동하는 자리에 안 적으면 발화하지 않는다.**

⚠️ **벽이 아니라 계기판이다.** 다만 **수단 자체가 없으면**(라벨 미설치) 실패로 본다 —
계기가 없는 것과 눈금이 0 인 것은 다르다.

읽기 전용이다.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPOS = ("standards", "workflows", "project-template", "divcal")

#: 🔴 **한 번에 가져오는 상한.** 200 이었는데 `standards` 가 **이미 머지된 PR 208건**이라
#: 넘어 있었다(제3자 리뷰 P2 · 2026-09-01). 상한에 **닿으면 실패로 본다** — 조용히 잘리면
#: `referrals_total` 이 줄어들고 **예전 관측이 사라진다.**
FETCH_LIMIT = 1000
LABEL = "decision"
RESIMPLE = "needs-simpler"

#: 회부의 **종류**. 12-Factor Agents Factor 7 계열의 HITL 분류를 그대로 쓴다 —
#: 셋은 **트리거도 대기 방식도 다르다**. 한 통에 담으면 긴급도가 안 보인다.
KINDS = {
    "decision:approval": "되돌리기 어려운 행동의 가부",
    "decision:input": "에이전트에게 없는 정보·취향",
    "decision:escalation": "막혔다 — 권한 없음 · 반복 실패",
}

#: 답이 **어느 경로로 왔는지**. 원문: *"Log everything — who approved what, when, via which channel."*
#: 🔴 대화로 온 답을 내가 옮겨 적으면, **내가 정확히 옮겼는지를 아무도 검증할 수 없다.**
#: 그 사실 자체를 남긴다.
CHANNEL_MARKER = "채널:"

#: 닫힌 회부는 **커밋된 기록**을 남겨야 한다. 이슈는 저장소 밖이라 diff 도 PR 리뷰도 없다 —
#: 코퍼스가 위키를 물리치며 든 이유가 그것이다(`decision-record-standard` §Publish).
#: RFC 는 이슈에 살아도 되지만 **ADR 은 커밋된다.** 이 검사가 그 다리다.
RECORD_DIRS = ("direction", "audit")

ROOT = Path(__file__).resolve().parent.parent

#: PR 본문에 회부를 남기는 표시(2026-09-01 · R5-37 ⓑ). 이슈 수단과 **병행**한다.
#: 형식: `회부: decision:input — <물음> → 답: <답> (채널: 대화)`
PR_MARKER = "회부:"

#: 답이 실제로 적혔는가. 🔴 **물음만 적힌 표시는 회부의 절반이다** — 종류·채널이 다 붙어 있어도
#: *결정이 기록된 것* 은 아니다(제3자 리뷰 P2 · 2026-09-01). 열린 PR 을 안 세는 이유가
#: *"답이 아직 없을 수 있어서"* 인데, 답 없는 표시를 완전한 것으로 세면 그 이유가 무너진다.
#: 이슈 쪽과 같은 처분을 한다 — **분모에는 넣고(회부는 일어났다) 따로 센다.**
#: 🔴 **화살표까지가 표시다.** `답:` 만 찾으면 **물음 안의 `답:` 도 통과한다** —
#: `회부: … 출력에 답: 접두사를 넣을까 (채널: 대화)` 가 *답이 적힌 회부* 로 세어졌다
#: (제3자 리뷰 3회차 · 2026-09-01). 종류 칸에서 물었던 것과 **같은 결함**이다.
ANSWER_MARKER = "→ 답:"


#: 🔴 **읽지 못한 원천.** `_json` 이 `None` 을 주면 호출부는 *빈 결과* 로 읽는데,
#: 그러면 **못 읽은 저장소가 회부 0건인 저장소와 구별이 안 된다** — fail-open 이다.
#: (제3자 리뷰 P2 · 2026-09-01. 이 저장소가 반복해서 무는 형태라 `AGENTS.md` 가 이름을 붙여뒀다.)
FETCH_FAILURES: list[str] = []


def _json(args: list[str]) -> object:
    label = " ".join(a for a in args if not a.startswith("-"))
    try:
        out = subprocess.run(args, capture_output=True, text=True, check=False)
    except OSError as err:
        # 🔴 `gh` 자체가 없으면 터진다 — 그건 *회부 0건* 이 아니라 **못 읽은 것**이다.
        FETCH_FAILURES.append(f"{label} ({err.__class__.__name__})")
        return None
    if out.returncode != 0:
        FETCH_FAILURES.append(f"{label} (exit {out.returncode})")
        return None
    try:
        return json.loads(out.stdout or "null")
    except json.JSONDecodeError:
        FETCH_FAILURES.append(f"{label} (JSON 이 아니다)")
        return None


def labels_installed(repo: str) -> bool:
    names = _json(["gh", "label", "list", "--repo", f"coolbress/{repo}",
                   "--limit", "60", "--json", "name"])
    if not isinstance(names, list):
        return False
    have = {n.get("name") for n in names}
    return LABEL in have and RESIMPLE in have


def referrals(repo: str) -> list[dict[str, Any]]:
    rows = _json(["gh", "issue", "list", "--repo", f"coolbress/{repo}", "--state", "all",
                  "--label", LABEL, "--limit", str(FETCH_LIMIT),
                  "--json", "number,title,state,labels,comments"])
    if not isinstance(rows, list):
        return []
    if len(rows) >= FETCH_LIMIT:
        FETCH_FAILURES.append(f"gh issue list {repo} (상한 {FETCH_LIMIT} 에 닿았다 — 잘렸을 수 있다)")
    return rows


def kind_of(issue: Mapping[str, Any]) -> str | None:
    for lbl in issue.get("labels") or []:
        name = lbl.get("name")
        if name in KINDS:
            return str(name)
    return None


def _has_channel_field(text: str) -> bool:
    """`채널:` 을 **줄 머리 칸**에서만 인정한다(굵게·목록 기호는 벗긴다).

    🔴 부분문자열로 보면 *"답변에는 채널: 항목도 적어야 합니다"* 같은 **진행 보고가 답이 된다**
    (제3자 리뷰 10회차 · 2026-09-01). PR 표시에 이미 적용한 규율을 이슈 쪽에도 맞춘다 —
    **필수 칸을 산문이 채울 수 있으면 그건 필수 칸이 아니다.**
    """
    for line in (text or "").splitlines():
        if line.strip().lstrip("-*# ").lstrip("*").startswith(CHANNEL_MARKER):
            return True
    return False


def has_channel(issue: Mapping[str, Any]) -> bool:
    return any(_has_channel_field(c.get("body") or "") for c in (issue.get("comments") or []))


#: 표시가 살 수 있는 자리. 🔴 **첫 `##` 제목 앞의 머리말**, 그리고 **열 0** 뿐이다.
#:
#: 🔬 **왜 이렇게 좁히나 — 손으로 마크다운 파서를 짓고 있었다** (2026-09-01).
#: 본문 전체를 훑으니 예시를 걸러내려고 펜스(백틱·물결·중첩·info string·목록 안·펜스 안 목록) ·
#: 들여쓴 코드 · HTML 주석을 차례로 때웠고 **제3자 리뷰가 그 가장자리로만 9건**을 물었다.
#: 가장자리는 끝이 없다(참조 링크 · 각주 · 표 안 코드 · `<pre>` …).
#:
#: 🔵 **자리를 좁히면 파싱이 사라진다.** 이건 이 세션에서 배운 것의 한 층 위다 —
#: *"필수 칸을 산문이 채울 수 있으면 그건 필수 칸이 아니다"* 의 형제:
#: **표시가 아무 데나 있을 수 있으면 아무 데나 파싱해야 한다.**
#:
#: ⚠️ **남는 위험은 적었다** — 머리말 안에 펜스로 예시를 넣으면 여전히 세어진다.
#: 그 자리는 **예시를 두는 곳이 아니라** 실질 위험이 낮고, 그 대가로 파싱 80여 줄이 사라졌다.
SECTION_START = "##"


def marker_lines(body: str) -> list[str]:
    """PR 본문 **머리말**에서 `회부:` 줄만 뽑는다. **순수 함수라 네트워크 없이 시험된다.**

    규칙은 둘뿐이다: **첫 `##` 제목 앞** · **열 0 에서 시작**.
    설명·예시는 제목 아래에 살므로 **저절로 걸러진다** — 펜스도 주석도 안 본다.
    """
    out: list[str] = []
    for raw in (body or "").splitlines():
        if raw.startswith(SECTION_START):
            break
        if raw.startswith(PR_MARKER):
            out.append(raw.strip())
    return out


def _run_length(text: str, at: int) -> int:
    """`at` 에서 시작하는 백틱 묶음의 길이."""
    n = 0
    while at + n < len(text) and text[at + n] == "`":
        n += 1
    return n


def _mask_code(text: str) -> str:
    """인라인 코드(`` ` `` 로 감싼 것)를 같은 길이의 `\x00` 으로 덮는다. **인덱스가 보존된다.**

    🔴 **구조를 찾을 때 산문을 봐야 한다.** `` `→ 답:` 표기를 쓸까 `` 처럼 **형식을 논하는 물음**이
    답 칸을 채웠다(제3자 리뷰 · 2026-09-01). 마스킹한 사본에서 자리를 찾고 **원본을 그 자리에서** 자른다.
    """
    out = list(text)
    text_len = len(text)
    i = 0
    while i < text_len:
        if text[i] != "`":
            i += 1
            continue
        # 🔴 **묶음 단위로 짝짓는다.** 위치 단위로 찾으면 **더 긴 묶음의 안쪽**을 닫는 것으로
        # 읽어 `` `foo`` `` 뒤가 안 가려진다(제3자 리뷰 · 2026-09-01). 여는 묶음과
        # **길이가 정확히 같은** 묶음만 닫는다.
        run = _run_length(text, i)
        close = -1
        j = i + run
        while j < text_len:
            if text[j] != "`":
                j += 1
                continue
            other = _run_length(text, j)
            if other == run:
                close = j
                break
            j += other
        if close < 0:
            # 🔴 **멈추지 않는다.** 짝 없는 묶음에서 `break` 하면 **그 뒤의 멀쩡한 인용이
            # 통째로 안 가려진다** — 뒤에 있는 `` ``→ 답:`` `` 이 답으로 세어졌다
            # (제3자 리뷰 · 2026-09-01). 그 묶음만 건너뛰고 계속 본다.
            i += run
            continue
        for k in range(i, close + run):
            out[k] = "\x00"
        i = close + run
    return "".join(out)


def parse_marker(line: str) -> dict[str, object]:
    """표시 줄을 **칸으로 쪼갠다.** 각 값은 자기 칸에서만 읽는다.

    형식: `회부: <종류> — <물음> → 답: <답> (채널: <어디> · needs-simpler)`
    끝의 **바깥 괄호**가 메타 칸이고, 채널과 재요청 표시는 `·` 로 나눈 **항목**에서만 읽는다.

    🔴 **왜 파싱하나 — 같은 결함을 다섯 번 물렸다** (종류 · 답 · 채널 · `needs-simpler` · 인용된 답):
    구조화된 줄을 부분문자열로 훑으면 **물음 텍스트가 필수 칸을 채운다.**
    **필수 칸을 산문이 채울 수 있으면 그건 필수 칸이 아니다.**
    """
    if PR_MARKER not in line:
        return {"kind": None, "answered": False, "channel": "", "resimple": False}
    body = line.split(PR_MARKER, 1)[1].strip()
    masked = _mask_code(body)
    meta = ""
    if masked.rstrip().endswith(")"):
        # 🔴 **바깥 괄호를 짝 맞춰 찾는다** — 채널에 괄호가 들어갈 수 있다.
        depth = 0
        for i in range(len(masked) - 1, -1, -1):
            if masked[i] == ")":
                depth += 1
            elif masked[i] == "(":
                depth -= 1
                if depth == 0:
                    meta, body = body[i + 1:-1], body[:i].rstrip()
                    masked = masked[:i].rstrip()
                    break
    head = body.split()
    at = masked.find(ANSWER_MARKER)      # 🔴 인용 밖에서만 찾는다
    answer = body[at + len(ANSWER_MARKER):] if at >= 0 else ""
    entries = [e.strip() for e in meta.split("·")]
    channel = ""
    for entry in entries:
        if entry.startswith(CHANNEL_MARKER):
            channel = entry[len(CHANNEL_MARKER):].strip()
    return {"kind": head[0] if head and head[0] in KINDS else None,
            "answered": at >= 0 and bool(answer.strip()),
            "channel": channel,
            "resimple": any(e == RESIMPLE for e in entries)}


def kind_of_line(line: str) -> str | None:
    """표시 줄의 **종류 칸**에서만 읽는다. 없으면 `None` — 긴급도를 못 가린다는 뜻이다.

    🔴 처음엔 **줄 전체**를 훑었다. 그러면 물음 안에 종류 이름이 있기만 해도 통과한다 —
    `회부: 이 요청을 decision:approval 로 분류할까 → 답: 예` 가 **종류가 붙은 표시**로 세어졌고
    `pr_marks_unkinded=0` 이라 경고도 안 났다(제3자 리뷰 P2 · 2026-09-01).
    **필수 칸을 물음 텍스트가 채울 수 있으면 그건 필수 칸이 아니다.**
    """
    kind = parse_marker(line)["kind"]
    return str(kind) if kind else None


def pr_marks(repo: str) -> list[tuple[str, int, str]]:
    """(repo, PR 번호, 표시 줄). 🔴 **머지된 PR 만** 센다 — 닫힌 채 버려진 PR 의
    본문은 결정이 아니다. 열린 PR 은 아직 답이 안 났을 수 있어 분모에 안 넣는다."""
    rows = _json(["gh", "pr", "list", "--repo", f"coolbress/{repo}", "--state", "merged",
                  "--limit", str(FETCH_LIMIT), "--json", "number,body"])
    if isinstance(rows, list) and len(rows) >= FETCH_LIMIT:
        FETCH_FAILURES.append(f"gh pr list {repo} (상한 {FETCH_LIMIT} 에 닿았다 — 잘렸을 수 있다)")
    out: list[tuple[str, int, str]] = []
    for pr in rows if isinstance(rows, list) else []:
        for line in marker_lines(str(pr.get("body") or "")):
            out.append((repo, int(pr.get("number") or 0), line))
    return out


def summarise_marks(marks: Sequence[tuple[str, int, str]]) -> dict[str, int]:
    """표시 줄만 따로 센다. 🔬 **음성 시험이 있다** — 종류가 없는 줄과 채널이 없는 줄을
    각각 세지 않으면 *"표시만 있으면 통과"* 가 되어 계기가 아무것도 안 재게 된다."""
    parsed = [parse_marker(ln) for _, _, ln in marks]
    counts = {"marks": len(marks),
              "unanswered": sum(1 for f in parsed if not f["answered"]),
              # 🔴 ⓐ 의 **분자에서 뺄 것**. 재요청과 답 없음을 따로 빼면 둘 다인 표시를 두 번 뺀다.
              "incomplete": sum(1 for f in parsed if f["resimple"] or not f["answered"]),
              "unkinded": sum(1 for f in parsed if f["kind"] is None),
              "no_channel": sum(1 for f in parsed if not f["channel"]),
              "resimple": sum(1 for f in parsed if f["resimple"])}
    for kind in KINDS:
        counts[kind] = sum(1 for f in parsed if f["kind"] == kind)
    return counts


def cited(repo: str, number: int, records: str) -> bool:
    """저장소까지 맞춰서 인용됐나. 🔴 **맨 `#224` 로는 안 된다** — 네 저장소가 번호를 공유해
    `workflows#224` 가 `standards#224` 인용으로 통과했다(제3자 리뷰 · 2026-09-01)."""
    # 🔴 **양쪽 경계를 다 본다.** 오른쪽만 막으면 `standards#224` 가 `standards#22` 의 인용으로
    # 통과하고, 왼쪽을 안 막으면 **다른 조직의 `otherorg/standards#22`** 가 우리 인용으로 통과한다
    # (제3자 리뷰 2회 · 2026-09-01). 둘 다 **다리가 조용히 초록이 되는** 쪽이다.
    # 🔬 형태마다 왼쪽 경계가 다르다. `repo#N` 은 앞이 **글자·슬래시면 안 되고**(다른 조직),
    # URL 은 앞이 **반드시 `https://github.com/`** 이어야 한다 — 호스트에 못 박지 않으면 `https://example.com/github.com/…` 도 통과한다 — URL 은 원래 앞이 `/` 라
    # 같은 경계를 쓰면 **실물 인용이 전부 끊긴다**(실측: `unbridged` 0 → 4).
    patterns = (
        rf"(?<![\w/-]){re.escape(repo)}#{number}(?!\d)",
        # 🔵 **우리 것을 완전한 형태로 적은 것은 받는다** — `coolbress/standards#22` 가
        # 왼쪽 경계에 걸려 거부됐다(제3자 리뷰 · 2026-09-01). 다른 조직은 여전히 막힌다.
        rf"(?<![\w/-])coolbress/{re.escape(repo)}#{number}(?!\d)",
        rf"https://github\.com/coolbress/{re.escape(repo)}/(?:pull|issues)/{number}(?!\d)",
    )
    return any(re.search(p, records) for p in patterns)


def committed_records(root: Path) -> str:
    """`direction/`·`audit/` 의 본문을 통째로 읽는다 — 이슈 번호가 인용됐는지 보려고."""
    chunks: list[str] = []
    for name in RECORD_DIRS:
        folder = root / name
        if folder.is_dir():
            chunks.extend(p.read_text(encoding="utf-8") for p in folder.rglob("*.md"))
    return "\n".join(chunks)


def summarise(rows: Sequence[tuple[str, Mapping[str, Any]]]) -> dict[str, int]:
    """세는 부분만 떼어낸다 — **네트워크 없이 시험할 수 있게.**

    🔬 처음엔 `main()` 안에 있었고 `(comments or 0) > 0` 이라 **빈 리스트일 때만 통과**했다.
    첫 코멘트가 달리자 `TypeError` 로 터졌다 — *실행되지 않은 경로의 초록은 증거가 아니다.*
    """
    closed = [i for _, i in rows if i.get("state") == "CLOSED"]
    resimple = [i for _, i in rows
                if any(lbl.get("name") == RESIMPLE for lbl in (i.get("labels") or []))]
    # 🔴 **코멘트가 있다 ≠ 답이 왔다.** 실측에서 그 코멘트들은 **진행 보고**였다(이 파일 상단).
    # 답은 *"누가 · 언제 · 어느 경로로"* 를 적은 것이라 **채널을 적은 코멘트**를 답으로 본다
    # (제3자 리뷰 8회차 · 2026-09-01). 진행 보고 하나로 ⓐ 의 성공이 되면 안 된다.
    answered = [i for i in closed if has_channel(i)]
    unkinded = [i for _, i in rows if kind_of(i) is None]
    no_channel = [i for i in closed if not has_channel(i)]
    # 🔴 **합집합으로 한 번만 뺀다.** 재요청이면서 답도 없는 회부를 따로 빼면 ⓐ 의 분자가
    # 음수로 간다 — 닫힌 회부 1건이 둘 다면 `1 - 1 - 1 = -1` 이라 **-100%** 가 찍혔다
    # (제3자 리뷰 3회차 · 2026-09-01). PR 쪽엔 이미 있던 처분을 이슈 쪽에도 한다.
    # 🔴 `answered` 와 **같은 정의**를 쓴다. 갈리면 진행 보고 하나로 ⓐ 의 성공이 된다.
    incomplete = [i for i in closed
                  if any(lbl.get("name") == RESIMPLE for lbl in (i.get("labels") or []))
                  or not has_channel(i)]
    counts = {"total": len(rows), "closed": len(closed), "resimple": len(resimple),
              "answered": len(answered), "unkinded": len(unkinded),
              "incomplete": len(incomplete), "no_channel": len(no_channel)}
    for kind in KINDS:
        counts[kind] = sum(1 for _, i in rows if kind_of(i) == kind)
    return counts


def unbridged(rows: Sequence[tuple[str, Mapping[str, Any]]], records: str) -> list[tuple[str, int]]:
    """닫혔는데 **커밋된 기록에 인용되지 않은** 회부.

    🔴 이게 이 도구의 핵심 다리다. RFC 는 이슈에 살아도 되지만 **결정은 커밋돼야** 한다 —
    안 그러면 *왜 그렇게 정했는지* 가 저장소 밖에만 남아 diff 도 PR 리뷰도 못 받는다.
    지금까지 그게 지켜진 것은 **우연이었고, 우연은 규율이 아니다.**
    """
    out: list[tuple[str, int]] = []
    for repo, issue in rows:
        if issue.get("state") != "CLOSED":
            continue
        number = int(issue.get("number") or 0)
        if not cited(repo, number, records):
            out.append((repo, number))
    return out


def unbridged_marks(marks: Sequence[tuple[str, int, str]], records: str) -> list[tuple[str, int]]:
    """표시를 단 **머지된 PR** 중 커밋된 기록에 인용되지 않은 것.

    🔴 **PR 본문은 저장소 밖이다.** 머지 뒤에도 고쳐지고 지워지며 **커밋에 안 들어간다** —
    처음엔 이 도구가 *"PR 본문은 머지 커밋에 인용된다"* 고 적었는데 **그건 사실이 아니었다**
    (제3자 리뷰 P1 · 2026-09-01). 이슈에 걸었던 다리를 **그대로** 건다:
    RFC 는 밖에 살아도 되지만 **결정은 커밋된다.**

    🔴 **다만 이 다리가 지키지 못하는 것을 분명히 한다** (제3자 리뷰 5회차 · 2026-09-01):
    이 함수는 **지금 본문에 남아 있는 표시**만 본다. 머지 뒤에 본문에서 표시를 지우면
    `pr_marks` 에서 사라지고 **`referrals_total` 이 조용히 줄어드는데, 여기서는 안 걸린다**
    (인용은 남아 있고 표시만 없어지므로 *못 이은 것* 으로도 안 잡힌다).
    **이 계기의 원천은 가변이다** — `GAPS` R5-47 로 등재했다. 지금 고치지 않는 이유는
    지속화 수단(커밋 메시지 · 별도 원장)이 **수단 선택**이라 눈금이 몇 건 쌓인 뒤에 정해야 하기 때문이다.
    """
    seen: set[tuple[str, int]] = set()
    for repo, number, _ in marks:
        if not cited(repo, number, records):
            seen.add((repo, number))
    return sorted(seen)


def rates(counts: Mapping[str, int], mcounts: Mapping[str, int]) -> dict[str, int]:
    """ⓐ·ⓑ 를 **두 수단을 합쳐** 낸다. 순수 함수라 네트워크 없이 시험된다.

    🔴 세 번을 틀린 자리다(제3자 리뷰 1·2·3회차 · 2026-09-01):
    ⓑ 가 이슈만 셌고 → ⓐ 도 이슈만 셌고 → **기록이 반쪽인 회부가 ⓐ 의 *성공* 으로** 세어졌다.
    분모만 올리고 분자에서 안 빠지면 **불완전한 기록이 비율을 좋게 만든다.**
    이슈 쪽도 같다 — *닫혔는데 답 코멘트가 없는 회부* 가 그동안 성공이었다(지금 0건이라 안 보였다).
    """
    denom = counts["closed"] + mcounts["marks"]
    numer = denom - counts["incomplete"] - mcounts["incomplete"]
    return {"a_denom": denom, "a_numer": numer,
            "b_total": counts["resimple"] + mcounts["resimple"]}


def main() -> int:
    missing = [r for r in REPOS if not labels_installed(r)]
    rows: list[tuple[str, dict[str, object]]] = []
    for repo in REPOS:
        rows.extend((repo, issue) for issue in referrals(repo))

    print("요구 ③ — 회부가 로그에 남는가")
    if missing:
        print(f"  🔴 수단이 설치 안 된 저장소: {', '.join(missing)} "
              f"(`{LABEL}`·`{RESIMPLE}` 라벨이 있어야 센다)")
    else:
        print(f"  ✅ 수단 설치됨 — 네 저장소 모두 `{LABEL}`·`{RESIMPLE}` 라벨이 있다")

    marks: list[tuple[str, int, str]] = []
    for repo in REPOS:
        marks.extend(pr_marks(repo))
    mcounts = summarise_marks(marks)

    counts = summarise(rows)
    total, n_closed = counts["total"], counts["closed"]
    n_resimple, n_answered = counts["resimple"], counts["answered"]
    records = committed_records(ROOT)
    gaps = unbridged(rows, records)
    mark_gaps = unbridged_marks(marks, records)

    print(f"\n  분모 — 회부된 결정 {total}건 (열림 {total - n_closed} · 닫힘 {n_closed})")
    for repo, issue in rows[:8]:
        mark = "✅" if issue.get("state") == "CLOSED" else "⬜"
        print(f"     {mark} {repo}#{issue.get('number')} {str(issue.get('title'))[:52]}")
    if total > 8:
        print(f"     … 외 {total - 8}건")

    if total or mcounts["marks"]:
        # 🔴 **이슈가 0건이어도 PR 표시가 있으면 낸다.** 이슈 수로만 게이트하면
        # `referrals_total=1` 인데 *"회부가 0건이다"* 라고 말한다(제3자 리뷰 3회차 · 2026-09-01).
        # 🔴 닫힌 게 없을 때 `0%` 로 찍으면 **나쁜 결과처럼 읽힌다.** 분모가 0 인 것과 다르다.
        # 🔴 ⓐ 도 **두 수단을 합쳐서** 낸다. 이슈만으로 내면 PR 표시의 재요청이 분모에서 빠져
        # 1/1(100%) 로 읽히는데 실제로는 1/2(50%) 다(제3자 리뷰 P2 · 2026-09-01).
        # 🔴 **기록이 반쪽인 회부는 성공이 아니다.** 답이 안 적힌 표시가 분모만 올리고 분자에서
        # 안 빠지면 ⓐ 가 1/1(100%) 로 읽힌다(제3자 리뷰 P2 · 2026-09-01). 이슈 쪽도 같다 —
        # 닫혔는데 답 코멘트가 없는 회부가 그동안 성공으로 세어지고 있었다(지금은 0건이라 안 보였다).
        r = rates(counts, mcounts)
        a_denom, a_numer = r["a_denom"], r["a_numer"]
        if a_denom:
            rate = f"{100 * a_numer / a_denom:.0f}%"
        else:
            rate = "판정 불가 — 아직 닫힌 회부가 없다"
        print(f"\n  ⓐ 되묻지 않고 판단 — **{a_denom}건 중 {a_numer}건 ({rate})** "
              f"(닫힌 이슈 {n_closed} + PR 표시 {mcounts['marks']})")
        # 🔴 ⓑ 는 **두 수단을 합쳐서** 낸다. PR 표시의 재요청을 빼면 그 PR 은 분모(`referrals_total`)를
        # 올리면서 ⓑ 에서는 사라져 **사전등록된 지표가 조용히 초록**이 된다(제3자 리뷰 P1 · 2026-09-01).
        print(f"  ⓑ 재요청(`{RESIMPLE}`) — **{r['b_total']}건** "
              f"(이슈 {n_resimple} + PR 표시 {mcounts['resimple']})")
        print(f"     ⚠️ 닫혔는데 답 코멘트가 없는 회부 {n_closed - n_answered}건")

        print("\n  종류 — 셋은 트리거도 대기 방식도 다르다")
        for kind, why in KINDS.items():
            # 🔴 이슈만 찍으면 **이슈 0건 + PR 표시 1건일 때 전부 0** 으로 보인다
            # (제3자 리뷰 8회차 · 2026-09-01). 두 수단을 합쳐 찍는다.
            print(f"     {counts[kind] + mcounts[kind]:2d}건  {kind:22s} {why}")
        if counts["unkinded"]:
            print(f"     🔴 종류가 안 붙은 회부 {counts['unkinded']}건 — "
                  "긴급도를 못 가린다")

        print(f"\n  다리 — 닫힌 회부가 커밋된 기록({'·'.join(RECORD_DIRS)}/)에 남았나")
        for repo, number in gaps:
            print(f"     🔴 {repo}#{number} — 결정이 **이슈 안에만** 있다")
        if not gaps and n_closed:
            print("     ✅ 닫힌 회부 전부 커밋된 기록에 인용돼 있다")
        if counts["no_channel"]:
            print(f"     🔶 답의 출처 채널(`{CHANNEL_MARKER}`)이 없는 회부 {counts['no_channel']}건")
    else:
        print("\n  ⚠️ 회부가 0건이다 — 계기는 달렸고 **눈금이 아직 안 움직였다.**")
        print("     회부 자체가 없었는지, 아니면 다른 데(대화·PR 본문)에 남겼는지는 이 도구가 못 가린다.")

    print(f"\n  PR 본문 표시(`{PR_MARKER}`) — 2026-09-01 에 연 두 번째 수단")
    if marks:
        for repo, number, line in marks[:8]:
            flag = "🔴" if kind_of_line(line) is None else "  "
            print(f"     {flag} {repo}#{number} {line[:76]}")
        if len(marks) > 8:
            print(f"     … 외 {len(marks) - 8}건")
        if mcounts["unkinded"]:
            print(f"     🔴 종류가 없는 표시 {mcounts['unkinded']}건 — 긴급도를 못 가린다")
        if mcounts["unanswered"]:
            print(f"     🔴 답(`{ANSWER_MARKER}`)이 없는 표시 {mcounts['unanswered']}건 — "
                  "물음만 적힌 것은 회부의 절반이다")
        for repo, number in mark_gaps:
            print(f"     🔴 {repo}#{number} — 표시가 **PR 본문에만** 있다 "
                  "(본문은 머지 뒤에도 고쳐진다 · 커밋된 기록에 인용해라)")
        if mcounts["no_channel"]:
            print(f"     🔶 채널(`{CHANNEL_MARKER}`)이 없는 표시 {mcounts['no_channel']}건")
    else:
        print("     ⚠️ 아직 0건 — 수단을 연 것과 쓰이는 것은 다른 문장이다")

    grand = total + mcounts["marks"]
    print(f"\n  분모 합 — 이슈 {total} + PR 표시 {mcounts['marks']} = **{grand}건**")
    print("     🔴 이 수가 안 늘면 수단 변경이 아니라 **완화**였다는 뜻이다 "
          "(2026-09-01 에 연 눈금 · 판정선은 안 긋는다)")

    print(f"\nMETRIC referrals={total} closed={n_closed} resimple={n_resimple} "
          f"unkinded={counts['unkinded']} unbridged={len(gaps)} "
          f"no_channel={counts['no_channel']} labels_missing={len(missing)} "
          f"pr_marks={mcounts['marks']} pr_marks_unkinded={mcounts['unkinded']} "
          f"pr_resimple={mcounts['resimple']} pr_unanswered={mcounts['unanswered']} "
          f"pr_unbridged={len(mark_gaps)} pr_no_channel={mcounts['no_channel']} "
          f"resimple_total={rates(counts, mcounts)['b_total']} "
          f"referrals_total={grand} unreadable_sources={len(FETCH_FAILURES)}")
    if FETCH_FAILURES:
        for source in FETCH_FAILURES[:6]:
            print(f"  🔴 원천을 못 읽었다: {source}")
        print("RESULT FAIL — 못 읽은 원천이 있다. **0 으로 읽으면 fail-open 이다** "
              "(못 잰 것과 눈금이 0 인 것은 다르다)")
        return 1
    if missing:
        print("RESULT FAIL — 수단이 설치되지 않았다. 계기가 없는 것과 눈금이 0 인 것은 다르다")
        return 1
    if gaps or mark_gaps:
        print("RESULT FAIL — 회부의 결정이 커밋된 기록에 없다. "
              "RFC 는 이슈·PR 본문에 살아도 되지만 **결정은 커밋된다** "
              "(둘 다 저장소 밖이라 나중에 고쳐진다)")
        return 1
    print("RESULT INFO — 계기판이다. 판정은 2주 관측 뒤에 한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
