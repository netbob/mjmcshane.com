---
layout: post
title: "Email Was Never Meant to Be a Filing Cabinet"
date: 2026-11-14 22:55:00 -0800
categories: [Tech]
tags: [Email, Privacy, Security, History]
author: netbob
---

My boss at Toshiba gave me a mandate: treat email as your filing cabinet. If a document mattered, save it in email too.

This was the cc:Mail and Lotus Notes era, and in that world the mandate made sense. Notes was a real database — a replicated document store that lived on the company's own servers, with access control and full-text search. Email wasn't a pipe in those days. It was the place where the documents lived.

The workflow was simple. My mail lived in a file called mmcshane.nsf. When it got too large, I copied it offline and started a fresh one. The copies became Backup_01.nsf, Backup_02.nsf, and so on. By the time I was let go in 2008, I was up to Backup_50.nsf. I still have them, in a virtual machine of my old Tecra M3 notebook.

The backups weren't only about size. The business unit I was in had nosy corporate types, and I understood that anything on the company's servers could be read by someone I didn't choose. Copying the .nsf offline was how I kept my own data mine. It was a file I controlled. I could take it with me. And I did — eighteen years later, I still have it, because it was in a file I owned. If that mail had only lived on a corporate Exchange server, it would be gone.

The habit outlived the architecture. That's the problem.

Exchange, Outlook, and Gmail are not Notes. The filing cabinet moved off my machine and onto someone else's servers. It's reachable from anywhere in the world with a password, and it's the first thing attackers go for. I kept the habit — if a document mattered, save it in email — and the archive kept growing. Today it's about 27 gigabytes across four mailboxes. The biggest, mmcshane@outlook.com, is 91% full.

Then Microsoft 365 went down on November 12, and the cabinet was locked for more than twelve hours. Every address I own runs on Exchange Online, so every one of them was hit. The mail wasn't lost — senders retry, and the messages waited in queues — but I couldn't reach any of it. The only local copies are the .pst files I exported the next day, 25.8 gigabytes of them, and I still don't have a confirmed second copy anywhere off the machine that made them.

The .pst files are the other half of the problem. They're the supposed equivalent of the .nsf — a local archive you can take offline — but they're clunky in a way the .nsf never was. A .pst is a fragile single-file store, tied to Outlook, and my two big ones are around 12 gigabytes each, which is the size where .pst gets slow and corruption-prone. The .nsf was a real database in a portable file. The .pst is a legacy format that was never designed to be a 12-gigabyte archive.

So the mission changed. Or rather, it split in two, and I finally saw the two halves clearly.

The first half is: don't lose the archive. The second half is: don't lose the ability to receive messages. I'd been trying to solve both with one mechanism — a chain of providers that would fail over from one to the next — and that's why it had so many moving parts. The chain was the wrong shape, because the two problems need different answers.

I keep coming back to packet radio for the shape of this. In packet radio, the station keeps its own log locally, and the network just moves packets. You don't run five radios on five different networks. You have one station, and the packet takes whatever path is open. The message and the medium are separate. The station's log doesn't live on the digipeater.

The equivalent here is three layers, and each one does one job.

The front door is Cloudflare Email Routing. It takes the mail for my domains and forwards it to wherever the live mailbox is. It stores nothing — Cloudflare is not an email host, it has no mailboxes, and it can't replace Exchange as the live mailbox. That's not a weakness. It's the point. The front door is a stable address with a swappable backend, and because it holds no mail, there's nothing to lose if it changes.

The live mailbox is one provider at a time. Right now the best fit is Fastmail — 60 gigabytes for $60 a year, an independent company, good IMAP, easy to leave. New mail lands here. It's transient. It's not the archive.

The archive is local, and this is the part that finally feels like Notes again. The modern equivalent of the .nsf is a format called Maildir, where each message is its own file in a directory tree. A small sync tool pulls mail from the live mailbox into a local Maildir on a schedule. When it gets big, you split it by year — Maildir-2024, Maildir-2025 — the same pattern as Backup_01.nsf. You back it up by copying the directory to another drive. It's portable, it's searchable, and it's yours. No provider can lock you out of it, because it doesn't live on a provider.

I wish Lotus Notes were in the public domain, or open source. It's not — HCL owns it, and it's a commercial product. But the idea at the center of it doesn't belong to any company: a local, portable, searchable store that you control. That idea is open, and it has a name now. It's Maildir.

The habit is changing. Documents go in a real store now, not in an email to myself. Email goes back to being what it was always best at: moving messages. The filing cabinet leaves email, and the cabinet is a directory on a drive I own, backed up to another drive I own — the same move I made with the .nsf files, pointed at Microsoft instead of Toshiba.

The first step is the unglamorous one: get a second copy of those .pst files off the machine that made them. Everything else follows from the archive being safe.
