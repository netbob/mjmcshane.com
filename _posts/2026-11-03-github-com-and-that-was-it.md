---
layout: post
title: "github.com, and That Was It"
date: 2026-11-03 00:20:00 -0800
categories: [Tech]
tags: [AI, Gemini, GitHub, Markdown]
author: netbob
description: "Early Gemini sessions taught me that what a chat UI shows isn't always what your clipboard holds."
---

Early on, when I was using Gemini for system-install tasks — the Make.com era, that kind of work — I kept running into a wall with GitHub. I would ask for a link to something, a long file path three folders deep, and what came back was:

```
github.com
```

And that would be it. No path, no file, nothing to copy. You cannot install software from a domain name. The sessions went around in circles: ask again, get the same clipped answer, wonder whether the model didn't know the URL or whether something between the model and my screen had eaten it.

It was the second one. Probably. That distinction matters, and it took me a while to see it clearly, because three different failure points all produce the same symptom: the URL you paste isn't the URL you needed.

## Three ways a URL gets shorter between the model and your editor

**1. Display elision.** A chat UI shortens a long URL for display — an ellipsis in the middle, or in the worst case just the domain. The underlying link may be intact. What you *see* is not necessarily what you *get*, and the trouble starts when you treat the rendered text as the source.

**2. The copy path.** If you copy from the rendered view instead of from a code block, your clipboard can hold the shortened text. A paste into an editor can also wrap a long line and break it. Either way, the code now contains a URL that looks plausible and points nowhere useful.

**3. The model itself.** Separate from any rendering, a language model can garble a long URL in generation — a dropped path segment, a transposed character in an ID. This one is still very much alive, and no UI fix addresses it, because the corruption happens before rendering.

The classic symptom, when the corrupted URL reaches a script, looks like this:

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

That error means the script asked for JSON and got an HTML page instead — usually a login redirect or a landing page. It is worth knowing, and worth not over-reading: a wrong endpoint or a failed login produces exactly the same error. A clipped paste is one possible cause, not the only one, and diagnosing every `<!DOCTYPE` error as truncation will send you hunting in the wrong place.

## The test you can run yourself

This is the part that makes it a field report instead of a complaint: the mechanism is reproducible on a public URL, no private data involved. Take a long one, for example:

```
https://github.com/netbob/powerwall-dispatch/blob/main/logger/LOGGER_SPEC.md
```

Paste it into a chat UI. Look at what renders. Then paste *from the rendered view* into a plain-text editor and compare character for character with what you started with. If what lands isn't what you started with, you have found the hazard on that surface — and you have found it with a URL anyone can check, which is the whole point of doing it this way.

## The fix, in order

**First: never copy a URL out of rendered prose.** Copy from a fenced code block or from a raw file. Code blocks are the copy source; rendered text is not. This one rule kills the first two failure points outright, and it is the rule I now treat as non-negotiable for anything that will end up in code.

**Second: verify the paste.** After pasting into code, glance at the pasted text before running anything. Pasting into a plain-text view first and comparing costs five seconds and catches all three failure points, including the model's own garbling.

**Third, only when you cannot control the surface:** build the URL from parts in code, so no single long literal ever passes through a renderer. In a Google Apps Script context that looks like this:

```javascript
// Build the endpoint from parts so no long literal crosses a chat renderer.
var transportProtocol = "https://";
var coreDomain        = "api.netzero.energy";
var apiVersion        = "/api/v1/";
var accountIdentifier = "YOUR_SITE_ID";
var terminalEndpoint  = "/config";

var targetUrl = transportProtocol + coreDomain + apiVersion + accountIdentifier + terminalEndpoint;
```

This works. It is also the second layer, not the first, and it should be labeled as such: it makes code harder to read and harder to grep, and it protects nothing against the model garbling a component. Use it where the rendering surface is genuinely out of your control, not as a substitute for copying from a code block.

## A note on timing

This was an early-era problem. Modern chat UIs copy fenced code blocks byte-exact, and the classic form of the bug — the renderer itself destroying a URL — is mostly dead. What survives is the copy path: rendered prose, mobile line-wrap, and the model's own transcription. The lesson generalizes past any one UI, and it is short enough to keep:

What you see is not always what you paste. Trust the clipboard's contents, not the screen's rendering — and check before you run.
