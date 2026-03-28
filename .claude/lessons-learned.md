# Lessons Learned

A running log of process improvements, recurring mistakes, and things that worked well. Reviewed at the start of `/kickoff` for relevant context.

## Format

```
### YYYY-MM-DD — Short title
**What happened:** What went wrong or what insight emerged.
**Root cause:** Why it happened.
**Process change:** What rule or step was added/changed as a result.
**Applies to:** Which issue types or phases this affects.
```

---

## 2026-03-28 — MVP line drawn at commit 736ab606

**What happened:** MVP v0.1.0 declared complete. All work up to and including commit `736ab606` on `main` is MVP bootstrap — process setup, documentation, Linear issues, skills. This work went directly to `main` without PRs, which is a one-time justified exception.

**Root cause:** The PR process was being established during this work. It would be circular to require PRs for the commits that created the PR requirement.

**Process change:** From commit `736ab606` onwards, the full process is mandatory for all work — no exceptions except explicit agreement with the user:
1. Idea → Linear (Backlog + Idea label)
2. `/review-ideas` → convert to issue
3. `/kickoff` → feature branch → implement → PR → merge

**Applies to:** All future work without exception.

---

## 2026-03-28 — Documentation not tracked during post-MVP cleanup session

**What happened:** A full session of work (Linear docs archived, DOMAINS.md expanded, project description updated, README/ARCHITECTURE rewritten, MVP docs created) was completed without any entries in `RELEASE_NOTES.md` under "Unreleased". The work was invisible in the release history.

**Root cause:** The CONTRIBUTING.md step 8 (Merge) only mentioned updating RELEASE_NOTES.md but did not explicitly list which other docs to check, and did not make the documentation review a named step. It was easy to skip.

**Process change:** Added step 9 (Documentation update) and step 10 (Lessons learned) to CONTRIBUTING.md. Step 9 includes a table mapping change types to the docs that must be reviewed. Step 9 is now a required named step, not a bullet under Merge.

**Applies to:** All issue types — every merge requires a documentation review pass.

---

## 2026-03-28 — Instagram token was for wrong account

**What happened:** First Instagram publish attempt failed — the access token was for the personal account (radoslawutkala) not the business account (@otwarteraporty). Token had to be regenerated after switching the active profile in Meta Developer portal.

**Root cause:** Meta Developer portal defaults to the personal profile. The correct account must be explicitly selected when generating tokens.

**Process change:** Documented in `.claude/playbooks/social.md` — token generation step now specifies "ensure @otwarteraporty is the active profile in Meta Developer before generating".

**Applies to:** Instagram publishing, token refresh (next: ~May 2026).

---

## 2026-03-28 — Instagram image cached by URL

**What happened:** After regenerating the Instagram card with Nordic theme colors, republishing to the same URL (`post_test.png`) showed the old image. Instagram had cached the original.

**Root cause:** Instagram caches media container images by URL. Same filename = same URL = cached image, even if the file content changed.

**Process change:** Documented in `.claude/playbooks/social.md` — always use a unique filename per post. Timestamp or content-based naming recommended.

**Applies to:** Instagram publishing — every post.

---

## 2026-03-28 — Ghost title env var ignored on existing installation

**What happened:** Added `title: Otwarte Raporty` to Ghost environment in docker-compose.yml. After restart, the blog header still showed "Open Reporting".

**Root cause:** Ghost env vars for `title`, `description`, etc. only apply on first install (when the DB is initialised). An existing Ghost installation ignores them — the value is stored in the `settings` table in the Ghost database.

**Process change:** To rename Ghost on an existing install, use Node.js knex query directly against ghost.db:
```bash
docker exec ghost node -e "
  const knex = require('knex')({client:'sqlite3',connection:'/var/lib/ghost/content/data/ghost.db'});
  knex('settings').where({key:'title'}).update({value:'Otwarte Raporty'}).then(()=>process.exit(0));
"
```

**Applies to:** Ghost CMS configuration changes on existing installations.
