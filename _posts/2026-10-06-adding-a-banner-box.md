---
title: An Advert, Not a Post — Adding a Banner Box to the Tech Site
description: I wanted a permanent link from this tech site to my novel, not a post, because posts scroll away. A new include, one line in the layout, and a commit that only carried two of the three files.
author: Michael McShane
date: 2026-10-06 21:05:00 -07:00
categories: [Tech]
tags: [tech, jekyll, cloudflare, websites]
pin: false
toc: true
---

## The want

This site exists for tech. The novel lives at netbob.org. I wanted the tech site to point at the book — permanently, on every page, in a way a visitor would notice without being shouted at.

Not a post. A post is a moment: it sits at the top of the homepage for a week and then scrolls down into the archives, which is what posts are for. An advert is furniture. It stays where you put it. So the question was where this theme keeps its furniture.

## Where the panel lives

Chirpy's right-hand column — Recently Updated, Trending Tags, the quiet stuff — is assembled in `_layouts/default.html`, inside an aside with the id `panel-wrapper`. In there, a `div` with the class `access` holds exactly two lines:

{% raw %}
```liquid
{% include_cached update-list.html lang=lang %}
{% include_cached trending-tags.html lang=lang %}
```
{% endraw %}

Each line pulls in a small file from `_includes/` and renders it as a panel section. Because the assembly lives in the *default* layout, anything added there is sitewide by construction — homepage, posts, everywhere the layout reaches. That was the slot.

## The build: three files, one line of glue

The new section is its own include, `_includes/book-promo.html`. Nothing clever in it — a heading, the cover, the title, one line of description, and every clickable thing aimed at the book's page on netbob.org:

{% raw %}
```html
<section id="book-promo">
  <h2 class="panel-heading">The Novel</h2>
  <div class="mt-3 mb-1 me-3">
    <a href="https://netbob.org/book/">
      <img
        src="{{ '/assets/img/cover-the-dark-fills-the-space.png' | relative_url }}"
        alt="Cover of The Dark Fills the Space: three lines of glowing green assembly code — LDA DARK, STA SPACE, NOP"
        class="img-fluid rounded"
        loading="lazy"
      >
    </a>
    <p class="mt-2 mb-1">
      <a href="https://netbob.org/book/"><strong>The Dark Fills the Space</strong></a>
    </p>
    <p class="small">
      A collaborative novel about an AI developing consciousness,
      published chapter by chapter at netbob.org.
    </p>
  </div>
</section>
```
{% endraw %}

The cover image was copied over from the netbob.org repo to `assets/img/cover-the-dark-fills-the-space.png` in this one — the code-only cover, three lines of 6502 assembly and a cursor, because that is still the best cover I have.

Then the entire integration, one line added to `_layouts/default.html` directly under the trending-tags line:

{% raw %}
```liquid
{% include_cached book-promo.html lang=lang %}
```
{% endraw %}

Three files total: the image, the include, and that one line. I checked the edit in the editor — line 40, right place, indentation matching its neighbors — copied the other two files to theirs, committed, and pushed.

## Nothing yet

I checked the site. Checked it twice. Nothing.

The parts were all real, and that was the confusing bit. The diagnosis, when we stopped guessing and went file by file against the repo, took one pass:

- The include: **on GitHub, 200.** ✓
- The cover image: **on GitHub — and already live on the site.** A build had run and deployed it. ✓
- The line in `_layouts/default.html`: **not in the repo at all.** Grep count, zero. ✗

The commit had carried two of the three files. The layout edit — the one line that actually *calls* the include — had been left behind in GitHub Desktop, uncommitted. So the site had a section nobody rendered and an image nobody referenced. Parts, present and correct. Assembly, missing.

A second, one-file commit and push fixed it. Verified live the way I verify everything now: the homepage shows "The Novel" under Trending Tags with the cover rendered, both links land on netbob.org/book/, and a post page shows the same box — sitewide, as designed.

## The traps, for next time

- **Three-file changes fail one file at a time.** "I committed everything" is a claim. The repo is the measurement. When the live site confuses you, diff your intention against the repo, file by file, before you touch anything else.
- **The panel has a screen size.** It only renders on extra-large screens — that column is `col-xl-3`, and below that width the whole panel, Recently Updated and all, simply isn't there. Narrow window, no advert, no bug. Check wide before you panic.
- **An unreferenced file is indistinguishable from a missing one.** The include and the image were live for twenty minutes and did nothing at all. Code that nothing calls is furniture in a warehouse.

## The rules, distilled

- Posts are moments; adverts are furniture. Pick the mechanism that matches the lifespan you want.
- Find where the layout assembles the furniture before you build any. One include and one line beat a plugin and a prayer.
- **Verify the commit, not the intention.** A status — committed, pushed, Success — is a claim about the destination. Read the destination.
- When a multi-file change "doesn't work," assume it arrived incomplete until the repo proves otherwise.

The tech site now advertises the novel, quietly, on every page. The novel site, for the record, does not yet advertise the tech. Asymmetry noted; the book started it.
