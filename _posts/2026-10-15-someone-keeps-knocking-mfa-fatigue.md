---
layout: post
title: "Someone Keeps Knocking — MFA Fatigue and the Alias That Stops It"
description: "My phone kept lighting up with Microsoft Authenticator requests I never made. Changing my password did nothing. The fix was not a better password — it was making my email address stop working as a sign-in name."
author: Michael McShane
date: 2026-10-15 21:55:00 -0700
categories: [Tech]
tags: [tech, security, microsoft, authenticator]
pin: false
toc: true
---

My phone kept lighting up with Microsoft Authenticator requests I never made. Approve or deny, for a sign-in I had not started, on an account I was not using at the time.

I did the thing you are supposed to do. I changed my password — a long, fresh one. The requests kept coming, exactly as before.

That failure is the clue, and it took me longer than I care to admit to read it correctly: **nobody was guessing my password.** They were never at the password step at all.

## What is actually happening

The attack has a name: **MFA fatigue**, or push bombing. The method is patience. Someone who knows your email address — and after two decades of data breaches, everyone's email address is known — starts sign-in attempts against your account, over and over, at all hours. Each attempt can send an approval request to your phone. They are not trying to outsmart the technology. They are waiting for you to get tired, distracted, or half-asleep and tap **Approve** once.

What makes the password change useless is a convenience feature. When Authenticator sign-in notifications are enabled on a Microsoft account, a sign-in can reach the approval step **with the email address alone, before any password is typed**. My new password never entered into it. The attackers were rattling a doorbell, and the doorbell rings whether or not the lock behind it is new.

The stakes of one wrong tap are not small. Security researchers who documented this behavior on personal Microsoft accounts found that a single accidental approval can hand over a session capable of making high-risk security changes to the account — in plain terms, a full takeover, bought for the price of one tired tap. Microsoft has a security case on file for it. This is not theoretical.

## Why the usual advice fails

Everything on the standard checklist — change your password, make it longer, make it unique — defends the password step. This attack never reaches the password step. You cannot fix it by improving the thing that is not being attacked.

The thing being attacked is the **address itself**. As long as your email address works as a sign-in name, anyone on earth who knows it can make your phone buzz. So the real fix is to make the address stop working as a sign-in name, without giving up the mailbox.

## The fix — change which name opens the door

Microsoft accounts let you hold several aliases — addresses that all reach the same account and the same inbox — and, separately, let you choose which of those aliases are allowed to *sign in*. That separation is the whole trick.

1. Go to your Microsoft account's alias page (account.live.com/names/manage) and **add a new email alias**. A fresh outlook.com address works fine. It never has to be given to anyone or used for mail.
2. **Make the new alias your primary alias.**
3. Open **Change sign-in preferences** on the same page and **uncheck your old email address**. From that moment, the old address can no longer be used to sign in — by the bots, or by you.
4. **Do not delete the old address.** This is the step people get wrong. Keep it on the account as an alias. Mail sent to it still arrives in your inbox exactly as before. Deleting a Microsoft-domain address can destroy the account and everything purchased through it, and it is irreversible. You are not removing the address. You are removing its key.

The receipt that it worked: try signing in with your old address and Microsoft answers that the username does not exist. That is the same wall every bot now hits. The knocking stops because the doorbell they were ringing is disconnected — while your mail, your files, and your account sit untouched behind a sign-in name known only to you.

Microsoft's own support answers recommend this exact move for accounts under this kind of attention, which raises the obvious question of why it is buried three screens deep instead of offered the third time a foreign sign-in gets denied. But buried or not, it works.

## Supporting moves

The alias change is the cure. These are the seatbelts:

- **Deny, every time, and use number matching.** With number matching on, an approval requires typing the two-digit number shown on the *sign-in screen* into the app. A request you did not start has no screen and no number, so it cannot be "accidentally" approved in a moment of inattention — the strongest argument for leaving the feature on.
- **Check the app account settings.** In Authenticator, open your account and turn off phone sign-in if it is offered. That forces attempts back to password-first. Treat this as secondary, though: the alias fix works regardless of the app's toggles.
- **Read the Recent Activity page.** Your Microsoft account keeps a log of sign-in attempts, successful and not, with locations. It is the receipt for what has been happening — and after the alias change, the receipt that it has stopped.
- **Sign out everywhere.** In the account's advanced security options, one command terminates every active session. Worth doing once, so the account's only living sessions are the ones you started after the fix.

## The moral

I spent my first effort on the lock, because that is where a lifetime of security advice points. But the attackers were never picking the lock. They knew my address — everyone knows everyone's address — and Microsoft had helpfully wired that address to a doorbell on my phone, ringable by strangers, day and night, in the hope I would eventually answer it wrong.

The alias change does not move the house or change the locks. It just disconnects the doorbell from the address the whole world knows, and connects it to one they do not.

If your phone keeps lighting up with approvals you never requested, do not change your password a second time. Change which name opens the door.

---

*Sources: the alias remedy and sign-in preferences are Microsoft's own support guidance — see the [Microsoft Q&A thread on making a new alias to stop unwanted Authenticator attempts](https://learn.microsoft.com/en-us/answers/questions/4701066/making-a-new-alias-to-stop-unwanted-authenticator). The passwordless-trigger behavior and the takeover impact are documented in a [security research write-up on MFA fatigue risk in Microsoft personal accounts](https://github.com/paulus1337/mfa-fatigue-risk-when-authenticator-sign-in-notifications-are-enabled).*
