---
layout: post
title: "Three BASICs, One Chip"
description: "Integer BASIC, Applesoft, and Commodore BASIC all ran on the same 6502 - one written by hand, one finished by Apple, one bought cheap and left stock"
author: Michael McShane
date: 2026-10-15 11:35:00 -0700
categories: [Tech]
tags: [tech, '6502', retro, basic]
pin: false
toc: true
---

I am building a 1985-style Apple //e on a breadboard, around a W65C02S — the modern descendant of the 6502. A fair question came up at my own bench: the 6502 also powered the Commodore machines, and the Apple II had *two* BASICs of its own. Same chip, three languages. How do they actually differ?

It turns out the answer is a story about authorship.

## Integer BASIC — the one written by hand

Steve Wozniak wrote Integer BASIC himself, in assembly, largely on paper. It is exactly what the name says: **integers only**, 16-bit, no floating point anywhere. Division truncates. Strings were rudimentary — you sliced them by position rather than manipulating them with functions:

```
10 A$="BREADBOARD"
20 PRINT A$(1,5)
```

That prints `BREAD`. Primitive — and *fast*. With no floating-point machinery to haul around, Integer BASIC ran integer work, games especially, noticeably quicker than the language that replaced it. It shipped in ROM in the original Apple II in 1977 and was displaced from the II+ onward. The Enhanced //e I am recreating doesn't even carry it.

## Applesoft — Microsoft's engine, Apple's finish

Applesoft is Microsoft 6502 BASIC underneath: 40-bit floating point (about nine significant digits), integer variables with a `%` suffix, full string handling, and `ONERR GOTO` error trapping. It carries the Microsoft family traits — including the famous one that only the **first two characters** of a variable name mean anything:

```
10 FISH = 42
20 PRINT FINGER
```

That prints `42`. `FISH` and `FINGER` are the same variable as far as Applesoft is concerned.

What made Applesoft *Applesoft* is that Apple paid to have the machine wired into the language. Graphics are commands, not memory addresses:

```
10 HGR : HCOLOR= 3
20 FOR X = 0 TO 279 STEP 4
30 HPLOT X,0 TO 279-X,191
40 NEXT X
```

`HGR`, `HPLOT`, `DRAW`, shape tables, lo-res `PLOT` and `HLIN` — the //e's personality, spoken natively. Even DOS commands arrived through a BASIC idiom, `PRINT CHR$(4);"CATALOG"`. The price of all that floating-point furniture: slower than Integer BASIC at integer work, and a string garbage collector that could pause a busy program while it tidied up.

## Commodore BASIC — the same engine, bought cheap and left stock

Commodore licensed the *same* Microsoft 6502 BASIC — famously for a flat one-time fee, reported at $25,000, no royalties — and then essentially never paid to modernize it. The BASIC V2 in a 1982 Commodore 64 is the 1977 interpreter wearing a new name badge: same floats, same two-letter variable names, same `?SYNTAX ERROR`, same leisurely garbage collection.

The consequence is one of computing's great ironies. The C64 was sold on its graphics and its SID sound chip, and its BASIC contains **no graphics commands and no sound commands at all**. You want a black border and background? Memory addresses:

```
POKE 53280,0 : POKE 53281,0
```

You want sound? `POKE 54296,15` for volume, then a page of further POKEs to shape a note. A generation of Commodore kids learned computing as a POKE table — or bought Simon's BASIC to get the commands the machine deserved. In fairness, Commodore BASIC had one jewel Applesoft never matched: `TI$`, a built-in clock you could simply print. And the C64 boots to a generous **38911 BASIC BYTES FREE**.

## Why this matters on my breadboard

Three outcomes from one Microsoft codebase, decided entirely by what each buyer did after the check cleared. Wozniak hand-built a sprinter with no arithmetic beyond integers. Apple took the Microsoft engine and finished it into a machine language — Applesoft *is* the //e's personality, which is why Phase 3 of my build aims at it. Commodore bought the same engine at a discount and shipped it raw for a decade.

There is a practical wrinkle, and it shapes my project: Applesoft's personality is Microsoft's copyrighted code. The ROM images aren't mine to bake into a breadboard machine and call it honest, so the plan routes around it — a Wozmon-style monitor first, and an open Microsoft-derived BASIC (EhBASIC) or a clean reconstruction for the floating-point era. The chip on the breadboard won't know the difference. But I will — and now, so will anyone who has read this far.

*LDA DARK. STA SPACE. NOP.*
