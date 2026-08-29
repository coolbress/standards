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

    print(f"\nMETRIC referrals={total} closed={n_closed} resimple={n_resimple} "
          f"unkinded={counts['unkinded']} unbridged={len(gaps)} "
          f"no_channel={counts['no_channel']} labels_missing={len(missing)}")
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
