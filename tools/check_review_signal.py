#!/usr/bin/env python3
"""제3자 리뷰가 **신호를 내는가, 소음을 내는가** — 계기다. 판정선은 긋지 않는다.

🔴 **왜 이게 필요한가.** `third-party / review` 벽은 *"제3자가 이 커밋을 봤다"* 까지만
보증한다. 그런데 등재된 실증이 **그 다음이 새는 곳**이라고 말한다:

- `IPW-020`(MSR '26 · PR 3,109 · 에이전트 13종) — **13종 중 12종이 signal ratio 60% 미만** ·
  닫힌 CRA-only PR 의 **60.2%가 0~30% 소음대**
- `IPW-019`(AI PR 33,596) — **61.38%가 리뷰 기록 자체가 없다**

⚠️ **그래서 우리 것도 재야 한다.** 남의 저장소가 시끄럽다고 우리 것이 시끄러운 건 아니고,
반대도 마찬가지다. **재기 전에는 모른다.**

🔴 **판정선을 상상해서 박지 않는다.** `R5-2` 에서 배운 것이 그것이다 —
*"θ 는 **건강한 실행**에서 읽고 시험 데이터에서 읽지 않는다."* 지금은 표본이 없다.
**쌓이면 그때 긋는다.** 다시 볼 조건은 아래 `ENOUGH` 에 적었다.

## 못 재는 것 (명시한다)

- 🔴 ***"읽혔는가"* 는 못 잰다.** 아래 `touched_after` 는 **댓글이 달린 파일이 그 뒤 커밋에서
  바뀌었나** 일 뿐이다 — 우연히 같이 바뀌었을 수도, 읽고 무시했을 수도 있다. **대리지표다.**
- **finding 이 옳았는지**도 못 잰다. 그건 판단이고 사람이 한다.
- 코드 검토와 보안 검토를 **작성자로는 못 가른다**(같은 봇 · `openai/codex#38110`).

네트워크를 탄다 — **CI 밖**이다.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter
from typing import Any

#: 제3자 리뷰어의 로그인. 벽(`pr-review.yml`)의 기본값과 **같은 이름**이어야 한다.
REVIEWER = "chatgpt-codex-connector[bot]"

#: 재는 저장소. 소유자 접두를 붙인다 — 안 붙이면 404 가 나고 조용히 0 이 된다(실측 사고).
REPOS = ("coolbress/standards", "coolbress/workflows")

#: 최근 몇 개의 PR 을 보나.
RECENT = 30

#: 🔴 **이만큼 쌓이면 판정선을 논의한다.** 그 전에는 숫자를 보고 결정하지 않는다.
ENOUGH = 20

#: 코덱스는 심각도를 배지 이미지로 박는다: `![P1 Badge](https://img.shields.io/badge/P1-…)`
SEVERITY = re.compile(r"!\[(P\d) Badge\]")


def _env() -> dict[str, str]:
    """`gh` 가 에이전트 토큰을 쓰게 한다."""
    env = dict(os.environ)
    env.pop("GITHUB_TOKEN", None)
    return env


def gh(path: str) -> Any:
    """`gh api` 한 번. 실패는 None — 조용히 넘기지 않고 부르는 쪽이 센다."""
    # 억제를 안 단다 — `ruff.toml` 이 S603·S607 을 이미 ignore 하고,
    # 안 걸리는 것에 `noqa` 를 달면 `RUF100` 이 반대로 터진다(실측).
    r = subprocess.run(
        ["gh", "api", "--paginate", path],
        capture_output=True,
        text=True,
        check=False,
        env=_env(),
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def severity_of(body: str) -> str:
    """댓글 본문에서 심각도를 읽는다. 배지가 없으면 `"?"`.

    🔴 **본문 전체를 안 본다** — 첫 배지만 센다. 한 댓글에 배지가 둘이면 앞엣것이 그 댓글의 것이다.
    """
    m = SEVERITY.search(body or "")
    return m.group(1) if m else "?"


def is_reviewer(login: str) -> bool:
    """제3자 리뷰어가 쓴 것인가. 대소문자는 무시한다(실측: 표기가 흔들린다)."""
    return (login or "").lower() == REVIEWER.lower()


def tally(comments: list[dict[str, Any]], touched: dict[str, set[str]]) -> Counter[str]:
    """리뷰 댓글을 심각도별로 세고, **그 뒤에 그 파일이 바뀌었는지**를 같이 센다.

    `touched[commit_of(c)]` 는 그 커밋 이후 PR 안에서 바뀐 파일 경로들이다.
    순수 함수다 — 네트워크를 안 탄다.

    🔴 **키가 `commit_of` 여야 한다.** 지도는 `original_commit_id` 로 만들어놓고 조회를
    `commit_id` 로 했더니 **전부 빗나가 `after` 가 늘 빈 집합**이었다 — 대리지표가 조용히
    낮아진다. 🔬 **같은 뿌리에 네 번째로 물린 자리다**(벽 · 지도 · 여기): *한 곳을 고칠 때
    **같은 값을 읽는 다른 줄** 을 안 봤다.*
    """
    out: Counter[str] = Counter()
    for c in comments:
        if not is_reviewer((c.get("user") or {}).get("login") or ""):
            continue
        sev = severity_of(c.get("body") or "")
        out["findings"] += 1
        out[f"sev_{sev}"] += 1
        after = touched.get(commit_of(c), set())
        if (c.get("path") or "") in after:
            out["touched_after"] += 1
            out[f"touched_{sev}"] += 1
    return out


def commit_of(comment: dict[str, Any]) -> str:
    """댓글이 **처음 달린** 커밋.

    🔴 `commit_id` 를 쓰면 안 된다 — PR 에 새 커밋이 붙을 때마다 **GitHub 이 그 값을 현재
    head 로 옮긴다**(실측 2026-09-01 · `workflows#71` 이 같은 이유로 벽을 고쳤다).
    그러면 옛 지적이 전부 head 것으로 보여 **대리지표가 통째로 어긋난다.**
    """
    return str(comment.get("original_commit_id") or comment.get("commit_id") or "")


def merged_unaddressed(pr: dict[str, Any], comments: list[dict[str, Any]]) -> int:
    """머지된 PR 의 **마지막 커밋에 달린 지적** 수 — 정의상 아무도 안 고친 것이다.

    🔬 **오탐이 0인 계기다**: 그 뒤 커밋이 없으므로 *구조적으로* 안 고쳐졌다. 판단이 안 들어간다.
    ⚠️ **"무시했다" 가 아니라 "처분 기록이 없다" 이다** — 지적이 틀렸거나 범위 밖일 수 있는데
    **그걸 적을 자리가 아직 없다.** 그 자리를 만드는 것이 `GAPS` R5-40 ⓒ **리뷰 처분 계약**이고,
    이 눈금이 그 층이 기다리던 재료다.
    🚫 **벽이 아니다.** *findings 로 안 막는다* 는 `IPW-020`(13종 중 12종이 signal ratio 60% 미만)으로
    사전등록된 결정이다 — 이건 **보이게만** 한다.
    """
    if not pr.get("merged_at"):
        return 0
    head = (pr.get("head") or {}).get("sha") or ""
    return sum(1 for c in comments if head and commit_of(c) == head)


def _touched_map(repo: str, comments: list[dict[str, Any]],
                 head: str) -> tuple[dict[str, set[str]], int]:
    """(댓글이 달린 커밋 → 그 뒤로 바뀐 파일 집합, **못 읽은 비교 수**). 커밋당 한 번만 묻는다.

    🔴 **비교를 못 읽은 것을 *바뀐 파일 없음* 으로 읽지 않는다.** 그러면 `touched_after` 가
    조용히 낮아지고 `RESULT INFO` 로 끝난다 — 같은 fail-open 이 이 도구에서만 **세 번째**다
    (PR 목록 · 댓글 · 여기. 제3자 리뷰 · 2026-09-02).
    """
    out: dict[str, set[str]] = {}
    bad = 0
    for base in {commit_of(c) for c in comments if commit_of(c)}:
        if base == head:
            out[base] = set()
            continue
        cmp_ = gh(f"repos/{repo}/compare/{base}...{head}")
        if not isinstance(cmp_, dict):
            print(f"     🔴 {repo}: {base[:8]}…{head[:8]} 비교를 못 읽었다")
            bad += 1
            continue
        files = cmp_.get("files") or []
        out[base] = {f.get("filename") or "" for f in files}
    return out, bad


def scan(repo: str) -> tuple[Counter[str], int, int]:
    """저장소 하나. (합계, 리뷰가 붙은 PR 수, 본 PR 수).

    합계에 `merged_open`(미처분 지적 수)과 `merged_open_prs`(그런 PR 수)가 같이 담긴다.
    """
    prs = gh(f"repos/{repo}/pulls?state=all&per_page={RECENT}")
    if not isinstance(prs, list):
        print(f"  🔴 {repo}: PR 을 못 읽었다(권한이나 이름을 확인해라)")
        c: Counter[str] = Counter()
        c["unreadable"] += 1
        return c, 0, 0

    total: Counter[str] = Counter()
    reviewed = 0
    for pr in prs[:RECENT]:
        num, head = pr.get("number"), (pr.get("head") or {}).get("sha") or ""
        cs = gh(f"repos/{repo}/pulls/{num}/comments")
        if not isinstance(cs, list):
            # 🔴 **못 읽은 PR 을 *댓글 0건* 으로 읽지 않는다.** 그러면 `merged_open` 이
            # 조용히 줄고 `RESULT INFO` 로 끝난다 — 이 저장소의 대표 fail-open 이고
            # `check_decision_referrals` 에서 이미 한 번 고친 형태다(제3자 리뷰 · 2026-09-02).
            print(f"     🔴 {repo}#{num}: 댓글을 못 읽었다")
            total["unreadable"] += 1
            continue
        mine = [c for c in cs if is_reviewer((c.get("user") or {}).get("login") or "")]
        if not mine:
            continue
        reviewed += 1
        touched, bad = _touched_map(repo, mine, head)
        total["unreadable"] += bad
        total.update(tally(mine, touched))
        open_n = merged_unaddressed(pr, mine)
        if open_n:
            total["merged_open"] += open_n
            total["merged_open_prs"] += 1
            print(f"     🔴 {repo}#{num} — 머지 head 에 지적 {open_n}건(처분 기록 없음)")
    return total, reviewed, len(prs[:RECENT])


def main() -> int:
    print("제3자 리뷰가 신호를 내는가 — 계기 (판정 아님)\n")
    grand: Counter[str] = Counter()
    prs_reviewed = prs_seen = 0
    for repo in REPOS:
        t, reviewed, seen = scan(repo)
        grand.update(t)
        prs_reviewed += reviewed
        prs_seen += seen
        sev = " ".join(f"{k[4:]}={v}" for k, v in sorted(t.items()) if k.startswith("sev_"))
        print(f"  {repo:26s} PR {seen:3d} · 리뷰 붙은 PR {reviewed:2d} · "
              f"finding {t['findings']:3d}  {sev}")

    f = grand["findings"]
    ta = grand["touched_after"]
    print(f"\nMETRIC prs_seen={prs_seen} prs_reviewed={prs_reviewed} findings={f} "
          f"touched_after={ta} unreadable={grand['unreadable']} "
          f"merged_open={grand['merged_open']} "
          f"merged_open_prs={grand['merged_open_prs']} " + " ".join(
              f"{k}={v}" for k, v in sorted(grand.items()) if k.startswith("sev_")))
    if f:
        print(f"  대리지표: finding 이 달린 파일이 그 뒤 바뀐 비율 = {ta}/{f} = {ta / f:.0%}")
    print(f"  PR 당 finding = {f / prs_reviewed:.1f}" if prs_reviewed else "  아직 표본이 없다")

    if grand["unreadable"]:
        print(f"\n  🔴 **못 읽은 원천 {grand['unreadable']}건** — 세다 만 수치다.")

    if grand["merged_open"]:
        print(f"\n  🔴 **처분 기록 없이 머지된 지적 {grand['merged_open']}건** "
              f"(PR {grand['merged_open_prs']}개) — 머지 head 에 달려 **그 뒤 커밋이 없다.**")
        print("     ⚠️ *무시했다* 가 아니라 ***적을 자리가 없다*** 이다 — "
              "그 자리가 `GAPS` R5-40 ⓒ **리뷰 처분 계약**이고, 이 수가 그 층의 재료다.")
        print("     🚫 벽이 아니다 — *findings 로 안 막는다* 는 `IPW-020` 으로 사전등록된 결정이다.")

    print("\n  ⚠️ **읽혔는지는 못 잰다** — 위 비율은 *파일이 바뀌었나* 일 뿐이다(대리지표).")
    print("  ⚠️ 코드 검토와 보안 검토를 **작성자로는 못 가른다**(openai/codex#38110).")
    if prs_reviewed < ENOUGH:
        print(f"  🔴 표본 {prs_reviewed} < {ENOUGH} — **판정선을 긋지 않는다.** "
              "쌓이면 그때 논의한다(R5-2 에서 배운 것).")
    else:
        print(f"  🔵 표본이 {ENOUGH} 를 넘었다 — **이제 문턱을 논의할 수 있다.**")
    if grand["unreadable"]:
        print("RESULT FAIL — **못 읽은 것을 0 으로 읽지 않는다.** "
              "판정선은 여전히 안 긋지만, *세다 만 수치* 는 계기가 아니다")
        return 1
    print("RESULT INFO — 계기판이다. 판정선은 긋지 않았다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
