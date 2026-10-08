---
layout: post
title: "Standing Orders — AGENTS.md and the GitHub 101 I Wish I'd Had"
date: 2026-10-07 21:57:00 -0700
description: "How a per-repo rules file taught my coding agent the house rules, and the three distinctions (login, session, workspace; commit, push; rules, instructions) that nobody explained when I was learning GitHub."
author: Michael McShane
categories: [Tech]
tags: [tech, github, muse-code, ai]
toc: true
pin: false
---

## The question I asked

Tonight at 8:31 PM I asked my chat-side Muse a question that tells you exactly where my mental model was:

```powershell
c:\src\mjmcshane.com\muse /login %muse.md%
```

I wanted the Muse Code session on my Dell to start up already briefed — memory file loaded, house rules known, no re-explaining. What I typed was a small museum of wrong assumptions: a path where a command belongs, `%variable%` syntax from the cmd era in a PowerShell window, and a login step treated like the front door to everything. None of those is how it works. Finding out how it *does* work took one evening and fixed gaps that go back to when I was learning GitHub in the first place.

## What I actually wanted

The repo that matters is `powerwall-dispatch`, the public repository where my Powerwall automation project lives. It has a two-file memory system: `context/MUSE.md` (standing reference) and `context/muse-bridge.md` (dated handoffs — current state first, log below). The bridge is the only channel between the chat-side Muse that plans with me and the local Muse Code sessions that edit and commit on the Dell.

Since September 30 I'd been briefing every local session by hand: read the bridge, don't attempt the push, here are the invariants. What I wanted was for the repo to brief its own sessions.

## The mechanism: standing rules

Muse Code loads standing rules at session open from `.agents/AGENTS.md` in the workspace. Meta's own cookbook says so in one sentence, and `muse init` will scaffold the file. The key design point, which I got wrong in my first instinct: **the rules file holds orders, not memory.** Memory changes weekly; orders shouldn't. So the file is short, and mostly it points:

```markdown
## At session start
Before doing anything else, read:
- context/muse-bridge.md — current state, open threads, settled decisions
- context/MUSE.md — the owner's standing reference

## Working rules
- NEVER run git push. You run as a sandbox identity that cannot reach the
  owner's GitHub credentials; pushes fail and burn the session.
  Commit and stop. Michael reviews and pushes.
```

Rules in `AGENTS.md`, living memory in the bridge, the bridge itself versioned in the repo. Nothing to load by hand because there is no loading step — the harness reads the file before your first prompt.

## Three distinctions GitHub 101 never gave me

**Login is not a session is not a workspace.** Login is the account: persistent, machine-wide, and it follows you. A session belongs to the folder you launch it in — that folder decides which rules load and where the session can work. My question "do I need to log out to change repos?" had it backwards. `/logout` signs out of the account, which is never the move. `/exit`, `cd` to the next repo, run `muse` again. New session, new rulebook, same login.

**Commit is not push, and the split is a security design, not an inconvenience.** A commit is local bookkeeping — no credentials involved. My local sessions run sandboxed as `netbob\muse-sbx-r1`, deliberately unable to reach my Windows credential vault, and they can commit all day. A push publishes under my name to a public repository, so it requires my credentials — which the sandbox can't produce. At first I filed this under "tooling gap." It's better understood as the review gate: the agent prepares, I inspect the diff, I sign. You want exactly one of those steps to require the human.

**Standing rules outrank the instructions of the moment.** The first verified session read the bridge, as ordered — and the bridge, written September 30, contained a proposed assignment: *commit and push this file.* The session committed, and held the push, citing the standing rule, and asked me to call it. A week-old instruction in a log file does not override a standing order. That hierarchy — rules above tasks, both of them written down in the repo — is the closest thing I've seen to how you'd brief a careful human contractor.

## The receipt habit

I didn't assume the files loaded. In each repo I asked the same question — *what standing rules did you load?* — and read the summaries against what I'd written. Three repos, three faithful briefings:

- `powerwall-dispatch`: rules, bridge catch-up, and the hook protocol note, commits `b208b21`, `380e727`, `1479941` — pushed.
- `mjmcshane.com`: commit `253ae37` — committed and pushed.
- `netbob.org`: commit `c62780d` — whose message is, verbatim, a sentence I typed in chat that evening: "mkdir .agents and in that folder, AGENTS.md." Provenance doesn't get more honest than that.

Everything above is verifiable on GitHub, which is rather the point of keeping the records there.

## One honest footnote

The repo's pre-commit hook — a Python script that scans staged changes for secrets, installed after a history purge in September — cannot run inside the sandbox. Python itself is denied there. The session's handling is the protocol until a shell-based version exists: read the hook, check the staged diff against its patterns manually, commit with `--no-verify`, leave the hook untouched, and *disclose the bypass in the report*, then write the limitation into the bridge so the next session walks in knowing. A guard that can't execute isn't a guard. But a disclosed workaround with a paper trail is an honest system, and my own native commits still run the real hook.

## What I'd hand my GitHub-101 self

- A repository can carry its own instructions. Put the standing orders in the repo, versioned with the code they govern.
- Point, don't paste. Keep the rules file short and stable; keep changing facts in a dated log the rules point at.
- Per-repo means per-repo. Start the session in the repo you're working on; there is no master session.
- Let the agent commit. You push. A push is a signature, not a chore.
- Ask for the receipt. "What did you load?" is a complete verification protocol in five words.

At GitHub 101 I thought a repository was where the code lives. Tonight it briefed three AI sessions, kept the minutes of how it did it, and refused — politely, in writing — to let one of them exceed its orders. The code lives there too.
