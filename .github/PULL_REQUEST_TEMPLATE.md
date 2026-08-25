<!-- 제목은 Conventional Commits 로 쓴다: type(scope): 요약
     이 템플릿의 형태는 census 근거다 — PR 템플릿 중앙값 3절 · 빈 체크리스트 62%(중앙값 5항목) ·
     인라인 HTML 주석 가이드 70% · "type of change" 는 11.5%뿐이라 CC 를 쓰는 저장소는 뺀다.
     (corpus/aspects/24-governance-collaboration-compliance/issue-pr-writing-conventions.md) -->

## 무엇을 왜

<!-- 결론부터. 무엇을 바꿨고 왜 필요했는지.
     주장을 고쳤다면 "무엇이 틀렸는지" 를 먼저 적는다. -->

## 어떻게 확인했나

<!-- 돌린 검사와 결과. 실측이면 명령과 출력을 붙인다.
     "확인했다" 가 아니라 무엇을 보고 그렇게 판단했는지. -->

## 확인

- [ ] `python3 tools/validate_corpus.py` 통과
- [ ] `node tools/build-routes.mjs --check` 최신
- [ ] `python3 -m unittest discover -s tools -p 'test_*.py'` 통과
- [ ] 주장을 바꿨다면 **1차 출처를 직접 열었다** (요약·2차 인용으로 대체하지 않았다)
- [ ] 수정이 **전파된 곳까지** 갔다 (같은 수치·문구를 `grep` 전수)
