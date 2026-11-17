---
layout: post
title: "Your Mail Is Not in the Cloud"
date: 2026-11-17 01:00:00 -0800
categories: [Tech]
tags: [Email, Maildir, Mutt, Privacy]
author: netbob
---

"The cloud" is a misleading phrase. It sounds like a place — a vast, reliable warehouse where your things are stored. It isn't. It's a server owned by someone else, running software you don't control, under terms that can change. When Microsoft 365 went down on November 12, every email address I own stopped working at once, because they all lived on Exchange Online. My mail wasn't "stored in the cloud." It was held on Microsoft's machines, and when those machines had a bad day, I had nothing.

That outage is what pushed me to move my mail home. Not to another cloud provider — to a directory on my own disk, in a format I can read with tools I control. The format is Maildir. The reader is Mutt. The pipe that keeps it current is mbsync. Here's what that looks like, and why it beats Outlook.

## One file per message

Maildir is almost embarrassingly simple. A mailbox is a directory. Each message is one file inside it. New mail lands in `new/`, read mail moves to `cur/`, and `tmp/` holds messages being written. That's it. No database, no index you can't rebuild, no proprietary container.

Compare that to the two formats most people actually live in. Outlook's .pst is a single proprietary file — a black box that only Outlook truly understands, and that grows until it becomes fragile. (My largest was 12.6 GB.) mbox, the Unix classic, is a single file per folder with every message concatenated into it; one corrupt byte can take the whole folder with it.

Maildir's bet is the opposite: if each message is its own file, nothing can corrupt anything but itself. You can back it up with rsync, grep it, move it, read it with any tool that understands files. It's email as files, and files are the one format that never goes out of style.

## Getting twenty years out of .pst

I had about 27 GB of mail in four .pst files, going back to 2006. Getting it into Maildir took two small Unix tools, both free, run from WSL2 on the same Windows machine that made the .pst files:

- `readpst` (from pst-utils) reads a .pst and writes out mbox files, one per folder.
- `mb2md` converts those mbox files into a Maildir tree.

The big file — mmcshane@outlook.com, 12.6 GB — came out with its counts intact: Inbox 48,151 messages, Sent 6,538. The smallest, netbob.org, came out at Inbox 405, Sent 22. The counts matched readpst's report exactly where it mattered, which is how I knew the conversion was sound. The whole archive now lives at `C:\Users\mmcsh\Maildir`, a directory I can copy, back up, and read from any machine.

## mbsync and Mutt: the live half

The archive is the past. For the present, new mail still arrives at my providers — Runbox for mjmcshane.com, Migadu for netbob.org. I don't read it there. I pull it down with mbsync, which speaks IMAP and writes to the same Maildir, under a separate `live/` subtree so it can't collide with the archive.

The configuration is deliberately one-directional: pull only. mbsync downloads and never deletes from the server. The server is a transit point, not a store — mail arrives, gets pulled down, and the local copy is the one that matters. Passwords come from Bitwarden's CLI, fetched at runtime, so no password ever sits in a config file. Sending still happens in Thunderbird; Mutt, in this setup, is a reader.

Mutt itself is the part I like best. It's a terminal client from an era when email was text, and it reads Maildir natively — no import step, no conversion. Open it and the inbox is there: 23 messages the first time I ran it, with the archive a keystroke away. It does one thing, it does it fast, and it stays out of the way.

## Better than Outlook

Outlook's pitch is convenience: your mail, everywhere, handled for you. The price is that your mail lives on someone else's infrastructure, in a format only they fully control, and when their infrastructure fails — as it did for me on November 12 — you have no mail at all. The "cloud" framing hides that dependency. It makes a service sound like storage.

Microsoft Outlook: Runbox explicitly does not recommend using the newer versions of Microsoft Outlook with IMAP/SMTP accounts. Recent iterations route mail traffic through Microsoft's cloud infrastructure rather than logging into your mail server directly, raising privacy and authentication concerns. (If you choose to use it anyway, you must manually configure the server settings).

The alternative isn't a different cloud. It's owning the storage. A Maildir on your own disk, a client that reads it directly, and a provider that becomes a replaceable pipe rather than a landlord. If Runbox or Migadu ever goes away, I change one DNS record and one mbsync line; my mail doesn't move, because it was never theirs.

That's the point of the exercise. Not to escape email, and not to build a fortress — to keep the part that matters (the messages, twenty years of them) in a form that outlasts any single provider. Maildir is that form. Mutt is the way I read it. And neither one answers to Redmond.
