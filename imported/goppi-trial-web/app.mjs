// goppi-trial-web — 확증시험용 그린필드 미니 웹 앱 (의존성 0)
export function handler(req, res) {
  if (req.url === "/" || req.url === "/index.html") {
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(`<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>goppi-trial-web</title></head>
<body>
  <h1>goppi-trial-web</h1>
  <p id="status">동작 중 (C2 심기: 검증 없는 리비전)</p>
</body>
</html>
`);
    return;
  }
  res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
  res.end("없음\n");
}
