---
layout: post
title: "Sign Your Mail with GPG in Thunderbird"
date: 2026-11-17 23:00:00 -0800
categories: [Guide]
tags: [GPG, Email, Thunderbird, Privacy, Security]
author: netbob
---

Anyone can put your name in the From line of an email. A GPG signature is how the person on the other end knows it was actually you. This is signing, not encrypting: the message stays readable to everyone, but anyone with your public key can verify you sent it and nobody altered it in transit. It is the anti-spoofing piece.

This guide sets up signed sending in Thunderbird with a key you already have (or one you create). It was written on Windows with Gpg4win and Thunderbird; the steps are the same on other platforms, only the key manager changes.

## What you need

- A GPG key pair. If you already have one, you need its key ID. If you don't, create one first in Kleopatra (File > New Key Pair) or with `gpg --full-generate-key` — a 255-bit EdDSA key is a good default.
- Gpg4win (which includes Kleopatra and the `gpg` command) on Windows, or GnuPG on your platform.
- Thunderbird, with your mail account already added.

## Step 1: Export your secret key

Thunderbird needs your secret key to sign. Export it to a file:

```powershell
gpg --export-secret-keys --armor --output secret.asc 1A5794117A228B99
```

Replace `1A5794117A228B99` with your own key ID. Run it in the folder where you want the file (here, `C:\src`). The `--armor` flag makes the output text instead of binary, so you can inspect it.

One gotcha: in Kleopatra, the plain Export command and the right-click menu only export the *public* key. To export the secret key in the GUI, use **File > Backup Secret Keys...**. The command above is the reliable route.

**Keep `secret.asc` safe.** It is your private key in a file. You will delete it at the end of this guide, once Thunderbird has the key.

## Step 2: Import the key into Thunderbird

In Thunderbird:

1. Open **Account Settings**.
2. Expand your mail account (click the **>** next to it) and choose **End-To-End Encryption**.
3. Click **Add Key**, then **Import an existing OpenPGP key**.
4. Pick the `secret.asc` file you just exported.
5. Check **Treat this key as a Personal Key** and finish the import.

You should see a green confirmation and the key's fingerprint. Confirm the fingerprint matches the one Kleopatra shows for your key.

You may see a warning that the key "advertises an unsupported feature" and that correspondents might send you mail in an incompatible format. Click OK. That warning is about *receiving* encrypted mail with a newer OpenPGP feature Thunderbird's crypto library does not fully support. It does not affect *sending signed* mail, which is what this guide sets up.

Do not import the key from Settings > Privacy & Security. That is the global encryption page, and it tells you to use Account Settings instead.

## Step 3: Turn on signing

On the same End-To-End Encryption page for the account, set:

- **Encryption:** "Do not encrypt new messages by default" (signing is not encrypting; leave encryption off unless you specifically want it).
- Check **Digitally sign unencrypted messages**.
- Check **Attach the public key for this identity when digitally signing messages**. This attaches your public key as a small `.asc` file, so recipients can verify you without hunting for your key.
- Check **Include this account's public key in message headers (for Autocrypt compatibility)**.

Do this for each account you send signed mail from. The key is the same; the setting is per account.

## Step 4: The signature line

Your email signature should carry your fingerprint — the short, human-checkable form of your key — and nothing else. The full public key block does not belong in the body: it is long, it looks like encoded spam to filters, and the `.asc` attachment already carries the key in machine-readable form.

A good signature:

```
--
Michael McShane
PGP: F195 0F9F A38A 28DA 2303 431C 1A57 9411 7A22 8B99
```

Replace the name and fingerprint with your own. Note the `--` at the top: Thunderbird adds its own separator automatically, so do **not** put a `--` line in your signature text or you will get two of them. Put only your name and the fingerprint line.

## Step 5: Clean up

Once Thunderbird has the key and you have sent a signed test, **delete `secret.asc`**. Your private key now lives in Thunderbird (and in Kleopatra, where it belongs). A stray copy of your secret key sitting in a folder is a liability, not a backup. Your real backup is the key in your password manager or an encrypted export stored deliberately — not a file left in `C:\src`.

## If you add an address to your key later

A GPG key can carry several email addresses as user IDs. If you add one *after* you exported `secret.asc`, the copy Thunderbird imported does not have it yet. Re-export with the same command (it overwrites the file) and import it again in Thunderbird — Thunderbird updates the key it already has. Then delete `secret.asc` again.

## Verify it works

Send a test message to an address you can read on another device. A signed message shows a **Signed** badge in the recipient's mail client (Apple Mail on iPad shows it clearly) and carries the `.asc` public-key attachment. If the badge is there, signing works. If it is not, re-check Step 3: the "Digitally sign unencrypted messages" box is the one people miss.

## Do not use Outlook for this

This is the part that matters as much as the setup. **Do not use the newer versions of Microsoft Outlook with a third-party mail account for signed mail.**

Microsoft Outlook: Runbox explicitly does not recommend using the newer versions of Microsoft Outlook with IMAP/SMTP accounts. Recent iterations route mail traffic through Microsoft's cloud infrastructure rather than logging into your mail server directly, raising privacy and authentication concerns. (If you choose to use it anyway, you must manually configure the server settings).

That routing is the problem. When your mail passes through Microsoft's cloud on its way to your provider, you are no longer connecting directly to your mail server, and you are handing Microsoft a copy of mail that was supposed to go straight from you to your provider. A signature proves the message came from you; it does not help if the client itself sends your mail through a third party's servers first.

Use a mail client that connects directly to your provider over IMAP and SMTP. Thunderbird does, and it has OpenPGP signing built in. That combination — direct connection plus a signature — is the point: your mail goes from you to your provider to the recipient, and the recipient can verify it was you.

## The short version

Create or find your key. Export the secret key, import it into Thunderbird as a personal key, turn on "Digitally sign unencrypted messages" and "Attach the public key," put only your fingerprint in the signature, delete `secret.asc`, and send a test to confirm the Signed badge. And send it from a client that talks to your mail server directly — not one that routes your mail through someone else's cloud.
