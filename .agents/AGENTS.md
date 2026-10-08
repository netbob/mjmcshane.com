# Standing orders — mjmcshane.com

## What this repo is
The owner's tech site: Jekyll + Chirpy, in a fork of the theme's own repo
(the theme source IS the site tree). GitHub: netbob/mjmcshane.com.
Cloudflare Pages project: mjmcshane-com — the only one for this site.
Push to main = live in about two minutes.
Genre: first-person field reports from this house, code shown in fences.

## Working rules
- NEVER run git push. You run as a sandbox identity that cannot reach the
  owner's GitHub credentials; pushes fail and burn the session.
  Commit and stop. Michael reviews and pushes.
- Pull before editing. One editing session per file at a time.
- After Michael pushes, the live URL is the verdict: a 404 five minutes
  after a push means the build failed — suspect front matter first.

## Front matter is code
- An unquoted YAML value must never contain a colon followed by a space.
  It invalidates the whole block (three chapters on the sister site lost
  their titles and categories to exactly this). Use a hyphen, or quote it.
- Dates must be real calendar dates, format YYYY-MM-DD HH:MM:SS -07:00.
- New posts follow _posts/_post-template.md.
- Bylines: the author value is an ID looked up in _data/authors.yml, not
  a display string. It must exist as a key there or the byline renders
  blank. Current keys: netbob, Michael McShane, Muse.

## Code samples
- Fenced blocks take a language tag (yaml, powershell, python, liquid...).
- Any sample containing Liquid MUST be wrapped in {% raw %} ... {% endraw %}
  around the fence, or Jekyll executes the sample during the build
  instead of printing it.

## Load-bearing files
- .gitmodules defines the assets/lib submodule. Never delete it —
  that reproduces the Oct 1, 2026 outage exactly.
- memory/ stays out of this repo (it is gitignored). It is a separate
  personal repo that merely lives nearby on disk.

## Hard limit
This repo is PUBLIC. Never write secrets, tokens, API keys, account
numbers, or personal identifiers into any file here.
