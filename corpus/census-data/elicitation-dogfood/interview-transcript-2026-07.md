# Dogfood interview — a command-line bookmark manager

A live interview conducted by the host session model (`claude-opus-4-8`) acting as the `elicit`
interviewer, against a fresh idea (not one of the eval fixtures). It records the **model-only layer** the
per-PR gates deliberately do not exercise: question *phrasing* (Mom-Test, ≤2 per turn) and answer →
structured-fragment *extraction*. The structured extraction is `transcript.json`; the locked output is
`prd.yml` (seal `6319d9c7…`).

---

**Interviewer:** Tell me about the last time you actually went looking for a link you'd saved before —
what were you trying to find, and where had you saved it?

**Builder:** Last week I wanted a recipe I'd bookmarked ages ago. I had no idea if it was in my browser
bookmarks, a note, or a message to myself. I gave up and re-googled it.

**Interviewer:** So the real job is *finding a saved link again later*, not just saving it. When you go
back for one, what do you actually remember about it — the site, or more like "it was a recipe" / "it was
about taxes"?

**Builder:** Definitely the topic, not the site. I'd remember "recipe" or "work stuff".

> _Extracted → job-to-be-done: "find a previously saved link again by the tags I remember"; the core
> stories: save a URL with tags, search by tag, open in the browser, all in one local file._
> _Between turns: `gingoa elicit validate draft.yml` → all four acceptance criteria are well-formed EARS._

**Interviewer:** `gingoa elicit measure --next draft.yml` says the least-covered area is **scope**. Two
quick ones: should this also try to sync across your machines, or is one computer fine? And do you want a
browser extension, or is a command-line tool enough?

**Builder:** One computer is fine, and no extension — command line is exactly what I want. Keep it small:
save with tags, search, open, and maybe list everything.

> _Extracted → scope.must: save-with-tags · search-by-tag · open-in-browser · list-all;
> scope.out: sync-across-machines · a browser extension._

**Interviewer:** Next gap is **assumptions**. Can I assume you've got a default browser the tool can just
hand a URL to? And that a single file on your machine is enough to hold the whole collection?

**Builder:** Yes to both — I always have a default browser, and I'd never have so many bookmarks that one
file is a problem.

> _Extracted → assumptions: a default browser the OS can launch · one local file is enough for a personal
> collection._

**Interviewer:** Last gap is **anti-goals** — the things you explicitly *don't* want this to become.
Anything you'd want it to never do?

**Builder:** Never upload my stuff anywhere, and please don't track which links I click. It's just for me.

> _Extracted → anti_goals: never sync to a server or the cloud · never track which links the user opens._
> _Between turns: `gingoa elicit risk draft.yml` → no danger zone tripped (local tool, no payments / personal
> data / public exposure); `gingoa elicit measure draft.yml` → every dimension covered, zero open
> clarifications, but `mustElicit` still lists visibility and license as `unasked`._

**Interviewer:** Two last choices that are yours to make. First — is this project public, where anyone can
see the code, or private, just for you? Second, the license: most people use MIT (anyone can use it, few
strings); if you're not sure, MIT is the common default. Public + MIT, or would you change either?

**Builder:** I'll put it on GitHub for others, so public. MIT is fine.

> _Extracted → audience.visibility: public (a public project also gets a Code of Conduct) · license: MIT._
> _`gingoa elicit measure draft.yml` → `mustElicit`: both `answered`._

**Interviewer:** That's the whole picture — what it does, its quality bar, scope, constraints,
assumptions, risks, anti-goals, who it's for, and its visibility + license. I'm locking the requirements now
so they can't drift while we build.

> _`gingoa elicit lock draft.yml` → `ok: true`, `status: locked`, sealed (the seal now also covers the
> declared visibility)._
