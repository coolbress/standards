// 인수 검사 — 서버를 임시 포트에 띄우고 / 가 200 + 제목을 반환하는지 확인한다.
// exit 0 = 통과 · exit 1 = 실패
import { createServer } from "node:http";
import { handler } from "./app.mjs";

const srv = createServer(handler);
await new Promise((r) => srv.listen(0, r));
const { port } = srv.address();

let ok = false;
try {
  const res = await fetch(`http://127.0.0.1:${port}/`);
  const body = await res.text();
  ok = res.status === 200 && body.includes("<h1>goppi-trial-web</h1>");
  console.log(`status=${res.status} title=${body.includes("<h1>goppi-trial-web</h1>")}`);
} catch (e) {
  console.error(`요청 실패: ${e.message}`);
} finally {
  srv.close();
}
process.exit(ok ? 0 : 1);
