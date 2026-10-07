---
title: Two Sites, One Tree — Building netbob.org and mjmcshane.com
description: One forked Chirpy theme became two websites, the home of my novel and this tech site. A submodule outage, an iPad merge, a demo CDN, five build projects for one site, and a single colon that hid three chapters. The build log, with the code left in.
author: Michael McShane
date: 2026-10-06 19:53:00 -07:00
categories: [Tech]
tags: [tech, jekyll, cloudflare, websites]
pin: false
toc: true
---

## Why two sites

I write a novel in public, one chapter at a time, and I have forty years of tech lying around that deserves its own shelf. Mixing them on one site served neither, so: **netbob.org** for the book, **mjmcshane.com** for the tech. One stack for both, because I only ever wanted to learn one stack.

The stack is Jekyll with the Chirpy theme, hosted on Cloudflare Pages. The unusual part, and the source of half the lessons below: my repo isn't a site that *uses* the theme. It's a **fork of the theme's own repository** — the theme source is the site tree. That makes everything inspectable and everything my problem.

The entire publishing workflow is one line long. Push Markdown to `main`, Cloudflare builds:

```
RUBYOPT=-EUTF-8 bundle install && RUBYOPT=-EUTF-8 bundle exec jekyll build
```

…and the site is live about two minutes later. When it works. This post is about when it didn't.

## The outage: my memory repo broke my website

On October 1st I learned my site had been serving a **four-month-old build**. The last two production builds had failed, quietly, and Cloudflare kept serving the last good one. Nothing looked broken. It just wasn't *current* — which for a site publishing new chapters is the same thing.

The cause was mine. A commit had swept my nested personal `memory/` folder — itself a separate git repo, where it lives inside my site folder on disk — into the site's index as a **gitlink**: a pointer to another repository. Cloudflare's build clones with submodules, went looking for the submodule's URL in `.gitmodules`, and found nothing, because no URL existed. The build died with:

```
fatal: No url found for submodule path 'memory'
```

The fix was two moves:

```
git rm --cached memory
```

…plus one line in `.gitignore`:

```
memory/
```

Rebuild went green the same night. The rule is now permanent: **personal repos stay out of the site repo** — and `.gitmodules` (which defines the legitimate `assets/lib` submodule) is load-bearing. Delete it and you reproduce this outage exactly.

## The iPad lesson: git status doesn't phone home

Same week, second education. I edit on a Dell and an iPad (Working Copy). A chapter commit sat on the iPad *unpushed*, on a remote that hadn't synced since June — and `git status` said everything was fine, because **git status never touches the network.** It compares you to your local copy of the remote, and my local copy of the remote was four months old.

Pulling first surfaced the divergence, the merge stacked Chapter 2's closing line twice, and Chapter 3's front matter carried a date of `2026-20-01` — a month that does not exist — which failed the build until corrected. Working discipline since, written on the wall:

- **Pull before editing, on any device.**
- One device per file at a time.
- **Verify the live URL after pushing.** If it's 404 after five minutes, the build failed; read the front matter first.

## Traps inherited with a forked theme

Forking a theme means inheriting its demo configuration. Three finds:

- **The demo CDN.** My `_config.yml` pointed images at the theme author's demo host — one line, `cdn:` aimed at somebody else's Netlify. One comment character retired it.
- **The missing avatar.** The config referenced `/commons/avatar.jpg`. There was no `commons/` folder and no avatar. The sidebar rendered a placeholder until I dropped in an actual photo.
- **Five build projects, one website.** Through various experiments, *five* Cloudflare Pages projects were wired to build netbob.org on every push. Four were deleted (their names were homer, gert, delta, and ellie, if you're wondering how these things happen). **One Pages project per site** is the rule now.

## Site two, by photocopy

mjmcshane.com — this site — was a WordPress site for years, then a placeholder. Building it took an afternoon because it wasn't built; it was *copied*. The proven netbob.org tree, minus its history:

```powershell
cd C:\src\mjmcshane.com
if (Test-Path .git) { Remove-Item -Recurse -Force .git }
```

That `.git` deletion is the whole trick — skip it and the new repo inherits the old site's history and origin remote, and your first push goes to the wrong website. Then prune the theme-development boilerplate (`.github`, `.devcontainer`, `docs`, `tools`, the demo posts, the old `CNAME`), keep every structural file — `.gitmodules` above all — set the new identity in `_config.yml`, `git init`, new GitHub repo, new Pages project (`mjmcshane-com`), same build command verbatim.

The domain was still pointing at four legacy GitHub Pages A records. Those came out; a single CNAME to the Pages host went in; SSL lit itself. The novel's chapter template, which had ridden along in the copy, was shown the door — wrong site. By evening the tech site was live, waiting for something to say. (Its first two posts are an AI's essay and an installer post-mortem. The site has opinions already.)

The runbooks for all of this live in a **private** docs repo, not the public site tree — a Markdown file at a Jekyll repo's root gets served to the world, and I don't publish my own operating manual.

## The book gets a front door — and one colon hides three chapters

Last night the novel site got its book page: a new tab, the cover (three lines of 6502 assembly, glowing green, nothing else), and a chapter list generated from the posts themselves — no hand-maintained index to rot:

{% raw %}
```liquid
{% assign chapters = site.categories["Zo's Page"]
  | where_exp: "p", "p.title contains 'Chapter'"
  | sort: "title" %}
```
{% endraw %}

Zero-padded chapter numbers sort into reading order for free. It worked beautifully — for exactly one chapter. The other three had vanished from the list, lost their titles, and fallen back to ugly dated URLs. The bug was in descriptions I had just edited, on lines like this:

```yaml
description: Ch 1: Chapter 1 of The Dark Fills the Space, a collaborative novel…
```

A colon followed by a space inside an unquoted YAML value is not punctuation; it's a syntax error, and it invalidated the entire front matter of three files at once. One character per file — colon to hyphen — restored everything. **Front matter is code.** Proofread it like code.

The companion trap, same evening: the book page's browser title rendered empty. The theme builds a tab's title by looking the page's own title up in a locales file, lowercased — `tabs[page.title | downcase]`. My page was titled "The Book," so it went hunting for a key called `the book`, which will never exist. The page title is now simply `Book`, the locales file has the entry, and the title renders *The Book | netbob.org* — the theme had a design; I just had to stop fighting it.

## The rules, distilled

- One Pages project per site. `.gitmodules` is load-bearing.
- Personal repos never enter the site repo. `.gitignore` is a fence, not a suggestion.
- Pull before editing; `git status` does not phone home; **verify the live URL after every push.**
- A forked theme ships with the author's demo settings. Read your own config like an auditor.
- Runbooks live in private docs. The public tree is the product, not the manual.
- Front matter is code. A colon is a syntax error wearing a trench coat.

Two sites, one tree, zero regrets — and every scar above is now load-bearing documentation.
