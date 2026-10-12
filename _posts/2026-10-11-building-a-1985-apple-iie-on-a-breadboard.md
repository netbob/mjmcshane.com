---
title: Building a 1985 Apple //e on a Breadboard
description: A ten-dollar chip, a Raspberry Pi 400, and the computer I owned in 1985, rebuilt one wire at a time
author: Michael McShane
date: 2026-10-11 21:30:00 -0700
categories: [Tech]
tags: [tech, '6502', raspberry-pi, retro]
pin: false
toc: true
---

## My path through the eighties

I started on a TI-99/4A, segued to an Apple //e, and was eventually
enticed away by an IBM PC running PC DOS 3.31. Three machines, three
philosophies, one kid learning that computers were understandable
things. The middle one is the one that never left me — and last
week, debugging an ultrasonic sensor on a breadboard for my
granddaughter, I realized the middle one could come back. Not as an
emulator. As silicon.

The processor is the give-away: Western Design Center still makes
the 6502's direct descendant, the W65C02S — the same lineage as the
65C02 in the Enhanced Apple //e of 1985. Ten dollars, forty pins,
plugs into a breadboard. This post is the field report's first
installment: what I'm building, what it costs, and why.

## The comparison that explains the project

| | Apple //e (1985) | Dell Inspiron 16 7640 (my desk) |
|---|---|---|
| Processor | 65C02 at 1.023 MHz | Core Ultra, ~4.8 GHz boost |
| Memory | 128 KB | 16 GB (131,072× more) |
| Storage | 140 KB floppies | 1 TB SSD (~7 million floppies) |
| Transistors | A few thousand | Billions |

The Dell wins every row by orders of magnitude, and I would not
trade it for the //e as a tool. But capability and comprehensibility
traded places somewhere in those forty years. The //e is the last
computer one person can understand *completely* — every wire, every
cycle, every transistor accountable. The Dell is a miracle no
single human fully knows. For getting work done, take the miracle.
For learning what a computer *is*, take the machine you can hold in
your head.

## The plan

The 65C02 sits on the breadboard. My Raspberry Pi 400 — already on
the bench from the sensor project — does three jobs through its
GPIO header:

1. **Clock.** The modern 65C02 is fully static: the Pi can clock it
   at 1 MHz, at one step per second, or one step per button press,
   and the chip waits patiently between ticks.
2. **Memory.** The Pi emulates RAM and ROM, holding each cycle
   while it services the access. The //e's beloved bank-switching
   becomes software instead of circuitry.
3. **Witness.** Every bus cycle gets printed — fetch, read, write —
   so the machine's thinking is on the big screen, in plain text.

It also runs at 3.3 volts, same as the Pi's logic, so the two talk
without translators. Parts ledger: the CPU ($8–12), an optional
W65C22 VIA for the chip's own peripherals ($7–10), EEPROM and RAM
if I later want it standalone (~$15), glue logic and a second
breadboard — call it **$50–80 all-in**. A working Enhanced //e on
today's market is $200–400, and it would never let me stop its
clock.

## What "done" means

Boots to a monitor prompt. Runs BASIC — the real thing, since
Applesoft was Microsoft BASIC underneath all along. Renders the
//e's 80-column text and hi-res graphics on the Pi's screen. Saves
and loads through the Pi. It will not be cycle-exact Apple hardware —
software that leans on the Disk II controller's tricks need not
apply — and that's fine. I lived at the prompt, not in the copy
protection.

And it has a second job, which is the actual reason it's on the
bench next to a 4th grader's sensor kit. My granddaughter thinks
she wants to be an engineer. This machine is the genesis of that
path if she chooses it: a heartbeat, numbered boxes, fifty
instructions, and the discovery that machines are understandable
and she's allowed to understand them. No assignment. An invitation
with blinking lights.

## The first program

Every build deserves a first program, and this one's was written
before the parts were ordered — it's the epigraph of the novel I'm
serializing across the street at netbob.org, in this chip's own
assembly language:

```
LDA DARK
STA SPACE
NOP
```

Three instructions. Load the dark, store it in the space, do
nothing — and watch the bus monitor prove the machine understood.
Parts go on order this week. Part 2 will be the free-run: a
processor, a clock, and nothing else, thinking out loud.
