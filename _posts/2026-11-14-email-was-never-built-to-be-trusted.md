---
layout: post
title: "Email Was Never Built to Be Trusted"
date: 2026-11-14 21:45:00 -0800
categories: [Tech]
tags: [Email, Security, Internet History, Privacy]
author: netbob
---

The question came up while I was sorting out the aftermath of the Microsoft outage: where did email actually come from, and why is it so fragile? The answer turns out to be a story about a myth, an accident, and a group of people who saw the problem coming thirty years before the rest of us did.

## The nuclear war story is mostly a myth

The version most people hear is that the internet was built to survive a nuclear war — a DARPA project, designed so the military could keep communicating after the bombs fell. There's a grain of truth in it, but the project it describes isn't the one that became the internet.

In the early 1960s, Paul Baran at RAND really did design a distributed, packet-switched network meant to survive attack. That was a real project with a real military purpose. But ARPANET — the network that became the internet, funded by ARPA in 1969 — had a different job: sharing expensive computing resources between research institutions. A researcher at UCLA using a mainframe at Stanford. That was the point. Packet switching also came independently from Donald Davies at the UK's National Physical Laboratory, who coined the term.

ARPANET's distributed design did make it resilient. But that was a consequence, not the goal. TCP/IP came later — Cerf and Kahn in the 1970s, ARPANET switched over on January 1, 1983 — and its goal was internetworking, connecting disparate networks, not surviving war.

## Email was an accident that became the killer app

Email started on single machines. In 1965, MIT's CTSS time-sharing system had a MAIL command so users on the same mainframe could leave each other messages. In 1971, Ray Tomlinson at BBN sent the first message between two hosts on ARPANET, and picked the @ sign to separate the user from the host.

It wasn't ARPANET's purpose at all. But it quickly became the dominant traffic on the network. The standards followed: RFC 822 for message format and SMTP in 1982, then MIME, IMAP, and POP3.

And here's the part that matters: email was designed for a small, trusted network where everyone knew each other. So SMTP has no built-in authentication — anyone can claim to be anyone, which is why phishing and spoofing are structural, not bugs. No encryption, because nobody on ARPANET needed it. No spam protection, because there was no spam. SPF, DKIM, and DMARC are all patches bolted on thirty years later, and they're still not universal.

## The centralization is a second-order effect

Email is federated in principle — anyone can run a server, SMTP is open. But in practice the big providers dominate, because deliverability is the gate: spam filtering, IP reputation, and ISPs blocking port 25 make it nearly impossible for a small independent mail server to get its mail accepted. That's how all five of my addresses ended up on Exchange Online, and why one outage on November 12 took them all down. The protocol is decentralized. The ecosystem isn't.

## The hackers saw it first

The people who understood email's weaknesses earliest didn't try to fix email. They assumed the network was hostile, built their own layer on top, and never trusted the infrastructure.

Compartmentalization first: different identities for different things, no cross-contamination. The real identity never touches the handle.

PGP for anything that matters. Phil Zimmermann released Pretty Good Privacy in 1991 precisely because email was plaintext and unauthenticated — end-to-end encryption plus a web of trust instead of a central authority. The US government investigated him for "exporting munitions" because the crypto was that strong. It never went mainstream because it's hard to use, but it's still the standard for people who take email security seriously.

Anonymous remailers, then Tor. In the nineties, before Tor, there were remailers — anon.penet.fi, Mixmaster, Mixminion — that stripped identifying headers and bounced mail through multiple hops, so no single server knew both sender and recipient. Tor, from the Naval Research Lab with a public release in 2002, generalized the idea. Then Tails, an operating system that routes everything through Tor and leaves no trace on the machine, and Qubes OS, which compartmentalizes via virtual machines so a compromise in one task can't reach the others.

And the metadata. The hackers knew the content was only half the story — who you talk to, when, how often is often more revealing than what's said. That's why Tor and the remailers exist: they hide the metadata, not just the content. The sensitive conversations never go over email at all. Signal, XMPP with OTR, Briar. Email is for the disposable, the public, the low-stakes.

The cypherpunk movement in the nineties — Eric Hughes' 1993 manifesto, "privacy for the weak, transparency for the powerful" — was explicitly about building these tools because the mainstream systems couldn't be trusted. They didn't try to fix email for everyone. They built tools for people willing to learn them and accepted that most people wouldn't.

## The dark web, and Swartz

The dark web's purpose is anonymity, not information access. Tor hidden services let you publish and communicate without revealing who or where you are. That enables whistleblowing and journalism — SecureDrop, the system newsrooms use for anonymous sources, runs as a Tor hidden service — and it also enables illicit markets.

Aaron Swartz wasn't a dark-web figure. His fight was open access to publicly funded research. But here's the real connection: Swartz worked on DeadDrop, the system that became SecureDrop. He was directly in that tradition — building a way for sources to reach journalists without email's metadata trail. The shared root is the same ethos: distrust centralized control, information should be free, build your own infrastructure when the mainstream one fails you.

## What you can actually do

You don't need to live on Tor. The principles scale down:

Own your domain, so you can move providers. Route mail through an independent layer — I'm using Cloudflare Email Routing. Keep a second provider. Keep a local archive. Encrypt what matters — my secure-contact form uses PGP for exactly this reason. Use a password manager and hardware two-factor.

That's the individual's defense against centralization, and it's the right one. The protocol won't save you, so you build the redundancy yourself. Assume the network is hostile, and add your own layer. The hackers were right about that much.
