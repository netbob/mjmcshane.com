---
title: "Two Books, One Tab: How netbob.org Reads Its Novels from GitHub"
date: 2026-10-29
author: Michael McShane
description: "The Books tab on netbob.org now serves two novels from two GitHub repos, rebuilt automatically on every chapter push. Here's the pipeline, and the three things that bit along the way."
tags: [github, cloudflare, jekyll]
---

I filed Chapter 11D of *The Shattered Lens* on a Thursday night, and a few minutes later it was sitting on the Books tab at netbob.org, in the chapter list, with the right title, next to eleven other chapters. No deploy step from me. No post to write. It just showed up, like magic.

Magic, of course, is a pipeline you haven't looked at yet. Here's the one behind the tab.

## Two books, two repos, one reading face

Both novels now live in their own public repos, which are the manuscripts' source of truth:

- *The Dark Fills the Space* — `netbob/The-Dark-Fills-the-Space`, four chapters plus dedication, migrated off the site's post files the same night.
- *The Shattered Lens* — `netbob/The-Shattered-Lens`, fifty-four modules across eleven chapters and counting.

The site itself, `netbob/netbob.org`, is the reading face. The Dark chapters still render from site posts — the repo is the manuscript, the post is the publication step. The Lens chapters had never been on the site at all; they lived only in GitHub. The Books tab needed to serve both without turning the site repo into a second copy of either manuscript.

Jekyll can't read another repo at build time — no plugin does that on Cloudflare Pages. So the fetch happens before Jekyll runs, in the build command itself:

```
python3 tools/fetch-lens.py && RUBYOPT=-EUTF-8 bundle install && RUBYOPT=-EUTF-8 bundle exec jekyll build
```

The script shallow-clones the Lens repo, copies `chapters/*/module-*.md` into a `_lens/` directory, and injects the YAML front matter Jekyll needs to render each module as a page. `_lens/` is git-ignored build output; it never gets committed. A `lens` collection in `_config.yml` renders it at `/lens/:path/`, and the Books tab lists it with a Liquid loop grouped by chapter. If the collection is ever empty — fetch failed, script missing — the tab falls back to linking the GitHub repo instead of rendering a broken list.

## The chain that makes it automatic

A chapter push to the Lens repo fires a GitHub Action, which posts to a Cloudflare Pages deploy hook, which rebuilds the site with the fetch step:

```yaml
name: Rebuild netbob.org

on:
  push:
    branches: [main]
    paths:
      - 'chapters/**'
      - 'cover.webp'

jobs:
  rebuild:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Cloudflare Pages deploy hook
        run: |
          if [ -n "$NETBOB_DEPLOY_HOOK" ]; then
            curl -sf -X POST "$NETBOB_DEPLOY_HOOK"
          else
            echo "NETBOB_PAGES_DEPLOY_HOOK not set; skipping."
          fi
        env:
          NETBOB_DEPLOY_HOOK: ${{ secrets.NETBOB_PAGES_DEPLOY_HOOK }}
```

The hook URL lives in exactly two places: the Cloudflare dashboard and a GitHub repo secret. The Action skips cleanly until the secret exists, so the workflow file can land before the secret does.

## Three things that bit

**Chapter 1's headers are shaped differently.** Chapters 2–11 open each module with an H1 module title. Chapter 1 opens with an H1 act header, an H2 chapter header, and the module title down at H3. My first title-derivation logic took the first H1, so all five Chapter 1 entries rendered as "Act I: The Logic Loop." The fix was in the script, not the manuscript: prefer a `Module NX:` heading at any level, fall back to the first H1. Filed text stays verbatim; the tool adapts.

**Cloudflare "retry" rebuilds the same commit.** After fixing the script, I hit Retry deployment and watched the build succeed — with the old script, because retry re-runs the original commit. The fix only went live with a fresh deployment from latest main. Retrying feels like redeploying; it isn't.

**The bot couldn't write the workflow file.** GitHub won't let the machine account create `.github/workflows/` files — a workflows-permission boundary, not a bug I could retry past. That one file I committed by hand in the web editor, and it's the only step in the chain that needed a human hand. Everything else went through the normal approval-and-push flow.

## Where it stands

The Books tab now serves both novels, the repos hold the manuscripts, and the site rebuilds itself when the manuscripts change. The one deliberate asymmetry left: Dark chapters still reach the site as posts, a publication step I do by hand, while Lens chapters arrive by fetch. Unifying that is a separate decision — the Lens path would need URL-preserving care for the Dark posts' existing addresses — and it's not one I've made yet.

The pipeline's job is to disappear. Filing a chapter should feel like the chapter showing up. Thursday night, for the first time, it did.
