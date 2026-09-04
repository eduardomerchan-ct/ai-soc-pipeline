# AI-Powered Cybersecurity Incident Response Pipeline

**Status:** In progress (2026)
**Author:** Eduardo Merchan — CSE @ UConn, AI concentration

## What this is

So this is a multi-agent AI pipeline I've been building on Azure AI Foundry. Basically I wanted to see if I could get a chain of AI agents to do what a SOC (Security Operations Center) analyst does — take a pile of raw security logs, figure out what actually happened, and spit out something a real team could use, instead of just a cool-looking demo that doesn't really go anywhere.

Instead of one giant agent trying to do it all, I split it into three agents that hand off to each other, with each one picking up where the last one left off.

## How it works

**Agent 1: Log Analysis**
Reads through the raw logs and figures out what kind of attack this is, what systems got hit, and what's actually worth flagging.

**Agent 2 : Threat Scoring**
Takes what Agent 1 found and scores it with CVSS — the real scoring system security teams actually use — so every threat gets a severity rating (Low to Critical) plus a CVE reference when there is one.

**Agent 3 : Report Writing**
Takes everything from the first two agents and writes it up into a full incident report: timeline, threat breakdown, remediation steps, all formatted the way a real SOC team would want to see it.

## Tech Stack

- Azure AI Foundry (running the multi-agent chain)
- CVSS / CVE for threat scoring
- Python

## Still on my to-do list

Not done yet, still chipping away at this:

- [ ] Plug in real logs from simulated traffic instead of sample data
- [ ] Add KQL (Kusto Query Language) so logs get filtered more precisely before they hit the pipeline

## Why I'm building this

I wanted something that felt close to real SOC work,Chaining the agents together made me actually think about how info should flow between the different steps of incident response, and it's shown me where AI genuinely pulls its weight in security and where you still need a human double-checking things.

## Notes

Everything here runs on data I own or have permission to use.
