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
| **ⓒ *"그때 뭘 승인한 거지"*** | PR 본문은 **리뷰를 거치고 머지 커밋에 인용된다** — 이슈보다 찾기 쉽다 |
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
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPOS = ("standards", "workflows", "project-template", "divcal")
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


def _json(args: list[str]) -> object:
    out = subprocess.run(args, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout or "null")
    except json.JSONDecodeError:
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
                  "--label", LABEL, "--limit", "200",
                  "--json", "number,title,state,labels,comments"])
    return rows if isinstance(rows, list) else []


def kind_of(issue: Mapping[str, Any]) -> str | None:
    for lbl in issue.get("labels") or []:
        name = lbl.get("name")
        if name in KINDS:
            return str(name)
    return None


def has_channel(issue: Mapping[str, Any]) -> bool:
    return any(CHANNEL_MARKER in (c.get("body") or "") for c in (issue.get("comments") or []))


def marker_lines(body: str) -> list[str]:
    """PR 본문에서 `회부:` 줄만 뽑는다. **순수 함수라 네트워크 없이 시험된다.**

    🔴 **코드펜스 안은 안 센다.** 첫 실물 시험에서 이 도구가 **자기 사용법 예시를 회부로 셌다**
    (`회부: decision:input — <물음> → 답: <답>`). 형식을 설명하는 PR 마다 분모가 부풀면
    `referrals_total` 이 *행동* 이 아니라 *문서를 몇 번 썼나* 를 재게 된다 —
    **계기가 재겠다던 것을 안 재는 것**이다. 예시는 펜스 안에, 진짜 회부는 본문에 쓴다.
    """
    out: list[str] = []
    fenced = False
    for line in (body or "").splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced and PR_MARKER in line:
            out.append(line.strip())
    return out


def kind_of_line(line: str) -> str | None:
    """표시 줄이 스스로 밝힌 회부 종류. 없으면 `None` — 긴급도를 못 가린다는 뜻이다."""
    for kind in KINDS:
        if kind in line:
            return kind
    return None


def pr_marks(repo: str) -> list[tuple[str, int, str]]:
    """(repo, PR 번호, 표시 줄). 🔴 **머지된 PR 만** 센다 — 닫힌 채 버려진 PR 의
    본문은 결정이 아니다. 열린 PR 은 아직 답이 안 났을 수 있어 분모에 안 넣는다."""
    rows = _json(["gh", "pr", "list", "--repo", f"coolbress/{repo}", "--state", "merged",
                  "--limit", "200", "--json", "number,body"])
    out: list[tuple[str, int, str]] = []
    for pr in rows if isinstance(rows, list) else []:
        for line in marker_lines(str(pr.get("body") or "")):
            out.append((repo, int(pr.get("number") or 0), line))
    return out


def summarise_marks(marks: Sequence[tuple[str, int, str]]) -> dict[str, int]:
    """표시 줄만 따로 센다. 🔬 **음성 시험이 있다** — 종류가 없는 줄과 채널이 없는 줄을
    각각 세지 않으면 *"표시만 있으면 통과"* 가 되어 계기가 아무것도 안 재게 된다."""
    counts = {"marks": len(marks),
              "unkinded": sum(1 for _, _, ln in marks if kind_of_line(ln) is None),
              "no_channel": sum(1 for _, _, ln in marks if CHANNEL_MARKER not in ln),
              "resimple": sum(1 for _, _, ln in marks if RESIMPLE in ln)}
    for kind in KINDS:
        counts[kind] = sum(1 for _, _, ln in marks if kind_of_line(ln) == kind)
    return counts


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
    answered = [i for i in closed if len(i.get("comments") or [])]
    unkinded = [i for _, i in rows if kind_of(i) is None]
    no_channel = [i for i in closed if not has_channel(i)]
    counts = {"total": len(rows), "closed": len(closed), "resimple": len(resimple),
              "answered": len(answered), "unkinded": len(unkinded),
              "no_channel": len(no_channel)}
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
        number = issue.get("number")
        if f"#{number}" not in records and f"issues/{number}" not in records:
            out.append((repo, int(number or 0)))
    return out


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
    gaps = unbridged(rows, committed_records(ROOT))

    print(f"\n  분모 — 회부된 결정 {total}건 (열림 {total - n_closed} · 닫힘 {n_closed})")
    for repo, issue in rows[:8]:
        mark = "✅" if issue.get("state") == "CLOSED" else "⬜"
        print(f"     {mark} {repo}#{issue.get('number')} {str(issue.get('title'))[:52]}")
    if total > 8:
        print(f"     … 외 {total - 8}건")

    if total:
        # 🔴 닫힌 게 없을 때 `0%` 로 찍으면 **나쁜 결과처럼 읽힌다.** 분모가 0 인 것과 다르다.
        if n_closed:
            rate = f"{100 * (n_closed - n_resimple) / n_closed:.0f}%"
        else:
            rate = "판정 불가 — 아직 닫힌 회부가 없다"
        print(f"\n  ⓐ 되묻지 않고 판단 — 닫힌 {n_closed}건 중 {n_closed - n_resimple}건 ({rate})")
        print(f"  ⓑ 재요청(`{RESIMPLE}`) — {n_resimple}건")
        print(f"     ⚠️ 닫혔는데 답 코멘트가 없는 회부 {n_closed - n_answered}건")

        print("\n  종류 — 셋은 트리거도 대기 방식도 다르다")
        for kind, why in KINDS.items():
            print(f"     {counts[kind]:2d}건  {kind:22s} {why}")
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
          f"referrals_total={grand}")
    if missing:
        print("RESULT FAIL — 수단이 설치되지 않았다. 계기가 없는 것과 눈금이 0 인 것은 다르다")
        return 1
    if gaps:
        print("RESULT FAIL — 닫힌 회부의 결정이 커밋된 기록에 없다. "
              "RFC 는 이슈에 살아도 되지만 **결정은 커밋된다**")
        return 1
    print("RESULT INFO — 계기판이다. 판정은 2주 관측 뒤에 한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
