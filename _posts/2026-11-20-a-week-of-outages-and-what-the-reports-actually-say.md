---
layout: post
title: "A Week of Outages, and What the Reports Actually Say"
date: 2026-11-20 05:25:00 -0800
categories: [Tech]
tags: [Outages, Microsoft, FAA, Security]
author: netbob
---

In less than a week, Microsoft 365 went down, the FAA grounded every flight in the country, the National Weather Service was reported down, and then several major banks had trouble on a Monday. It felt like a pattern. It looked like a pattern. The question is whether it was one.

Here is the ledger, as of this morning. What each incident's own reports actually say, what is still unknown, and what nobody has said.

## Microsoft 365, November 12-13

Exchange Online went down on Thursday, November 12, and stayed down into Friday. Microsoft's incident number is EX1550543. The preliminary post-incident report, dated November 15, names three causes that lined up together:

1. A latent Windows defect, shipped to the Microsoft 365 gateway servers in July, that made them become unresponsive under certain load conditions.
2. A Teams failover at 01:07 UTC on November 12 that moved Teams onto the same gateway that serves Exchange Online.
3. Nearly 14 percent of gateway capacity already out of service from an unrelated issue the day before.

Automatic traffic redirection then spread the failure to more than 80 percent of the gateway servers. Microsoft says it was not a cyberattack and not caused by AI. The final post-incident report is due today, November 20.

One thing worth noting, because it is a reason to read these reports critically rather than take them on faith: Microsoft revised the outage duration in the interim report, from 30 hours down to just under 24 hours, by moving the start time six hours later. That changes what businesses can claim under their service-level agreements. It does not change the cause, but it is a reminder that the company writing the report has an interest in how the report reads.

## The FAA ground stop, November 13

On Friday afternoon the FAA ordered a nationwide ground stop. It lasted about four and a half hours, from 3:45 to 8:15 p.m. Eastern, and disrupted more than 10,000 flights. Seventeen of the twenty-two air route traffic control centers were affected.

The FAA posted its initial findings on November 15. New routers at two sites — a radar site in Amarillo, Texas, and a radio communications site in El Dorado, Arkansas — flooded the FAA's telecommunications network with 1,000 connection attempts every four to five seconds, destabilizing communications and radar feeds. The contractor L3Harris had just installed a new Juniper router at El Dorado during a copper-to-fiber cutover. When L3Harris blocked the two sites, the network stabilized, and the same function was disabled on about sixty similar routers as a precaution.

Transportation Secretary Sean Duffy said it was either an installation error or faulty equipment. The suspect routers are being analyzed at an L3Harris lab, with the FBI on site. The Department of Homeland Security said there was no evidence of a cyber or artificial intelligence attack. The FAA calls this an initial investigation and says the root cause is still being looked into.

## The National Weather Service: not an outage

This is the one that was not what it looked like. On Friday, reports spread that the National Weather Service was experiencing a nationwide outage, based on notices appearing on NWS webpages. The NWS said the same day that there is no radar outage and that radar.weather.gov is fully operational. The notices were outdated content from isolated webpages that started circulating. There was a regional issue with NOAA weather radios, but no nationwide outage, and no link to the FAA problem has been established.

## The banks, November 16

On Monday, customers at several major banks reported trouble logging in, moving money, and using ATMs. Downdetector logged more than 4,600 problem reports for Chase, about 1,900 for Bank of America, more than 900 for U.S. Bank, and about 800 for Wells Fargo.

Chase identified the cause as a software bug in its on-premise hardware systems, and said explicitly that it was not cyber related. The other banks were affected only to the extent they were a party to a transaction with Chase — Chase is a party to so many transactions that its slowdown rippled outward, including into Zelle transfers, even though Zelle's own network was operating normally. Chase said transactions were back to normal Monday evening. There is no evidence connecting the bank problems to the Microsoft outage or the flight disruptions, and no verified evidence of a coordinated cyberattack on the banks.

## A separate disclosure, November 19

On November 19, Chase, Visa, and Mastercard each disclosed security incidents involving third-party vendors. Chase said a cyberattack on its vendors may have exposed some customer marketing data, but that it caused no service disruption and is unrelated to the November 16 outage. An extortion group's claim involving Chase remains unverified.

This is a different matter from the outage. It is worth naming separately precisely so it does not get folded into the outage story without evidence.

## What the ledger says

Four real incidents, one false alarm, and one separate disclosure. The documented causes are a software defect, a router flooding a network, and another software bug — all technical, all separate, none attributed to an actor. No state or non-state actor has been named as a suspect in any of them. The Department of Homeland Security has said there is no indication of a cyberattack in the FAA case, and Chase has said the same about the bank case.

What is still unknown: Microsoft's final report, due today, and the FAA's root-cause investigation, which is ongoing. Those reports are the authority, and they are still coming in.

The clustering is real, and it is worth noticing. Three major systems failing in four days is unusual, and it is reasonable to ask whether they are connected. But the reports we have so far say they are not, and they say so with specifics — a defect, a failover, a capacity shortfall, a router, a bug — not with a shrug. The honest position is to read the reports as they land, note what is still open, and not fill the gaps with a pattern before the evidence does.
