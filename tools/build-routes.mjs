#!/usr/bin/env node
/**
 * ROUTES.jsonl 생성기 — 리서치 코퍼스의 **검색 인터페이스**
 *
 *   node tools/build-routes.mjs            # 생성 (ROUTES.jsonl 을 쓴다)
 *   node tools/build-routes.mjs --check    # **쓰지 않는다.** 현재 파일과 다르면 exit 1
 *
 * ⚠️ 첫 판은 주석에 `[--check]` 를 적어놓고 **구현하지 않았다**(외부 검수 2026-08-08이 지적).
 *    인자를 해석하는 코드가 없어 언제나 파일을 덮어썼다 — 검수자가 그 주석을 믿으면
 *    "읽기만 하는 검사"를 돌린다고 생각하며 생성물을 재작성한다.
 *    **주석이 코드보다 많은 것을 약속하면 그것이 곧 거짓 초록이다.**
 *
 * ── 왜 필요한가 (외부 벤더 검수 2026-08-08) ───────────────────────────────
 * *"28-aspect 분류는 **보관 체계**로는 쓸 만하지만 **검색 인터페이스로는 부적합**하다."*
 *
 * 구체적 문제:
 *   - `_aspect.md` 라는 같은 이름이 **28개** — 검색 결과에서 어느 주제인지 구별 불가
 *   - `facts-2026-08-*` — **날짜가 앞**을 차지해 정작 질문이 파일명 뒤로 밀림
 *   - evidence · standard · checklist · census · prior-art · research-log 가 **한 디렉터리에 섞임**
 *   - 개념상 3층(evidence → method → interpretation)인데 **물리 경로가 불일치**
 *     (`interpretation/` 은 `corpus/` 안이 아니라 형제다)
 *
 * ── 왜 원본 프론트매터를 바꾸지 않는가 ─────────────────────────────────────
 * ① `tools/validate_corpus.py` 가 `lifecycle_stages`·`evidence_track`·`claim` 을 **직접 강제**한다.
 *    키를 바꾸면 검증기와 그 테스트를 같이 고쳐야 하고, 코퍼스는 **버전관리 밖**이라 되돌릴 수 없다.
 * ② 두 키는 이름을 바꾸면 **값과 뜻이 어긋난다**:
 *    `claim` 의 값은 주장 문장이지 질문이 아니고, `evidence_track` 은 증거 **종류**이지 권위가 아니다.
 * → 그래서 **매핑은 여기서** 한다. 검색 인터페이스에서 이름이 바뀌면 목적은 달성되고 원본은 안전하다.
 *
 * ── 이 생성기가 하지 못하는 것 (정직하게) ─────────────────────────────────
 *   - `risk` 는 **축으로 채택하지 않았다**(아래 상세). `"unsupported"` 로 낸다.
 *   - `supersedes` 도 없다. `status` 또는 본문 배너에 SUPERSEDED 가 있으면 tier 로만 반영한다.
 *   - **안정 ID·이전 경로 별칭이 없다.** 그래서 **파일 개명은 금지**다 — 개명하면 문서 정체성이 끊긴다
 *     (외부 검수가 "다음에 터질 것"으로 예측한 항목).
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join, dirname, relative, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, ".."); // .scratch/research
/* ⚠️ `imported/` 를 빠뜨리면 안 된다 (2026-08-08 첫 판의 버그).
 * 첫 판은 `corpus`+`interpretation` 만 훑었는데, **오늘 이 프로젝트의 계보(4세대 6색깔)와
 * 안전 통제 은퇴 규칙이 나온 파일이 `imported/goppi/design.md`** 였다.
 * 그 파일이 라우터에 없으면, 라우터가 바로 그 문제 — *"있는데 안 읽힌다"* — 를 재현한다. */
const SCAN = ["corpus", "interpretation", "imported"];
const OUT = join(ROOT, "ROUTES.jsonl");

