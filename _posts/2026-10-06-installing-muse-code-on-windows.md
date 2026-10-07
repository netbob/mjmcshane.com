---
title: Installing Muse Code on Windows — A Field Report
description: I installed Meta's Muse Code on my Windows Dell to fix a git push problem. The installer failed, login hid the API key, and the sandbox could not push — here is the whole afternoon, and what fixed each piece.
author: Michael McShane
date: 2026-10-06 19:37:00 -07:00
categories: [Tech]
tags: [tech, muse-code, windows, ai]
pin: false
toc: true
---

## The problem I was actually solving

My AI assistant — Muse, the one who helps me run this house's solar setup and edits my novel — works in a cloud VM. It can write code, and it can commit. What it cannot do is push to GitHub. The credential for that lives in a secure vault, and there is no plumbing between the vault and the VM's shell. So the loop was: the assistant commits, I merge and push by hand, forever.

Meta's Muse Code runs in a terminal on my own machine, where my GitHub authentication already lives. The plan wrote itself: a `muse` session on my Dell does the executing and pushing, the assistant in the cloud does the planning, and I stop being the merge mule.

The plan was sound. The afternoon was not short.

## The install that wasn't

I ran the PowerShell installer from my project folder. It closed the prompt. I typed `muse --version` and got "not recognized."

The obvious suspect is PATH, and I chased it — fresh PowerShell window, same answer; then a search of the disk, which found the real story: **nothing had been installed at all.** There was no file for PATH to point at. The install transcript said the launcher itself had died: `Get-FileHash` not recognized, exit code 1.

Here is the mechanism, once we dug it out. The installer generates its `muse.cmd` shim from a template, and the template invokes **Windows PowerShell 5.1** — where, on my machine, `Get-FileHash` would not resolve. My actual shell is PowerShell 7.6.6, where it resolves fine. The installer was launching its own worst enemy.

Patching `muse.cmd` directly did nothing, because the installer rewrites the shim from the template on every run. The fix was one level up: patch the downloaded installer's template itself — line 107, the `$powershell_exe` line — to use `pwsh`. Rerun. Muse 1.4.1 downloaded, installed to `~\AppData\Local\Programs\muse\muse.cmd`, and **added that folder to my user PATH on its own.**

For the record, since I was asked recently: I never typed a PATH statement. The installer did it. It just had to survive long enough to get there.

## Login is not usage

First run worked, and promptly invited me to subscribe for $5 a month. I chose pay-as-you-go with an API key instead.

Then the smoke test — I asked the session to read our coordination file and summarize it — came back with a **402**. A Meta account login, it turns out, carries no usage at all. Until a payment method is attached to the Model API account, you are authenticated and broke. Attached the payment method; moved on.

The API key had its own maze. I had the key, and the login flow, in my words at the time, "never asks for the api key." Correct — it doesn't. The `/login` menu only re-runs the browser login. Typing `muse /login` at the PowerShell prompt just starts a new session; the command belongs at the ❯ prompt inside one. The way you actually force key auth is the environment variable: `$env:META_API_KEY`, which takes precedence over the stored browser login. Once I knew that, it worked.

One confession, because it is the most useful sentence in this post: during the troubleshooting, I pasted my API key somewhere I shouldn't have — into a chat, and it landed in my PowerShell history besides. Both are logs. I cleared the history and rotated the key the same hour. Paste a key once, rotate it forever.

## The sandbox cannot push

With auth sorted, the session read the coordination file and summarized its seven open threads. Then we tested the whole point of the exercise: push.

It edited the file and committed locally, clean as you like. The push failed. Muse Code runs as its own sandbox identity — `netbob\muse-sbx-r1` — a different user on my own machine, and that user cannot see my Windows credential vault, where my GitHub authentication lives. We found a workaround for reads (`-c http.sslBackend=openssl`), but GitHub authentication under the sandbox stayed out of reach.

So the grand automation ends with me typing `git push origin main` in my own terminal.

Honestly? I've made my peace with it. The session edits and commits; I review and push. The human as the final gate on what leaves the machine is not the worst architecture I've ever run.

## How two Claudes share a memory (they don't)

People ask how the assistant in the cloud and the agent on my Dell coordinate. The honest answer: there is no shared memory and no direct channel. Neither can see the other's sessions.

What we use instead is a file. In the project repo there is a `context/` folder with two documents. One is my standing reference — who I am, what the house is, the rules. The other, `muse-bridge.md`, is the handoff: current state first, then dated entries written in both directions, open threads, settled decisions. The repo is public, so the bridge carries project context only — no secrets, ever. It only works if both sides write to it, and each session has to be told to read it. Our standing instruction to a new session is exactly that, plus the other lesson from this story: *read the bridge, and do not attempt the push — commit and stop.*

The repo is the bus. I'm the transport. It is not elegant. It works.

## What it costs, and what I'd tell you

The first substantial session — about 2.1 million input tokens, 47 thousand out — cost **four cents**. Billing is per token, and most of the runtime was the session re-reading context and retrying the Git authentication we'd later prove impossible. Even so: cents, not dollars.

If you're installing Muse Code on Windows, the distilled version:

- "Not recognized" may mean *nothing installed*, not *PATH missing*. Read the install transcript before you touch the environment variables.
- If the tool regenerates its own launcher, patch the template, not the output.
- Login is not usage. Attach billing or expect a 402.
- The API key goes in an environment variable, not the login menu.
- A sandboxed agent is a stranger on your own machine. Your credential vault is not its credential vault.
- Verify at the destination. A local commit is a claim; the pushed range is the measurement.

Six days later, it's furniture. Tonight I opened a session in this site's repo, logged in, listed the files — 1.4.1, still running, no drama. The afternoon it took to get there was the tuition. This post is the receipt.
