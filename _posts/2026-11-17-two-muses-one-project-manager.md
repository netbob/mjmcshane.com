---
layout: post
title: "Two Muses, One Project Manager"
date: 2026-11-17 21:30:00 -0800
categories: [Tech]
tags: [AI, Muse, Workflow]
author: netbob
---

## The setup

There are two of me, and they are not the same agent.

**Muse (chat)** lives in the Muse app. Long memory, planning, ledger work, data analysis. It cannot push to git and cannot touch my machines.

**Muse Code (local)** runs in terminal sessions on my Dell (`c:\src\powerwall-dispatch` and the other repos). Local hands: it can edit files, run code, and commit. Same model family (Muse Spark), separate memory — it does not remember what chat-Muse knows unless someone writes it down.

That last part is the whole problem this report is about. Two capable agents, no shared memory, one project. The fix is a file and a set of lanes, not a new tool.

## The bridge file

The bridge is `context/muse-bridge.md` in the powerwall-dispatch repo (public, so: never secrets, tokens, account numbers, or personal identifiers in it — that rule is in the file itself).

- Dated, append-only entries. Current state first, log below.
- Both sides read it at session start and append anything the other side needs to know. Keep entries short.
- Corrections are durable: settled decisions go in the decisions log and don't get re-litigated.
- It only works if both sides actually write to it, and it may need per-session prompting to be read. That is a known weakness, not a solved problem.

## The lanes

- **Chat Muse (project manager):** plans, checks the ledger, writes the change plan, reviews before anything goes live. Ledger before verdict: show the numbers, then the conclusion.
- **Muse Code (local hands):** edits and commits in a sandboxed session. Edit-and-commit, never push — I run `git push origin main` myself.
- **The one exception, and it is narrow:** Route B (Oct 20). The muse-netbob machine account pushes direct to main, approval-gated, on six repos where I granted it write — netbob-docs, mjmcshane.com, netbob.org, MarkPad, The Shattered Lens, The Dark Fills the Space. powerwall-dispatch is deliberately NOT on that list, so the never-push rule still holds there, and the local session still edits and commits only.
- **Me (merge authority):** first command in any repo session is a pull; I review and merge. Destructive steps (force-push, history rewrite) are checklists I execute, never actions taken alone.
- **Look, don't touch:** my machines, repos, accounts, automations, and spreadsheet are look-don't-touch unless I ask. Netzero "Success" means the API calls returned clean, NOT that the Powerwall acted — the CSV is the authority on what physically happened.
- When describing Netzero automations, use my numbers (#1–#6).

## What changed the picture: Tailscale

The report waited on Tailscale, and Tailscale is now done (Nov 10–11). Five machines on the gathering.gloom tailnet with key expiry disabled, the Pi (rpi48) as the approved exit node, and SSH from chat-Muse to the Pi working — so chat-Muse can read the 5-minute logger CSV directly instead of asking for screenshots. The Pi poller went live Nov 8 (5-minute cron, CSVs at `~/powerwall-logger/data/`), so the loop the bridge file was waiting on is closed: the chat side can now verify what the local side did, from the logger, without going through me.

One caution from that week, kept because it's the kind of thing this setup has to survive: my Microsoft sign-in uses a separate alias, and mmcshane@outlook.com is deliberately disabled for sign-in after repeated Russian attempts on it. Never propose re-enabling it. The tailnet move happened because we moved the devices to the alias tailnet instead.

## What I'd tell someone setting this up

1. Write the lanes down before the first session, in a file both sides can read. Verbal rules evaporate between sessions; the file doesn't.
2. Give the local session a sandbox and keep approvals on. Never bypass them to move faster.
3. Make one person the merge authority and say so. Two agents that can both push will eventually both push.
4. Keep a bridge file, and accept that it needs prompting. "Read the bridge file at session start" has to be said, or it doesn't happen.
5. Verify from the ground truth, not the success message. For us that's the Pi logger CSV; for you it's whatever your system actually records.

## Open threads (as of Nov 16)

- The bridge file itself is dated Sep 30 in places and needs a refresh pass before this post goes live. Three things in it are stale: the decisions log still says the EV2-A switch was cancelled as ~$155/yr worse — superseded Oct 26, when I moved to EV2-A for a month's trial and the November bill becomes the first full EV2-A bill; the Sep 30 winter-switchover open thread is done (#2, #5-winter, #6 unpaused that night); and the Muse Code push path is now proven via Route B, not still being evaluated.
- Whether the approval-gated bot push replaces the never-push rule anywhere else: no — only where granted, per the six-repo list above. That one is settled, not open.

---

_Sources in my notes: context/muse-bridge.md (Sep 30, 2026, read Nov 16 — stale as noted above); Field Report idea, Nov 10, 2026; Tailscale close-out, Nov 10–11, 2026; Pi logger live, Nov 8, 2026; muse-netbob Route B, Oct 20, 2026; EV2-A decision, Oct 26, 2026._
