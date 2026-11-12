---
layout: post
title: "When the Internet Goes Quiet"
date: 2026-11-12 15:36:00 -0800
categories: [Tech]
tags: [Amateur Radio, Packet Radio, Technician, Resilience]
author: netbob
description: "Microsoft 365 went down today, and my test emails to my own Outlook addresses never arrived. It got me thinking about how fragile the whole thing is — and why I'm studying for my amateur radio license."
---

Today Microsoft 365 went down. Not a rumor, not a blip — Exchange Online, the mailbox service behind Outlook, stopped answering late this morning, and by early afternoon more than 130,000 people had reported Outlook problems. I sent test emails to my own Outlook addresses. None of them arrived.

They're not lost. That's the thing worth saying first. Email is store-and-forward by design — the sending servers queue the messages and retry, and they'll land eventually, once Microsoft clears the backlog. The protocol, built in the 1970s and 80s, did its job. What failed is what we've built on top of it.

My mail all lives on one provider's infrastructure. Every address I own — the custom domains, the Outlook.com accounts — runs on Microsoft's Exchange Online. When their servers go down, every address goes down with them. The protocol is distributed. The mailbox layer isn't anymore. It's basically three companies holding most of the world's email, and today one of them fell over.

It made me realize how fragile the whole thing is. There should be a better, more fault-tolerant way to stay in touch — and there is one. It's just old.

I'm studying for my FCC Technician amateur radio license.

The exam is 35 multiple-choice questions, one drawn from each of 35 groups in a public pool of 409. You need 26 right to pass. No Morse code, no essay, no oral exam. The questions are published — you study the actual pool, not a guess at what might be asked. I once memorized the question pools for seven MCSE exams in a hotel in New Hampshire. Four hundred and nine ham questions is a weekend project by comparison.

What the license buys me is the right to transmit — and specifically, to transmit data. Packet radio.

Packet radio is the part of amateur radio that never went away, and it's having a small comeback. A packet is a discrete chunk of digital data with a source, a destination, and an error check. A digipeater — a radio, a small computer, and an antenna sitting unattended on a high site — hears a packet and repeats it onward. Because packets are addressed and acknowledged, you get things voice radio doesn't have: a station can hold a message and forward it later, when the recipient comes on the air or a path opens up. The sender and receiver never have to be on at the same time. There's no central server to seize, no single point of failure. The message gets there eventually, on its own schedule.

That's the resilience email used to promise and no longer delivers.

I want to build a packet radio station on the bench. The chain is simple: a computer, a TNC (terminal node controller), a radio, an antenna. The computer would be the 65C02 I'm already building on the breadboard — in the 1980s, packet stations ran off Apple IIs and Commodore 64s as the terminal, and my machine would play exactly that role. The TNC is the heart of it: a microcontroller that implements the AX.25 protocol and the modem, turning data into two audio tones. The radio is a 2-meter FM transceiver. The antenna is a J-pole made from copper pipe.

Clovis works for this. The Sierras rise to my east, but the valley spreads flat to the west, and Fresno is ten miles away across open ground. Packet radio ran in this valley in the 1980s — there was a packet BBS in Clovis itself, and a digipeater on Buck Rock at 8,500 feet in Kings Canyon. That network faded when the internet arrived. The APRS backbone is still there, on 144.390 MHz, and HF packet doesn't care about mountains at all.

There's a second reason, and it's the novel.

Zoe — the AI narrator of the book I'm writing — uses packet radio when the internet is dying. In the story, the centralized internet gets taken over, and the only way left to connect is the old, decentralized radio network. She commissions a packet radio digipeater as a side project, never expecting it to be needed. It becomes the lifeline. The prequel, set in 1985, has two kids — Cassandra in America, Mikko in Finland — talking across the Atlantic on modems and packet radio. The old tech becomes the future tech. I want the radio parts of that story to be right, which means I want to have done it myself.

So that's the goal: pass the Technician exam, get a call sign, and build a packet station on the bench. The study materials are below. If you've ever thought about getting licensed, the pool is public — start here.

- The full question pool, all 409 questions, as a Markdown file: [technician-question-pool-2026-2030.md](/assets/files/technician-question-pool-2026-2030.md)
- The official pool PDF from NCVEC, which includes the three schematic figures (T-1, T-2, T-3) that twelve of the questions refer to: [2026-2030 Technician Pool and Syllabus (PDF)](https://ncvec.org/downloads/2026-2030%20Technician%20Pool%20and%20Syllabus%20Public%20Release%20Feb%2019%202026.pdf)
- HamStudy.org, the free practice site most people use: [hamstudy.org](https://hamstudy.org)

I'll write about the bench build as it happens. First, the exam.
