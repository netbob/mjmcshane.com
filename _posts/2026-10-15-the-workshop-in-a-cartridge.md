---
layout: post
title: "The Workshop in a Cartridge"
description: "The TI-99/4A Editor/Assembler turned a home computer into a development system - the 6502 world answered in pieces, and my breadboard build inherits all of them"
author: Michael McShane
date: 2026-10-15 12:40:00 -0700
categories: [Tech]
tags: [tech, '6502', retro, assembler]
pin: false
toc: true
---

My first computer was a TI-99/4A, and the cartridge I still remember as a serious object was Editor/Assembler. Calling it a cartridge undersells it. It was a *package* — cartridge (PHM 3055), diskettes, and a manual with real weight — and it presumed a grown-up system around it: the 32K memory expansion and at least one disk drive. What it bought you was the whole workshop in one box: an editor, an assembler that produced relocatable object code, and a relocating linking loader that could resolve references between separately assembled pieces. On a home computer of that era, that was not a utility. That was a profession arriving by mail.

So a fair question for the W65C02S breadboard build on my bench: did the 6502 world ever have anything like it?

Yes — but characteristically, it answered in pieces, from different people, at different prices.

## The beloved one: S-C Assembler

Bob Sander-Cederlof's S-C Assembler (later the S-C Macro Assembler) was the tool half the Apple II world learned assembly on, and its trick was residency. Editor and assembler lived in memory *together*, with your source code alongside them — on a 48K machine, source programs of over 24,000 bytes could be handled entirely in RAM. No disk shuffle between editing and assembling: change a line, re-assemble, run it, change it again. That tight loop is exactly what the TI package promised, delivered by keeping everything in the room at once. Sander-Cederlof then documented the craft monthly in his *Apple Assembly Line* newsletter, which is why so much period 6502 code reads the way it does.

## The professional one: Merlin

Glen Bredon's Merlin, published by Southwestern Data Systems — later Roger Wagner Publishing — was the heavyweight: a full macro assembler for the Apple II under DOS 3.3, then ProDOS, with an integrated editor and a disassembler called Sourceror that could work backward from object code (it could even generate a commented disassembly of Applesoft from your own ROM). Merlin kept pace with the silicon: versions followed the 65C02, and a 16-bit successor, Merlin 16, served the IIGS generation. If S-C was the workshop you learned in, Merlin was the one you billed hours from.

## The one built into the machine

Underneath both sits the smallest answer, and Wozniak wrote it himself: a mini-assembler in the Apple II's monitor ROM — no symbols, just absolute addresses and constants, entered from the monitor at `F666G` to an exclamation-point prompt. On the Enhanced //e — the machine my breadboard recreates — it is always there, no disk, no cartridge, no load time. Type a line, it assembles in place; list memory, the built-in disassembler shows you what you made.

It carries one catch that matters directly to my build: the Enhanced //e's mini-assembler does **not** recognize the 65C02's new instructions. It speaks the original 6502 and stops there — on a chip that knows more than its own pocket assembler does. My W65C02S will inherit that exact quirk if I give it a //e-style monitor, and Phase 1 planning now has it written down: the mini-assembler is for the classic instruction set; the new opcodes go through the cross-assembler.

## How the job splits on my bench

The TI package bundled editor, assembler, and loader into one purchase because there was nowhere else for the work to live. My breadboard splits the same three jobs across forty years of tooling:

- **The heavy assembling** happens off-board, with **ca65** — the macro assembler in the cc65 suite, running on the Pi or the PC. It knows the 6502, the 65C02, and the 65816, produces relocatable code, and pairs with a real linker. This is the cartridge's assembler, grown up and living on the host.
- **The on-machine inspection** is the monitor's job — hex entry, disassembly, single-stepping — the mini-assembler's role, at the mini-assembler's scale.
- **The self-hosting endgame** is already on the shelf: Lausberg's CP/M-65 carries its own assembler among its utilities, so the standalone phase of this build could one day edit and assemble *on itself* — no host, no cartridge, the machine as its own workshop. That is the Editor/Assembler feeling, arrived at from the other direction.

```
        .segment "CODE"
start:  lda #$01        ; the seed instruction, cross-assembled
        sta $0200
        brk
```

The TI cartridge taught me what a development system felt like before I had words for it: the machine stops being an appliance and becomes a place where machines get made. The 6502 never sold that feeling in one box. It scattered it — a newsletter author's co-resident assembler, a professor's macro assembler, a pocket assembler from Wozniak in ROM — and left you to assemble the workshop yourself.

Which, on a breadboard, is more or less the assignment anyway.

*LDA DARK. STA SPACE. NOP.*
