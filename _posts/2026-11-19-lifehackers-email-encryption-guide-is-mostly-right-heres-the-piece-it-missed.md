---
layout: post
title: "Lifehacker's Email Encryption Guide Is Mostly Right — Here's the Piece It Missed"
date: 2026-11-19 15:00:00 -0800
categories: [Tech]
tags: [Email, Encryption, Privacy, Security]
author: netbob
---

Lifehacker ran [a guide to encrypting your email](https://lifehacker.com/tech/these-are-the-best-ways-to-encrypt-your-email) on November 13. I read it the way I read any mainstream security advice now: against what I actually did when I set up signing in Thunderbird last week. Verdict: mostly right, with one overstatement and one omission that matters.

## What it gets right

The core explanation is sound. TLS encrypts mail in transit, but it's hop-by-hop — stripped at each server, processed in plaintext, re-encrypted on the way out. Encryption at rest doesn't stop the provider from reading your mail, because the provider holds the key. Gmail's Confidential mode and Outlook's Encrypt feature are not end-to-end encryption, because Google and Microsoft still manage the keys. Proton Mail and Tuta are end-to-end encrypted by default, but only between users of the same service; writing to a Gmail user takes password protection or a PGP tool. And the caveats are honest: metadata like subject lines and addresses can stay in plaintext, encrypted mail is still phishable, and forwarding breaks the encryption.

That's all correct, and it's the same ground I covered in [Email Was Never Built to Be Trusted](/posts/email-was-never-built-to-be-trusted/) — the protocol was designed for a trusted network, and the encryption is a patch on top.

## The overstatement

The piece says enterprise users of Google Workspace and Microsoft 365 "have access to true end-to-end encryption without third-party add-ons." The Google half is fair — Workspace client-side encryption is real, for the enterprise tiers that offer it. The Microsoft half is not. Microsoft's equivalent is Double Key Encryption, and it's an E5-only feature that takes real setup — it's not something a general Microsoft 365 user has. Presenting it as a standard enterprise benefit overstates what's actually available.

## The omission

The guide's tool list is all add-ons and new services: PreVeil, SecureMyEmail, Virtru, Mailvelope, FlowCrypt, plus Proton and Tuta. What it never mentions is Thunderbird. Thunderbird has OpenPGP built in — no add-on, no new account, no subscription. You generate or import a key, check two boxes, and your mail is signed (or encrypted) from the address you already have. I wrote up the whole setup as a [Guide](/posts/sign-your-mail-with-gpg-in-thunderbird/) last week, and the test mail came through signed. It's the simplest free path to doing what the article describes, and it's absent from the list.

(There's also one garbled sentence about Proton's Gmail integration — a copy-editing slip, not a factual error, but it made me read the rest twice.)

## The bottom line

Lifehacker's bottom line is the same as mine: email wasn't designed to be highly secure, and end-to-end encryption adds a layer of privacy if you set it up, but it doesn't fix the trust problem. That's right. The piece is worth reading. Just don't take the Microsoft claim at face value, and don't assume you need a new service or a paid add-on to start — the tool you may already have does it.
