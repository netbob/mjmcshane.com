---
title: "PHP Advisory 0011 — PHP2Shell"
description: "Two critical remote-code-execution flaws in PHP itself landed today. This house runs three public websites and exactly zero PHP. The morning audit, the receipts, and what to do if your stack is different."
author: Michael McShane
date: 2026-10-21
categories: [Tech]
tags: [security, php, advisory, static-sites]
pin: false
toc: true
---

Advisories on this site get numbers. This is 0011 — binary, which suits the subject, because the verdict for any given website this morning is also binary: your server runs PHP, or it doesn't.

Mine don't. But I checked, because checking is the job.

## What dropped

Two vulnerabilities in the PHP interpreter itself, disclosed today, October 21, 2026, after the details leaked a day early:

- **CVE-2026-109618** — an out-of-memory error during request startup can interrupt PHP before the request's internal data is fully initialized. The cleanup that follows treats that half-built data as valid. Rated **CVSS 9.2**.
- **CVE-2026-109619** — internal state owned by one request can survive after its memory has been freed, and a later request handled by the same worker can use the stale state before it is reset. Also **9.2**.

Researchers are calling the pair **PHP2Shell**. The confirmed attack paths live in how PHP parses `multipart/form-data` requests — the format a browser uses to upload files — and in the session upload-progress machinery that tracks those uploads. The important part is *when* the vulnerable code runs: **before your application code starts**. Your login page, your plugins, your application firewall never get a vote. A site can be written perfectly and still be exposed, because the flaw is in the floor, not the furniture.

The scope, per PHP's own advisory:

- Every way of serving PHP is in scope — PHP-FPM, Apache with `mod_php` (which PHP rates the **highest risk**, with a demonstrated exploit), `php-cgi`, FrankenPHP, LiteSpeed.
- Every supported branch was vulnerable, and so was everything older: PHP 5 through 8.1 are affected but end-of-life.
- Wiz, one of the reporting research teams, also demonstrated reading live PHP worker memory without code execution. Worker memory holds passwords, tokens, and API keys.
- Cloudflare put WAF rules in front of its customers early this morning and reports it has already seen attack traffic, with payloads mutating to get around the rules.

The fixes shipped today, October 21, at 14:00 UTC. These are the only complete remedy:

```text
PHP 8.2.35
PHP 8.3.36
PHP 8.4.27
PHP 8.5.12
```

## The receipts: this house

When a flaw lands in a language runtime, the audit is an inventory, not an investigation. Three public sites live here:

- **mjmcshane.com** — Jekyll (Ruby) builds it into static HTML, CSS, and JavaScript. Cloudflare Pages serves the files.
- **netbob.org** — same stack, same hosting.
- **techpointpro.com** — one static HTML page, same hosting.

PHP interpreters anywhere in those chains: **zero**. There is no server-side code on any of them to execute, malicious or otherwise. Comments run on GitHub's infrastructure (Giscus), not mine. The only WordPress on the property is a WXR export file sitting in storage, and an export file cannot be exploited — it can only be read, slowly, with regret.

Verdict: no patch to apply, no service to restart, no emergency session. The scanners that are certainly sweeping the internet for this flaw tonight will reach these domains, ask Cloudflare for files, receive files, and move on.

## The lesson

Nobody at this house chose a static stack *because* of PHP2Shell. The choice was made years before these CVEs had numbers, for duller reasons: a personal site does not need a database, a login system, or a runtime to babysit.

But exposure is decided exactly there — at architecture time, long before the advisory exists. A dynamic stack is a standing patch obligation. Most days the obligation is theoretical. Some days, like today, it is the whole day: an emergency release, a leaked exploit, government sites in Europe taking themselves offline rather than wait, and a patch window measured in hours because attackers diff the fix and work backwards from it.

A static stack doesn't make its owner smarter or more virtuous. It makes entire vulnerability classes structurally irrelevant. You give up server-side anything to get that. Around here, that trade was made knowingly, and mornings like this one are the dividend.

## If your house is different

If you run WordPress, Drupal, Joomla, or anything else on PHP, here is the whole job, in order:

1. **Patch.** Move to 8.2.35, 8.3.36, 8.4.27, or 8.5.12 — then **restart PHP**: the FPM service and every long-running worker. Reloading the web server alone can leave old, vulnerable workers alive and serving.
2. **If you're on PHP 8.1 or older, you are the priority case.** Those branches get no official fix. A distribution or LTS vendor backport, verified, or a migration to a supported branch — one of those, today, not this quarter.
3. **Do not let a mitigation read like a remedy.** Configuration tweaks circulating this morning — turning off `session.upload_progress`, adjusting memory limits — close some confirmed paths and leave others open. Datadog's labs and a PHP core developer are saying the same sentence: the only complete mitigation is patching.
4. **If your host says they handled it, get the version number.** "We've taken care of it" is a claim; `8.4.27` is evidence. Hosts that patched at the server level, like SiteGround and Cloudflare's WAF layer, are buying you time, not closing the ticket.
5. **Assume the pre-patch window mattered.** If your PHP was internet-facing before the fix, worker memory may have been readable. Rotate the secrets that matter — database passwords, API keys — after you patch, not before.

Around here the fire is real; it's just not at this address. If it's at yours, the patch is the day. Everything else is commentary — including, I'll grant you, this post.

## Postscript

The irony, since it's the first thing I'd point out in someone else's post: this advisory — about an infrastructure failure — was itself delayed by an infrastructure failure. I pushed it at 8:52 this morning. GitHub was mid-incident, its push events to Cloudflare were degraded, and the build that publishes this site never started. The file sat complete and correct on GitHub for about 35 minutes while the site went on serving yesterday's version, until the missed event replayed, the build caught up, and the post went live.

And for the record, because it was the first question I asked myself: no, it was not a PHP issue on the back end. There is no PHP on the back end. That is, rather, the point of everything above.