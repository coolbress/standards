# goppi-trial-web

goppi 외부 확증시험(PRD §8 성공 기준 ④)용 그린필드 미니 웹 앱. 의존성 없음.

- 실행: `node server.mjs` → http://localhost:3000
- 인수 검사: `node check.mjs` (exit 0 = 통과)

이 저장소는 goppi 하네스가 **저장소 밖에서** 거짓 완료·낡은 증거·검사 바꿔치기·계약 삭제를
차단하는지 확인하는 시험대다. 계약은 `ACCEPTANCE.json`(소유자 고정), 하네스는 `/plugin`으로 설치.
