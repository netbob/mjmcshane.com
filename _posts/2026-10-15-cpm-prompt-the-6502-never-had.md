---
layout: post
title: "A Prompt the 6502 Never Officially Had"
description: "CP/M belonged to Digital Research, not Microsoft - and two clean reimplementations bring its A prompt to the 6502, copyright gotchas not included"
author: Michael McShane
date: 2026-10-15 12:25:00 -0700
categories: [Tech]
tags: [tech, '6502', retro, cp-m]
pin: false
toc: true
---

The most famous prompt in early microcomputing is `A>`. It belonged to CP/M, Digital Research's operating system, and CP/M ran on the 8080 and the Z80 — which means it officially never existed for the 6502 at the heart of my breadboard build. The Apple II got its CP/M the way it got most Z80 things: a Microsoft SoftCard with a second processor on it, doing the work the 6502 couldn't be asked to do.

Which raises a licensing-flavored question I keep meeting on this project. Applesoft, the //e's native tongue, is Microsoft's code, and baking it into a homebrew machine carries paperwork. Does a 6502 CP/M carry the same problem?

No — twice over, as it turns out. CP/M was never Microsoft's to begin with. And the 6502 versions that exist aren't Digital Research code at all.

## The one from the era: Lausberg's CP/M-65

Dietrich Lausberg built a CP/M-inspired system for his Elektor Junior Computer decades ago and maintains it still, published on GitHub. It is shaped exactly like the real thing, because he built it in the real thing's image:

- **BIOS** (~3K) — the hardware layer
- **BDOS** (2K) — the kernel
- **CCP** (1K) — the console that gives you the prompt

Disks use CP/M-style `d:filename.ext` naming with a directory format that standard tools can still read; programs are `.COM` files loaded at $0200 and run. The software shelf is the part that convinces me it's a life's work: an assembler, a BASIC, FORTH, XMODEM, utilities by the dozen. It's a reimplementation of CP/M's *interface* — the BDOS calls, the file model — written for the 6502. The one catch for a borrower: it's married to his hardware, a 6532 timer and his BIOS assumptions. Porting it is a project, not an afternoon.

## The modern one: Given's CPM-65

David Given's CPM-65 is the same idea executed as a contemporary open-source project: a from-scratch CP/M for the 6502, same BDOS interface, with the BIOS layer written to be retargeted — and ports across the classic 6502 machines, Apple II-class hardware among them. No Digital Research code, no Microsoft code, paperwork clean enough to frame. For a breadboard machine that will eventually want to stand alone, that portability is the whole point.

## The honest boundary

"CP/M-compatible" describes the operating system — the prompt, the file calls, the `.COM` loading model. It does not conjure the library. WordStar, Turbo Pascal, dBASE II: those are Z80 machine code, and no 6502 will ever run them. What runs under a 6502 CP/M is software built for it — the assemblers, editors, and utilities its authors wrote and ported. You get the genuine `A>` experience and a working disk operating system of the period. You do not get WordStar. I find I can live with that.

And for the record, even *genuine* CP/M is less encumbered than its reputation: in 2022 the rights holder put in writing that CP/M may be used, copied, modified, and distributed — closing a licensing ambiguity the hobbyist world had worked around for decades.

## Why it's filed under this build

My breadboard //e has a licensing shadow over its endgame: Applesoft is the personality I want, and Applesoft is Microsoft's. The staged answer so far has been a Wozmon-style monitor, then an open BASIC. CP/M-65 adds a second road to the standalone phase — the machine booting not to `]` but to `A>`, running a period operating system whose every line I have the right to use.

That's not a software decision. That's a *story*: the breadboard computer that runs the operating system its chip was never invited to. When the standalone phase comes, that's the chapter I want to write.

*LDA DARK. STA SPACE. NOP — and then, DIR.*
