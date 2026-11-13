---
layout: post
title: "Technician Quiz, Round 1: The Two I Got Wrong"
date: 2026-11-13 09:50:00 -0800
categories: [Tech]
tags: [Amateur Radio, Technician]
author: netbob
description: "First quiz round for the Technician license: 3 out of 5, and the two misses were both math."
---

I'm studying for the FCC Technician license — 35 questions, 26 to pass, every one drawn from a public pool of 409. This morning I took my first quiz round: five questions, electronics and propagation only, the parts that actually need memorizing. The rules and safety questions are mostly common sense.

Score: 3 out of 5. Both misses were math, not concepts. Here are the two I got wrong, and the theory behind the right answers.

## The resistance question (T5D04)

> What is the resistance of a circuit in which a current of 3 amperes flows when connected to 90 volts?
>
> A. 3 ohms / B. 30 ohms / C. 1/30 ohm / D. 270 ohms

I picked D — 270 ohms. That's 90 × 3. But 90 × 3 is power (270 watts), not resistance. Ohm's law is E = I × R, so to find resistance you divide:

```
R = E / I
R = 90 V / 3 A
R = 30 ohms
```

Answer B.

The Ohm's law triangle is the picture to keep in your head: E on top, I and R on the bottom. Cover the value you want and read off the rest. Cover R and you get E / I. Cover E and you get I × R. Cover I and you get E / R.

The trap in this question is that multiplication feels right — 90 and 3 are right there, and multiplying them gives a clean number. But if the question asks for resistance, you divide.

## The decibel question (T5B09)

> Which decibel value most closely represents a power increase from 5 watts to 10 watts?
>
> A. 2 dB / B. 3 dB / C. 5 dB / D. 10 dB

I picked D — 10 dB. That's the 10× rule: 10 dB means ten times the power. But 5 watts to 10 watts isn't ten times — it's a doubling. And doubling is always +3 dB. Answer B.

The formula:

```
dB = 10 × log10(P2 / P1)
dB = 10 × log10(10 / 5)
dB = 10 × log10(2)
dB ≈ 3 dB
```

The two rules to memorize:

| Power change | dB change |
|---|---|
| × 2 (double) | +3 dB |
| × 10 | +10 dB |
| × 4 | +6 dB |
| ÷ 2 (half) | −3 dB |
| ÷ 10 | −10 dB |

If the question says "double," the answer is almost always 3 dB.

## What the round taught me

The three I got right — the wavelength formula, the UHF horizon, the schematic — were all concepts. The two I got wrong were both arithmetic. So the math is the part to drill. I'm keeping one file per round with the answers and the theory behind each one, so the misses pile up into a drill sheet. The full Round 1 sheet is here: [Quiz Round 1 — Answers & Theory](/assets/files/quiz-round-1-2026-11-13.md).

The pool is public — the full 409-question Markdown file is [here](/assets/files/technician-question-pool-2026-2030.md) — and I'm studying on [hamstudy.org](https://hamstudy.org). Next round will lean harder on the math.
