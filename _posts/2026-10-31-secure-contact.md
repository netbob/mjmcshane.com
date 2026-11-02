---
layout: post
title: "Keys on the Doors: Secure Contact Without a Harvestable Address"
date: 2026-10-31
categories: [tech]
tags: [pgp, security, cloudflare]
author: netbob
description: "A public key on all three of my sites, plus a contact widget that encrypts in the visitor's browser, so nobody has to send me cleartext email."
---

## The problem

Every contact page on the internet has the same flaw: if you put your
email address on it, harvesters take it. If you don't, nobody can reach
you. And even when someone does write, the message itself travels in
the clear unless both parties happen to use encryption tooling — which,
for most people, they don't.

I used to attach a PGP footer to my emails, encrypted if I so desired.
The idea was sound: my key, available to anyone who wanted it. But it
put all the work on the other person. They needed PGP, they needed my
key, and they needed to know what to do with it. Most people just
sent cleartext instead.

## Why not Keybase

Keybase had the right model: a public key tied to identity proofs —
your domains, your GitHub, your accounts — so anyone could message you
encrypted without ever seeing your address. Then Zoom bought it in
2020 and development stalled. The model was good; the landlord wasn't.

So I rebuilt the model without a landlord. I already own the proof
set: three domains and a GitHub account, all under my control. The
key lives on my sites. The proofs are my sites.

## The design

Four parts, each doing one job:

**1. The key.** An Ed25519/Curve25519 keypair, generated on my own
machine, with a UID of just my name — no email address. That last
detail matters: a no-email UID means my address never appears in the
published key at all, so there is nothing to harvest. The private key
and a revocation certificate are backed up offline.

**2. Publish identically everywhere.** The public key block plus its
fingerprint goes on mjmcshane.com, netbob.org, and techpointpro.com,
plus keys.openpgp.org as a secondary discovery point. The same
fingerprint on all three domains is the cross-proof: anyone can see
it's the same key, controlled by the same person who controls all
three sites.

**3. The contact widget.** A small static page, identical on all
three sites. The visitor types a message, OpenPGP.js encrypts it in
their browser with my public key, and only the ciphertext is POSTed
to a Cloudflare Worker. The Worker emails the ciphertext to me. My
address lives only as a secret in the Worker — never on the page,
never in the JavaScript. Plaintext exists in exactly two places: the
visitor's browser, and my machine after I decrypt it. The reply
address goes inside the encrypted message, not in a separate form
field, so even the Worker and the email service never see it.

**4. My side.** I decrypt locally with GnuPG and reply out-of-band,
however the visitor asked to be reached.

## Honest limitations

This is not magic, and the limits are worth stating plainly:

- The visitor has to trust the JavaScript my site serves. That's
  inherent to web crypto — a compromised site could serve bad JS.
- Metadata is still visible: timing, message size, and sender IP are
  seen by the Worker and the email provider. Content is sealed;
  metadata is not.
- An open form can still be spammed with ciphertext. Turnstile plus
  rate limits mitigate that; they don't eliminate it.

## Step 1: Generate the key

The first step is the only one that must happen on my own machine.
The passphrase prompt is mine alone — it goes nowhere else.

On Windows, GnuPG isn't installed by default — my Dell answered
`gpg` with "not recognized." Install Gpg4win first:

```
winget install GnuPG.Gpg4win
```

Then close and reopen PowerShell so the new PATH takes effect, and
check with `gpg --version`. Then generate:

```
gpg --quick-generate-key "Michael McShane" default default 2y
```

That gives a primary Ed25519 key (sign and certify) plus a Curve25519
encryption subkey, expiring in two years. My first attempt used
`eddsa cv25519` — wrong on both counts: GnuPG's signing algorithm is
named `ed25519`, not `eddsa`, and quick-generate takes one algorithm
plus a usage, not two algorithms. Verify the result shows both lines:

```
gpg --list-keys "Michael McShane"
```

Expect `pub ed25519` and a `sub cv25519` line. If the subkey line is
missing, add it with the fingerprint from that listing:

```
gpg --quick-add-key <fingerprint> cv25519 encr 2y
```

Then export, revoke, and fingerprint:

```
gpg --armor --export <keyid> > michael-mcshane-public.asc
gpg --output revoke.asc --gen-revoke <keyid>
gpg --fingerprint <keyid>
```

Angle brackets mean "substitute your value" — they are not literal.
PowerShell rejects a literal `<` (it's a reserved redirection
operator), so `gpg --armor --export <keyid>` fails before doing
anything. Use your actual key ID or fingerprint from the listing,
or simply `"Michael McShane"` as the identifier for the export and
fingerprint commands.

The revocation certificate is the part people forget. Generate it
now, store it offline with the private-key backup, and the key can be
killed if it's ever compromised.

Note: GnuPG also auto-generates a revocation certificate at key
creation, stored in `%APPDATA%\gnupg\openpgp-revocs.d\<fingerprint>.rev`.
The `--gen-revoke` command above produces a standalone copy of the
same thing, in whatever directory you run it from — it does not land
inside the gnupg folder itself.

Done Oct 31, 2026: key generated — Ed25519 primary (sign and certify)
plus Curve25519 encryption subkey, created 2026-10-31, expiring
2028-10-31. The default keygen created the subkey, so no
`--quick-add-key` step was needed. Fingerprint:

```
F195 0F9F A38A 28DA 2303 431C 1A57 9411 7A22 8B99
```

## What actually shipped

Step 2 and 3 landed on Oct 31, 2026: the widget (`contact.html`) and
the Worker (`worker.js`) went up on all three sites at `/contact.html`,
with the Turnstile widget and the Worker's secrets in place. The one
surprise was the send path. The Worker's first version used
MailChannels' old keyless Workers integration — and every test came
back HTTP 401, despite a correct Domain Lockdown record. That
integration ended June 30, 2024; keyless sends simply don't work
anymore. The fix was the MailChannels Email API with an API key:
the Worker sends with an `X-Api-Key` header, the key lives only as a
Worker secret, and the Domain Lockdown record uses the `auth` form
(the MailChannels account ID) instead of the keyless `cfid` form.
SPF on the sending domain picked up `include:relay.mailchannels.net`.
A credit card went on the account to lift the verified-recipient
restriction — the no-card rule binds only on the recipient side, and
this form has exactly one recipient, so the card was a convenience,
not a structural need. The plan stays Free.

End-to-end test, Nov 1, 2026: the form reported success, the
ciphertext email arrived (from `contact@mjmcshane.com`, subject
"Encrypted contact message", PGP block for a body), and Kleopatra
decrypted it to exactly what the widget composes — a `Reply to:`
line, a blank line, then the message. The audit log confirmed the
message was encrypted to my Curve25519 subkey. Kleopatra's "not
signed" note is expected: the widget encrypts without signing, so a
message is private but not sender-authenticated. That is the design,
not a defect.

Live as of Nov 1, 2026: the encrypted contact form on mjmcshane.com,
netbob.org, and techpointpro.com, linked from each site's navigation.
The fingerprint is on the contact pages; the full public key block as
visible text, and a keys.openpgp.org upload, are still to come as
secondary discovery. The revocation certificate sits in a Bitwarden
secure note, with an encrypted-USB second copy still to make.

*Live Nov 1, 2026. The method works end to end — tested, decrypted,
and confirmed.*