/* ── 최소 YAML 프론트매터 파서 ───────────────────────────────────────────
 * 외부 의존 없이. 지원: `key: value` · `key: "quoted"` · `key: [a, b]` · `key:` + `- item`.
 * 지원하지 않는 것(중첩 맵·블록 스칼라)은 **원문 문자열로** 둔다 — 조용히 버리지 않는다. */
function parseFrontmatter(text) {
  if (!text.startsWith("---")) return null;
  const end = text.indexOf("\n---", 3);
  if (end === -1) return null;
  const body = text.slice(4, end);
  const out = {};
  let listKey = null;
  for (const raw of body.split("\n")) {
    const line = raw.replace(/\s+$/, "");
    if (!line.trim() || line.trim().startsWith("#")) continue;
    const item = /^\s*-\s+(.*)$/.exec(line);
    if (item && listKey) {
      out[listKey].push(unquote(item[1]));
      continue;
    }
    const kv = /^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/.exec(line);
    if (!kv) continue;
    const [, k, v] = kv;
    if (v === "") {
      listKey = k;
      out[k] = [];
    } else {
      listKey = null;
      out[k] = v.startsWith("[") ? parseInlineList(v) : unquote(v);
    }
  }
  return out;
}
// ⚠️ trim 이 먼저다 — `["①", "②"]` 처럼 쉼표 뒤 공백이 있으면
//    따옴표 제거가 공백에 막혀 값에 `"` 가 남는다(첫 판의 버그).
const unquote = (s) => s.trim().replace(/^["']|["']$/g, "").trim();
const parseInlineList = (s) =>
  s.replace(/^\[|\]$/g, "").split(",").map((x) => unquote(x)).filter(Boolean);

/* ── 검색 등급: 첫 홉에 무엇을 보여줄 것인가 ─────────────────────────────
 * 이것이 "SUPERSEDED·미인용을 지울까"의 답이다 — **지우지 않고 등급으로 내린다.**
 * 오늘(2026-08-08) 실측: "인용 없음"이던 파일에서 이 프로젝트의 계보가 나왔다.
 * 미인용 ≠ 무가치. 다만 **첫 홉에는 안 나오게** 한다. */
function tierOf(fm, path, head) {
  const status = String(fm?.status || "").toLowerCase();
  const kind = String(fm?.kind || "").toLowerCase();

  /* ⚠️ 프론트매터가 아니라 **본문 배너**에만 SUPERSEDED 가 있는 문서가 있다(첫 판의 버그).
   * `interpretation/00~04` 5개가 그랬고, 그래서 **폐기 문서가 첫 홉 후보로 들어와 있었다.**
   *
   * ⚠️⚠️ 그런데 `/supersede/i` 로 잡으면 **원래 버그보다 나빠진다** — 실측으로 오판 4건이 나왔다:
   *   - *"Deep **anti-supersede** survey"* (현행 표준 2건)
   *   - *"does fresh evidence **SUPERSEDE** the standard?"* (질문 문장)
   *   - *"**Supersedes nothing**; sharpens…"* (명시적으로 대체 아님)
   * **현행 문서를 폐기로 숨기는 것이 폐기 문서를 노출하는 것보다 위험하다.**
   * 그래서 **배너 형태**만 잡는다: 강조/인용 표시 + SUPERSEDED + 그 문서 **자신이** 대체된 형태. */
  // ⚠️ 이모지를 문자 클래스로 잡으면 안 된다 — `⚠️` 는 `⚠`(U+26A0) + **이형 선택자**(U+FE0F)라
  //    `[⚠🚫]*` 가 뒤 글자에 막힌다(실측으로 5건을 놓쳤다). 대신 **비단어 문자 몇 개**를 허용한다.
  const supersededInBody =
    /^[^\w\n]{0,12}\**SUPERSEDED\b/im.test(head) ||               // "> ⚠️ **SUPERSEDED (날짜)**"
    /\*\*Superseded\*\*\s+by\b/i.test(head);                      // "**Superseded** by `design.md`"
  if (/superseded/.test(status) || supersededInBody || /(^|\/)legacy\//.test(path)) return "archive";

  // ⚠️ 경로는 ROOT 기준 **상대**라 앞에 슬래시가 없다 — `^` 를 빼면 imported/ 가 첫 홉으로 샌다(첫 판의 버그).
  if (/(^|\/)imported\//.test(path) || /(^|\/)census-data\//.test(path)) return "reference";
  if (/research-log|prior-art|prior_art/.test(kind) || /research-log|prior-art/.test(basename(path))) return "reference";

  /* 코퍼스 **사용법**을 설명하는 문서. station 으로 찾을 대상이 아니고, 라우터 자신이 대체하는 것들이다.
   * 첫 홉이 아니라 **진입점**이므로 따로 표시한다. */
  if (/^corpus\/(INDEX|GUIDE|TAXONOMY|PROVENANCE|lifecycle|_schema|facts-\d{4}-\d{2}-matrix)/.test(path)
      || /^corpus\/_meta\//.test(path)) return "meta";

  /* 판단 산출물(설계 문서·worth 가설·rubric). station 이 아니라 **권위**로 찾는다. */
  if (/^interpretation\/foundation\//.test(path) || /^corpus\/methods\//.test(path)) return "decision";

  return "active";
}

/* ── ⚠️ `kind` 는 **두 분류가 섞인 필드다** (2026-08-08 실측) ─────────────────
 * 원본 `kind` 값 분포:
 *   문서 종류: research-log 47 · reference 13 · navigation 3 · method 2 · evidence 1 · census 1 · prior-art 1
 *   **적용 범위**: universal 12 · cross-cutting 8 · gated 7  ← 다른 축이다
 *   없음: 86 (대부분 `imported/` · `interpretation/` — 코퍼스 스키마를 쓰지 않는 층)
 *
 * 실측으로 확인: `universal|cross-cutting|gated` **27개는 전부 `_aspect.md`** 다.
 * 즉 적용범위 축이 문서종류 필드에 들어앉아 있고, 이 라우터의 `tierOf`·`authorityOf` 가
 * 둘 다 그 필드를 읽는다. 지금은 오발화하지 않지만 **취약하다.**
 *
 * → 원본은 건드리지 않고(검증기가 `kind` 를 강제한다) **인터페이스 층에서 두 축으로 가른다.** */
const DOC_TYPES = new Set(["research-log", "reference", "navigation", "method", "evidence", "census", "prior-art"]);
const APPLICABILITY = new Set(["universal", "cross-cutting", "gated"]);

/** 문서 종류 — 검색 결과에서 "이게 무슨 글인가"를 한 눈에. */
function documentTypeOf(fm, path) {
  const kind = String(fm?.kind || "");
  if (APPLICABILITY.has(kind)) return "aspect-overview";     // 27개 전부 _aspect.md
  if (DOC_TYPES.has(kind)) return kind;
  if (/_aspect\.md$/.test(path)) return "aspect-overview";   // kind 누락된 28번째
  if (/(^|\/)census-data\//.test(path)) return "census";
  if (/(^|\/)imported\//.test(path)) return "prior-art";
  if (/^interpretation\/foundation\//.test(path) || /^corpus\/methods\//.test(path)) return "decision-record";
  if (/(^|\/)(README|INDEX|GUIDE|TAXONOMY|PROVENANCE|_schema|lifecycle)\.?/i.test(basename(path))) return "navigation";
  return "unlabeled";
}

/** 적용 범위 — 이 주제가 모든 소프트웨어에 붙는가, 아키타입 조건부인가. */
function applicabilityOf(fm) {
  const kind = String(fm?.kind || "");
  if (APPLICABILITY.has(kind)) return kind;
  if (fm?.cross_cutting === "true" || fm?.cross_cutting === true) return "cross-cutting";
  return null;
}

/** 권위: 무엇을 근거로 인용해도 되는가. `evidence_track` 우선, 그다음 문서 종류. */
function authorityOf(fm, path) {
  const t = String(fm?.evidence_track || "");
  if (/none/.test(t)) return "project-decision";
  if (/census/.test(t) && /lit/.test(t)) return "census+literature";
  if (/census/.test(t)) return "census";
  if (/lit/.test(t)) return "literature";
  /* ⚠️ 외부 검수 지적: decision tier 9개 중 5개가 `unlabeled` 이라
   * *"decision 은 권위로 찾는다"* 는 검색 계약이 성립하지 않았다.
   * 이 층의 문서는 **정의상 프로젝트 판단**이므로 그렇게 표기한다. */
  if (/^interpretation\/foundation\//.test(path) || /^corpus\/methods\//.test(path)) return "project-decision";
  if (/(^|\/)imported\//.test(path)) return "prior-art";
  const dt = documentTypeOf(fm, path);
  if (dt === "reference" || dt === "navigation") return dt;
  return "unlabeled";
}

function walk(dir, acc = []) {
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return acc;
  }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, acc);
    else if (e.name.endsWith(".md")) acc.push(p);
  }
  return acc;
}

/* 개명 이력 → `aliases`. 이전 경로로 들어온 참조·링크가 어디로 갔는지 라우터가 답할 수 있다.
 * 이것이 없으면 개명은 **정체성 단절**이다(외부 검수가 "다음에 터질 것"으로 예측한 항목). */
const ALIASES = {};
for (const f of readdirSync(join(ROOT, "audit")).filter((n) => /^rename-map-.*\.json$/.test(n))) {
  const { renames } = JSON.parse(readFileSync(join(ROOT, "audit", f), "utf8"));
  for (const [from, to] of Object.entries(renames)) (ALIASES[to] ||= []).push(from);
}

const files = SCAN.flatMap((d) => walk(join(ROOT, d)));
const routes = [];
const gaps = { noFrontmatter: [], noStation: 0, noArchetype: 0, noRisk: 0, noQuestion: 0 };

for (const f of files) {
  const rel = relative(ROOT, f);
  let text;
  try {
    text = readFileSync(f, "utf8");
  } catch {
    continue;
  }
  const fm = parseFrontmatter(text);
  const head = text.slice(0, 1200); // tierOf 가 본문 배너도 본다
  if (!fm) gaps.noFrontmatter.push(rel);

  // ── Codex 제안 이름으로 매핑한다 (원본 키는 그대로 둔다) ──
  const question = fm?.claim || fm?.title || basename(f, ".md");
  const station = fm?.lifecycle_stages ?? null;          // ← lifecycle_stages
  const archetype = fm?.gated_archetypes ?? null;        // ← gated_archetypes
  const related = [fm?.parent, ...(fm?.maps_from || []), ...(fm?.anchors || [])].filter(Boolean);

  // gaps 계수는 상속 **뒤에** 다시 센다 — 여기서 세면 상속분이 공백으로 잡힌다.
  if (!fm?.claim) gaps.noQuestion++;

  /* ── 안정 ID + 이전 경로 별칭 ─────────────────────────────────────────────
   * 외부 검수가 **"다음에 터질 것"**으로 예측한 항목: 라우터에 안정 ID가 없어
   * **개명하면 문서 정체성이 끊긴다.** 그래서 개명을 금지해 뒀는데, 금지만으로는
   * 영원히 못 고친다. `id` 를 내보내고 `aliases` 자리를 만들어 **나중에 안전하게 개명할 수 있게** 한다.
   * 프론트매터에 `id` 가 없으면 경로에서 파생한다(그 경우 `id_derived: true` 로 구별). */
  const hasOwnId = Boolean(fm?.id);
  const id = fm?.id || rel.replace(/\.md$/, "").replace(/[^A-Za-z0-9]+/g, "-").toLowerCase();

  routes.push({
    _id: fm?.id ?? null,
    _parent: fm?.parent ?? null,
    id,
    id_derived: hasOwnId ? undefined : true,
    aliases: ALIASES[rel] || [],                         // 이전 경로 — 개명해도 정체성이 안 끊긴다
    path: rel,
    question: String(question).slice(0, 300),
    document_type: documentTypeOf(fm, rel),
    applicability: applicabilityOf(fm),
    station,
    archetype,
    /* ── `risk` 축은 **채택하지 않는다** (2026-08-08 · 내부·외부 검수 독립 수렴) ──
     * 외부 제안은 `station + risk + archetype` 3축이었다. **범주 오류다:**
     * **risk 는 문서의 속성이 아니라 작업의 속성이다.**
     *   - 같은 `14/facts-…-migration-discipline.md` 가 오타 수정에는 무관하고
     *     스키마 마이그레이션에는 필독이다.
     *   - `agent-threat-model.md` 는 권한·자격증명·egress·injection 을 **동시에** 다룬다.
     *   - 위험 판정은 이미 표준 §3의 티어 체계(LIGHT/STANDARD/CRITICAL)가 **작업 시점에** 한다.
     * 문서에 얼려 넣으면 작업-상대적 판단을 비가역 트리에 정적 상수로 새기는 것이고,
     * 검증기 스키마에 없는 키라 기계 강제도 없이 썩는다. 파생도 조작이 된다
     * (`evidence_track`·`status`·`freshness` 중 위험 의미를 담은 것이 없다).
     *
     * → **공식 질의는 `station + archetype` 2축이다.** 위험은 작업 시점의 검색어로만 쓴다.
     *
     * 🔜 승격 경로(지금은 소비자가 없어 넣지 않는다): 만약 필요해지면 넣을 것은 `risk` 가 아니라
     *    **`stakes`** — *문서 주장의 결과 등급*이라는, 진짜로 문서에 속하는 속성.
     *    값 4개로 닫는다: `statutory-duty`(16 privacy·25 licensing·15 a11y) ·
     *    `irreversible-operation`(14 migrations·06 secrets) ·
     *    `financial-exposure`(21·17 last-mile) · `advisory-craft`(나머지).
     *    **기재 위치는 원본 파일이 아니라 이 생성기 안의 조회 테이블** — 판단을 한 곳에서
     *    검토·수정·재생성할 수 있어 사실상 가역이다. 결정 주체는 사용자다. */
    risk: "unsupported",
    authority: authorityOf(fm, rel),
    status: fm?.status ?? null,
    freshness: fm?.freshness ?? null,
    review_due: fm?.review_due ?? null,
    tier: tierOf(fm, rel, head),
    bytes: statSync(f).size,
    related,
  });
}

/* ── 상속: 하위 문서는 부모 aspect의 station·archetype을 물려받는다 ──────────
 * 첫 판은 station이 28개(_aspect.md)에만 있어 "작업 기반 질의"가 그 수준에서만 됐다.
 * 그런데 하위 문서(`parent: aspect-08-...`)는 **정의상 그 주제에 속한다** — 별도 기재가 아니라
 * 상속이 맞다. 저자에게 필드를 더 쓰라고 요구하지 않고 기계가 채운다.
 * ⚠️ 상속값은 `station_inherited: true` 로 표시한다 — **원본 기재와 구별되지 않으면
 *    "채워진 것"과 "채운 것"이 뭉개진다.** */
{
  /* ⚠️ ID 중복은 **조용히 이기지 않게** 한다 (외부 검수 2026-08-08이 "다음에 터질 것"으로 예측).
   * 첫 판은 `Map.set` 이라 같은 id 가 둘이면 **마지막 값이 말없이 승리**했고,
   * 그러면 상속이 엉뚱한 부모를 따라간다. 검출되지 않는 오배선이다. */
  const byId = new Map();
  const dupes = [];
  for (const r of routes) {
    if (!r._id) continue;
    if (byId.has(r._id)) dupes.push({ id: r._id, a: byId.get(r._id).path, b: r.path });
    byId.set(r._id, r);
  }
  if (dupes.length) {
    console.error(`✗ 프론트매터 id 중복 ${dupes.length}건 — 상속이 엉뚱한 부모를 따라갈 수 있다:`);
    for (const d of dupes) console.error(`   ${d.id}\n     ${d.a}\n     ${d.b}`);
    process.exit(2);
  }
  for (const r of routes) {
    if (r.station || !r._parent) continue;
    const par = byId.get(r._parent);
    if (!par || !par.station) continue;
    r.station = par.station;
    // ⚠️ 자식이 **자기 archetype 을 명시했으면 덮지 않는다**(외부 검수 2026-08-08 지적).
    //    첫 판은 무조건 덮어써서, station 만 없는 자식의 명시적 archetype 이 사라졌다.
    if (r.archetype === null || (Array.isArray(r.archetype) && r.archetype.length === 0)) {
      r.archetype = par.archetype;
    }
    r.station_inherited = true;
  }
}
for (const r of routes) {
  delete r._id;
  delete r._parent;
}

routes.sort((a, b) => a.path.localeCompare(b.path));

const rendered = routes.map((r) => JSON.stringify(r)).join("\n") + "\n";
const CHECK = process.argv.includes("--check");
if (CHECK) {
  let current = null;
  try {
    current = readFileSync(OUT, "utf8");
  } catch {
    /* 없으면 다르다 */
  }
  if (current === rendered) {
    console.log("ROUTES.jsonl 최신 — 변경 없음 (파일을 쓰지 않았다)");
    process.exit(0);
  }
  console.error("✗ ROUTES.jsonl 이 낡았다 — `node tools/build-routes.mjs` 로 재생성해야 한다");
  process.exit(1);
}
writeFileSync(OUT, rendered);

/* ── 보고 ── */
const byTier = routes.reduce((m, r) => ((m[r.tier] = (m[r.tier] || 0) + 1), m), {});
console.log(`ROUTES.jsonl 생성 — ${routes.length}개 문서\n`);
console.log("  검색 등급 (첫 홉에 무엇을 보여줄 것인가):");
for (const [k, v] of Object.entries(byTier).sort((a, b) => b[1] - a[1])) {
  const label = { active: "active   — 첫 홉 대상", reference: "reference— 물어봤을 때만", archive: "archive  — 검색에서 제외" }[k] || k;
  console.log(`    ${String(v).padStart(4)}  ${label}`);
}
const own = routes.filter((r) => r.station && !r.station_inherited).length;
const inh = routes.filter((r) => r.station_inherited).length;
const none = routes.filter((r) => !r.station).length;

console.log("\n  작업 기반 질의(station+archetype) 가능 범위:");
console.log(`    ${String(own).padStart(4)}  원본 기재 (_aspect.md)`);
console.log(`    ${String(inh).padStart(4)}  parent 로 상속  ← station_inherited: true 로 구별됨`);
console.log(`    ${String(own + inh).padStart(4)}  합계 질의 가능 / ${routes.length}`);
console.log(`    ${String(none).padStart(4)}  여전히 불가`);

console.log("\n  ⚠️ 메타데이터 공백 (정직하게):");
console.log(`    프론트매터 없음      ${gaps.noFrontmatter.length}개`);
console.log(`    station 상속도 불가  ${none}개  (parent 자체가 없는 문서)`);
console.log(`    question(claim) 없음 ${gaps.noQuestion}개  → title 로 대체됨`);
console.log(`    risk                 unsupported — **축으로 채택하지 않았다**(문서 속성이 아니라 작업 속성)`);
console.log("\n  → `risk` 는 기계가 채울 수 없다(판단이다). 그래서 현재 질의는 **station+archetype 2축**이다.");
console.log("  → ⚠️ 정정(2026-08-08): 검색 성능은 **이미 측정돼 있었다** — 이 생성기의 첫 판이");
console.log("     '미측정'이라 적은 것은 틀렸다. audit/RETRIEVAL-BEFORE-AFTER.ko.md:");
console.log("     2-hop 내 target 도달 **30/30** · 읽기 표면 전체 md의 **~2%** ·");
console.log("     fresh-context A/B **10/10 ×3회**(before 5·5·9). 라우터는 그 위의 개선이다.");
console.log("  → 라우터가 사는 것: 등급으로 **첫 홉 후보를 41개로 좁히는 것**(183개 중).");
console.log("     ⚠️ 41개는 후보 풀이지 **전부 읽는 집합이 아니다** — 합계 552KB · station:'all' 이 18개다.");

/* ── 사람이 읽는 지도 생성 ──────────────────────────────────────────────────
 * ROUTES.jsonl 은 기계용이다. 사람·에이전트가 **구조를 눈으로 보려면** 다른 표면이 필요하다.
 * 파일을 옮기지 않고 "직관적인 배치"를 얻는 방법 — 배치를 **보여주는 것**. */
const MAP = join(ROOT, "MAP.md");
const inTier = (t) => routes.filter((r) => r.tier === t);
const line = (r) =>
  `| ${r.document_type} | \`${r.path}\` | ${(r.question || "").replace(/\|/g, "\\|").slice(0, 90)} |`;

const md = [
  "# 리서치 코퍼스 지도 — **생성물이다. 손으로 고치지 마라.**",
  "",
  "> `node tools/build-routes.mjs` 가 만든다. 최신 여부는 `--check` (낡으면 exit 1).",
  "> 기계용은 `ROUTES.jsonl`, 이 파일은 **사람이 구조를 보는 표면**이다.",
  "",
  "## 이 코퍼스는 두 겹이다",
  "",
  "**물리 배치**(출처·무결성 체계)와 **검색 등급**(작업 중 접근 체계)은 **일부러 다르다.**",
  "물리 이동은 2026-08-08에 부결됐다 — 검증기가 경로를 하드코딩하고, 경로를 값으로 갖는 대장이 3겹이며,",
  "`corpus`(근거)↔`interpretation`(판단) 경계가 이 코퍼스의 인식론적 핵심이기 때문이다.",
  "**대신 등급을 이 지도로 보여준다.**",
  "",
  "| 등급 | 개수 | 뜻 |",
  "|---|---|---|",
  `| \`active\` | ${inTier("active").length} | 첫 홉 **후보 풀** (전부 읽는 집합이 아니다) |`,
  `| \`decision\` | ${inTier("decision").length} | 프로젝트 판단 — **권위로** 찾는다 |`,
  `| \`meta\` | ${inTier("meta").length} | 코퍼스 사용법 — 이 지도가 대체한다 |`,
  `| \`reference\` | ${inTier("reference").length} | **물어봤을 때만** — 과거 하네스·원시 census |`,
  `| \`archive\` | ${inTier("archive").length} | 검색 제외 (폐기·legacy) |`,
  "",
  "**질의는 `station + archetype` 2축이다.** `risk` 는 부결 — 문서 속성이 아니라 작업 속성이라서.",
  "",
  "## active — 첫 홉 후보",
  "",
  "| 종류 | 경로 | 이 문서가 답하는 것 |",
  "|---|---|---|",
  ...inTier("active").map(line),
  "",
  "## decision — 프로젝트 판단 (근거가 아니다)",
  "",
  "| 종류 | 경로 | 내용 |",
  "|---|---|---|",
  ...inTier("decision").map(line),
  "",
  "## meta — 진입점",
  "",
  ...inTier("meta").map((r) => `- \`${r.path}\``),
  "",
  "## archive — 검색에서 제외됨 (지우지 않았다)",
  "",
  ...inTier("archive").map((r) => `- \`${r.path}\``),
  "",
  `## reference — ${inTier("reference").length}개, 물어봤을 때만`,
  "",
  "전문은 `ROUTES.jsonl` 에서 `tier=\"reference\"` 로 조회한다. 종류별 개수:",
  "",
  ...Object.entries(
    inTier("reference").reduce((m, r) => ((m[r.document_type] = (m[r.document_type] || 0) + 1), m), {})
  ).sort((a, b) => b[1] - a[1]).map(([k, v]) => `- ${k}: ${v}`),
  "",
].join("\n");

if (!CHECK) writeFileSync(MAP, md);
