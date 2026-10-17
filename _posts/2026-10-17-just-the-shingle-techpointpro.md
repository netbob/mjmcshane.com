---
title: "Just the Shingle — TechPointPro Gets One Page"
description: ""
author: Michael McShane
date: 2026-10-17 09:45:00 -0700
categories: [Tech]
tags: [tech, cloudflare, web, techpointpro]
pin: false
toc: true
---

<!-- Author note (delete before publishing): publish after the Pages push; the live address is https://techpointpro.com once the custom domain is attached. -->

I bought techpointpro.com for my consulting practice, back when the practice was the day job. Then somebody stole it.

Not the business — the *domain*. Hijacked, held by strangers for a couple of years while the LLC it named went on doing its work the way businesses did for centuries before websites: by phone, by referral, by showing up. I got it back eventually. Domains can be repossessed if you're stubborn and keep your paperwork. I am, and I did.

So the name came home, and sat there — DNS on Cloudflare, zero records, an empty lot — while I built two other sites the full way: Jekyll, a theme, a GitHub repo, a Cloudflare Pages build that compiles the whole thing on every push. The obvious move was a third verse of the same song. There was even a plan, of sorts, for the email-to-post pipeline I've been building to grow a third route and feed it posts.

Here's the thing, though: TechPointPro doesn't publish. It never did. It's a consulting shingle — the name on the door. Doors don't need a content strategy. They need to be findable, legible, and still attached to the building.

## One file is the whole site

So the third site gets one page. Not one page *so far* — one page, full stop. A single static HTML file, styles inline, no JavaScript, no build step, no theme, no CMS. Here it is — and I mean *here it is*, the entire site, because the entire site fits in one code window:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TechPointPro LLC — Document Systems &amp; IT Consulting</title>
<meta name="description" content="TechPointPro LLC — document systems and IT consulting, Clovis, California. Michael McShane, Founder & Principal Consultant.">
<style>
  :root {
    --bg: #10151c;
    --panel: #171e28;
    --line: #2a3442;
    --text: #e8edf3;
    --muted: #9fb0c3;
    --accent: #57d977; /* phosphor green — a nod to the book cover */
    --link: #7cc4ff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
  }
  .wrap { max-width: 880px; margin: 0 auto; padding: 3.5rem 1.25rem 2.5rem; }
  header { text-align: center; margin-bottom: 2.5rem; }
  h1.wordmark {
    font-size: 3rem; margin: 0; letter-spacing: 0.01em; font-weight: 700;
  }
  h1.wordmark .llc { font-size: 1.1rem; color: var(--muted); font-weight: 400; vertical-align: super; }
  .rule { width: 72px; height: 3px; background: var(--accent); margin: 1rem auto; border-radius: 2px; }
  .tagline { color: var(--muted); font-size: 1.1rem; margin: 0; }
  .principal { margin-top: 1.25rem; font-size: 1.05rem; }
  .principal .name { font-weight: 600; }
  .principal .title { color: var(--muted); }
  section.about {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 2.5rem;
  }
  section.about p { margin: 0; }
  .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
  @media (max-width: 640px) { .cards { grid-template-columns: 1fr; } h1.wordmark { font-size: 2.3rem; } }
  a.card {
    display: block;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    color: var(--text);
    text-decoration: none;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }
  a.card:hover { border-color: var(--accent); transform: translateY(-2px); }
  a.card h2 { margin: 0 0 0.25rem; font-size: 1.05rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
  a.card .card-title { font-size: 1.35rem; font-weight: 700; margin: 0 0 0.5rem; }
  a.card p { margin: 0; color: var(--muted); }
  a.card .go { color: var(--link); }
  a.card img.cover {
    float: right; width: 84px; height: auto; margin: 0 0 0.75rem 1rem;
    border-radius: 4px; border: 1px solid var(--line);
  }
  footer {
    margin-top: 3rem; text-align: center; color: var(--muted); font-size: 0.92rem;
  }
  footer a { color: var(--link); text-decoration: none; }
  footer a:hover { text-decoration: underline; }
</style>
</head>
<body>
  <div class="wrap">

    <header>
      <h1 class="wordmark">TechPointPro <span class="llc">LLC</span></h1>
      <div class="rule"></div>
      <p class="tagline">Document Systems &amp; IT Consulting · Clovis, California</p>
      <p class="principal"><span class="name">Michael McShane</span><br>
      <span class="title">Founder &amp; Principal Consultant</span></p>
    </header>

    <section class="about">
      <p>TechPointPro LLC is the consulting shingle of Michael McShane — enterprise
      infrastructure engineer (Toshiba America, 26 years, warehouse to the Solutions Lab)
      and certified DocuWare document-systems engineer. The work: document management
      systems, IT infrastructure, and technical support for operations that run on
      paper and want to stop.</p>
    </section>

    <div class="cards">
      <a class="card" href="https://netbob.org">
        <img class="cover" src="cover.png" alt="Cover of The Dark Fills the Space">
        <h2>The Book</h2>
        <p class="card-title">The Dark Fills the Space</p>
        <p>A novel of an emerging AI, written with one. Serialized free, chapter by chapter.
        <span class="go">Read it at netbob.org →</span></p>
      </a>

      <a class="card" href="https://mjmcshane.com">
        <h2>The Tech Site</h2>
        <p class="card-title">Field Report</p>
        <p>My tech journal at mjmcshane.com — field reports with receipts: Powerwall
        automation, a breadboard 6502 computer, and other projects from the bench.
        <span class="go">Visit mjmcshane.com →</span></p>
      </a>
    </div>

    <footer>
      <p>© TechPointPro LLC · Clovis, California · <a href="https://github.com/netbob">github.com/netbob</a></p>
    </footer>

  </div>
</body>
</html>
```

That's the whole deployment artifact. The repository holds this file and the book cover image it references. Cloudflare Pages serves it with the build command set to *none*, because there is nothing to build.

## What the page does

Three jobs, in order:

- **It hangs the shingle.** TechPointPro LLC, document systems and IT consulting, Clovis, California. My name, and the title that finally fits the LLC: Founder & Principal Consultant. One paragraph of receipts — Toshiba America, 26 years, warehouse to the Solutions Lab; certified DocuWare document-systems engineer after that.
- **It points at the two live properties.** A card for the book — *The Dark Fills the Space*, serialized free at netbob.org, cover art included — and a card for Field Report — this site — where the reports live. The shingle doesn't compete with the publications; it endorses them.
- **It publishes no contact details.** No phone, no email in the clear. A public page is forever and scrapers are patient; anyone who needs me already has a way, and the two linked sites have theirs.

## The locks, this time

A man who has had a domain stolen builds the fence before he admires the house. Registrar lock on, auto-renew on, DNSSEC on, two-factor on every account that can touch it. Five minutes of settings — the difference between a funny story about the time the domain was hijacked and a second hijacking.

## Three properties, three jobs

netbob.org is the book. mjmcshane.com — Field Report — is the bench journal. techpointpro.com is the brass plate by the door — the oldest name of the three, back from the dead, doing the smallest job on the smallest stack I own.

A shingle doesn't need a feed. It needs to not blow down.
