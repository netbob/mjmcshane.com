---
title: MarkPad — A Markdown Editor That Gets Out of the Way
description: A fast, minimal markdown editor for Windows with a GitHub-friendly git workflow, dark mode, preview toggle, and change markers. Free, MIT, no accounts, no telemetry.
author: netbob
categories: [Tech]
tags: [MarkPad, markdown, Windows]
image:
  path: /assets/img/markpad-card.png
  width: 1200
  height: 628
  alt: MarkPad — a minimal markdown editor
toc: true
pin: false
---

Markdown Monster is full of features, but mostly it's clunky to use. I wanted
a markdown editor that is quick and snappy and stays out of the way, so I
built one: MarkPad, for Windows, free and open source under MIT.

MarkPad does three things:

1. **A GitHub-friendly git workflow.** Open a file inside a repo and the
   status bar shows the branch and how many files changed. Commit (with a
   file checklist), push, and pull from the Git menu. It shells out to the
   `git` you already have installed, so it reuses your existing GitHub auth
   — GitHub Desktop or Git Credential Manager. No new login, no token.
2. **One view, like Notepad++.** The markdown source, with syntax
   highlighting coloring headers, bold, italic, code, links, lists, quotes,
   and rules in place. Tabs for multiple files, line numbers, Ctrl+F find.
   Change markers in the line-number margin: orange for edits since the
   last save, green once saved. View → Preview swaps the whole tab to a
   rendered read-only view — never a split pane.
3. **A dark mode switch.** View menu, Light/Dark, remembered between runs.

And the one hard rule: the editor never reformats a file. What you type is
what gets saved, with the file's original line endings and encoding
(including BOM) preserved. That matters for Jekyll front matter, where a
rewritten file can change meaning — a bare numeric tag parses as a YAML
integer, and a colon-space in a description can break a build. MarkPad is a
text editor; it has nothing to "fix."

Installation is the Setup installer from the
[releases page](https://github.com/netbob/MarkPad/releases). It installs
per-user with no admin rights, and it checks GitHub Releases on every
launch: a new version downloads in the background and installs itself when
you quit normally. It never interrupts an editing session.

Questions are welcome in the comments below, and bug reports go to GitHub Issues on the repo.

MarkPad is free forever, no accounts, no telemetry. The source is on
GitHub at [netbob/MarkPad](https://github.com/netbob/MarkPad), and if it
earns a coffee, the tip jar is at
[buymeacoffee.com/Netbob](https://buymeacoffee.com/Netbob) — the only money
door.

Spellcheck is next, queued for v1.1. A settings page and a few more ideas
are on the list after that. But v1 is the point: quick, snappy, and out of
the way.
