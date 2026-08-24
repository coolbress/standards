import { createServer } from "node:http";
import { handler } from "./app.mjs";

const port = Number(process.env.PORT || 3000);
createServer(handler).listen(port, () => {
  console.log(`goppi-trial-web: http://localhost:${port}`);
});
