---
title: "CCA-F Domain 5: Context Management and Reliability"
date: 2026-10-27T08:14:27+05:30
draft: false
featureImage: "images/df024c_fb94b84e2f79490ca16c4a56a758b6bd.jpg"
tags: ['[]']
categories: ['["6a89342d6797a1f792f34566"]']
showReadingTime: true
---

### As we discussed in the previous post on [Domain 4: Claude Code Configuration and Workflow](/post/cca-f-domain-4-prompt-engineering-and-structured-output), this part of the post will cover the Domain 5 which holds 15% weightage in the exam. This is also the ***last domain*** in this CCFA series.

### If you have directly stumbled upon this page, I am preparing for the Claude Certified Architect — Foundations (CCA-F), and placing all types of practice questions that I encounter. This may help others, but objective is to keep track of key concept and some practice question that define the topics as well.

Where to Register: [https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)

> Unofficial practice set, written to match publicly reported blueprint topics — not sourced from the real exam bank. Use for concept drilling, not as a guarantee of exam content.

#### ***Topics Covered***

Prompt Caching & *cache_control* Breakpoints

Lost-in-the-Middle Effects

Progressive Summarization Risks

Conversation Compaction

Verbose Tool Output Trimming

Token Estimation & Budget Management

Multi-Turn Conversation Design

Escalation Decision-Making (explicit criteria + few-shot)

Structured Error Propagation Across Multi-Agent Systems

Context Management in Large Codebase Exploration (scratchpad files, subagent delegation)

## 1. Prompt Caching & *cache_control* Breakpoints

Anthropic's API can **reuse the already-computed representation (KV cache)** of a prompt prefix instead of reprocessing it from scratch on every call — cutting cost and latency. You mark cache breakpoints using cache_control. **Critical rule: caching works on prefixes** — the cached portion must be identical and must come *before* the dynamic parts. **Stable content goes first (system prompt, project context), volatile content goes last (current message).** Any change to the stable prefix (e.g., injecting today's date at the top) invalidates the cache for everything after it.

**Q1.** A system prompt starts every request with "Today is {current_date}..." before the rest of the fixed instructions. Cache hit rates are near zero. Why? 

A) cache_control isn't supported for system prompts 

B) The changing date sits at the very start of the prefix, so it invalidates the cache for every token that follows it on every single call 

C) The prompt is too short to cache 

D) Dates cannot be included in prompts

Answer: B — the "don't put volatile content at the top" rule, tested directly.

**Q2.** Where should a per-user, per-session variable (like a username injected into context) be placed to preserve cache efficiency? 

A) As late as possible — near the dynamic/current-turn content, not mixed into the stable, cached prefix

B) At the very beginning of the system prompt 

C) It doesn't matter where it goes 

D) It should never be included at all

Answer: A.

**Q3.** What does a *cache_control* breakpoint mark in a request? 

A) A point where the conversation ends 

B) A rate-limit threshold 

C) A point in the prompt up to which content should be cached for reuse in future requests with the same prefix 

D) A required field in every JSON schema

Answer: C.

**Q4.** A team structures their prompt as: 

[current message] → [session history] → [CLAUDE.md project context] → [core system instructions]. 

Cache hits are poor. What's wrong with this ordering? 

A) Nothing, order doesn't matter 

B) It's backwards — stable content (core instructions, project context) should come first, with the most volatile content (current message) last, so the maximum stable prefix can be cached 

C) CLAUDE.md cannot be cached 

D) Session history should never be included

Answer: B.

## 2. Lost-in-the-Middle Effects

LLMs tend to **pay less attention to information placed in the middle of a long context**, compared to information near the beginning or end. 

*Practical implication:* critical facts buried in the middle of a huge context (long documents, long conversation histories) are more likely to be missed or under-weighted than facts placed at the start or end.

**Q5.** A 50-page contract is passed to Claude with the single most important clause sitting on page 25 (dead center). Extraction quality for that clause is worse than for clauses on page 1 or page 50. What effect explains this? 

A) Token limit exceeded 

B) Lost-in-the-middle — information in the middle of long context tends to be attended to less reliably than content at the start or end 

C) The model wasn't given the whole document 

D) This is a JSON Schema issue

Answer: B.

**Q6.** What's a practical mitigation for lost-in-the-middle effects when a specific fact absolutely must be captured accurately from a long document? 

A) Nothing can be done, it's an inherent limitation 

B) Always increase temperature 

C) Reposition or explicitly re-surface the critical information near the start or end of the context, or break the document into smaller chunks processed separately 

D) Use the Batch API

Answer: C.

## 3. Progressive Summarization Risks

As a long conversation grows, older parts are often **summarized to save space**. Repeating this (summarizing an already-summarized summary) compounds **information loss** — details get progressively vaguer or dropped entirely across each round, and by several rounds in, specific facts from early in the conversation may be irrecoverably gone.

**Q7.** A long-running agent session repeatedly summarizes its own summaries every time context fills up. After many rounds, the agent has lost track of a specific requirement stated at the very beginning. What's the cause? 

A) The model has a bug 

B) This is a lost-in-the-middle effect, unrelated to summarization 

C) The requirement was never actually processed

D) Progressive summarization compounds information loss each time a summary is re-summarized; specific early details erode over repeated rounds  <details>

Answer: D.

**Q8.** What's a safer alternative to repeatedly re-summarizing an already-summarized history? 

A) Summarize even more aggressively each round 

B) Preserve critical facts/decisions verbatim in a durable store (e.g., a scratchpad file or structured state) instead of relying purely on compounding text summaries 

C) Never summarize under any circumstances 

D) Increase the model's context window instead

Answer: B.

## 4. Conversation Compaction

A **built-in mechanism** (e.g., in Claude Code) that condenses accumulated session state into a brief summary once context usage gets too high, reclaiming window space so the session can continue — trading some historical detail for continued operability. Distinct from progressive summarization risk in that it's usually a single compaction pass reacting to actual pressure, not a repeated/compounding pattern — but it still loses detail and can strip specifics if triggered carelessly or repeatedly.

**Q9.** A Claude Code session hits high context usage on a long feature-build task. What happens under conversation compaction, and what's the trade-off? 

A) The session simply stops working 

B) Accumulated session state gets summarized down to reclaim space so work can continue, at the cost of losing some fine-grained historical detail 

C) Compaction deletes the current task entirely 

D) Compaction only affects tool outputs, never conversation text

Answer: B.

**Q10.** Why might an architect want to proactively manage context (e.g., via scratchpad files) rather than relying purely on automatic compaction? 

A) Proactive management preserves specific critical facts intact instead of leaving all information subject to lossy automatic summarization when the window fills up 

B) Automatic compaction is always sufficient and needs no supplementing 

C) Compaction is a manual-only feature 

D) There's no reason to; automatic compaction is strictly better

Answer: A.

## 5. Verbose Tool Output Trimming

Raw tool outputs (large API responses, full file contents, long logs) can consume large amounts of context for little benefit if returned in full every time. **Trimming** means stripping unnecessary bulk (mechanical bloat like raw dumps, base64 data, redundant metadata) while preserving the actually useful signal — keeping context lean without losing substance.

**Q11.** A tool call returns a 50KB raw API response, but the agent only ever needs 3 specific fields from it. What's the architectural fix? 

A) Pass the full 50KB into context every time, "just in case" 

B) Trim the tool output to the relevant fields before it enters context, discarding the unnecessary bulk 

C) Switch to the Batch API 

D) Increase the context window instead of trimming

Answer: B.

**Q12.** Why is verbose tool output trimming particularly important in long agentic sessions with many tool calls? 

A) Untrimmed verbose outputs accumulate turn after turn, consuming context budget fast and increasing the risk of hitting limits or triggering lossy compaction sooner 

B) It has no cumulative effect 

C) It only matters for the first tool call 

D) Trimming reduces the model's accuracy

Answer: A.

## 6. Token Estimation & Budget Management

Proactively **estimating how many tokens a task will consume** (system prompt + context + expected output) and **planning within a budget**, rather than discovering you've hit limits mid-task. Includes accounting for tool schemas (which consume tokens just by being defined, whether called or not) and reserving headroom for output.

**Q13.** A system has 15 tools defined, each with a lengthy schema, but a typical task only ever uses 2 of them. What's a token-budget consideration here? 

A) Tool schemas cost nothing unless called 

B) Only called tools count against budget 

C) All defined tool schemas consume context tokens on every request regardless of whether they're actually called, so unused tools still count against the budget 

D) This has no effect on token usage

Answer: C — ties back to Domain 2's "tool sprawl" from a token-budget angle.

**Q14.** Why should token budgeting reserve explicit headroom for the model's output, not just the input context? 

A) Output tokens are free 

B) If input consumes nearly the entire context window, there may be insufficient room left for the response the task actually requires, causing truncation 

C) Output never counts against context limits 

D) This only matters for structured output tasks

Answer: B.

## 7. Multi-Turn Conversation Design

Designing how a **conversation accumulates and is structured over many turns** — deciding what persists, what gets pruned, when to summarize vs. preserve verbatim, and how earlier decisions/context stay accessible without bloating every subsequent call.

**Q15.** A multi-turn support conversation needs the customer's original complaint (turn 1) to remain accurately known even by turn 40. What design choice best preserves this reliably? 

A) Trust that lost-in-the-middle and summarization won't affect it 

B) Ignore the risk since 40 turns isn't very long 

C) Re-ask the customer to repeat it every 10 turns

D) Explicitly preserve the original complaint as a persistent, structured fact (e.g., in a fixed context slot or state object) rather than letting it become buried and possibly summarized away deep in conversation history 

Answer: D.

**Q16.** What's a key multi-turn design trade-off between keeping full verbatim history vs. aggressive summarization? 

A) There is no trade-off 

B) Full verbatim history preserves accuracy but grows context/cost over time; aggressive summarization saves space but risks losing specific details (progressive summarization risk) — the design must balance both per what's actually critical to retain 

C) Summarization always improves accuracy 

D) Verbatim history is always infeasible

Answer: B.

## 8. Escalation Decision-Making (Explicit Criteria + Few-Shot)

Designing **when an agent should hand off to a human** (or a different system) rather than continue autonomously — built the same way as Domain 4's explicit-criteria and few-shot principles: concrete, checkable escalation thresholds, reinforced with few-shot examples covering ambiguous boundary cases, not vague judgment calls.

**Q17.** An agent's escalation rule says "escalate if the situation seems complicated." Escalation behavior is wildly inconsistent across sessions. What's the fix, (consistent with Domain 4 principles applied here) ? 

A) Remove escalation entirely 

B) Replace the vague rule with explicit, checkable criteria (e.g., specific conditions/thresholds) and reinforce with few-shot examples of ambiguous cases and the correct escalation decision 

C) Escalate on every single turn to be safe 

D) Increase the model's temperature

Answer: B.

**Q18.** Why are boundary/ambiguous-case examples more valuable than clear-cut examples when teaching an agent escalation behavior? 

A) They aren't more valuable 

B) Boundary cases are easier to write 

C) Clear-cut cases are already handled correctly by default; ambiguous cases are where inconsistent behavior actually happens, so that's where examples add the most signal 

D) Only clear-cut examples should ever be used

Answer: C — same principle as Domain 4's few-shot targeting, applied specifically to escalation design.

## 9. Structured Error Propagation Across Multi-Agent Systems

When a subagent fails, the failure needs to be reported **upward in a structured, informative way** (what failed, why, what was attempted) so the coordinator or calling system can make an informed decision — rather than a raw crash, a silent failure, or an ambiguous "something went wrong" bubbling up.

**Q19.** In a hub-and-spoke system, a subagent silently fails and the coordinator receives no signal at all, proceeding as if the subtask succeeded. What's missing? 

A) A larger context window 

B) Structured error propagation — the subagent's failure needs to surface to the coordinator with enough detail to act on, instead of failing silently 

C) A cache_control breakpoint 

D) Conversation compaction

Answer: B.

**Q20.** What should a well-designed error propagated from a subagent to a coordinator include? 

A) Nothing — the coordinator should just retry blindly 

B) Only a generic "error" flag with no detail 

C) What failed, why it failed, and what was attempted — similar to Domain 2's structured tool-error design, but at the agent-to-agent level 

D) The subagent's entire raw context dump

Answer: C — mirrors Domain 2's structured tool error handling, now at the multi-agent coordination level.

## 10. Context Management in Large Codebase Exploration (Scratchpad Files & Subagent Delegation)

For large codebases, **dumping the whole repo into context doesn't scale**. Two key patterns:
* **Scratchpad files** — Claude writes findings/notes to a file on disk as it explores, instead of holding everything in the context window; the file becomes durable, offloaded memory.
* **Subagent delegation** — hand off exploration of a specific module/directory to a subagent with its own scoped, smaller context, reporting back a summary rather than dumping everything into the main session.

**Q21.** An agent exploring a 500-file repository tries to read every file into a single session's context to "understand everything first." What's the architectural problem, and the better pattern? 

A) No problem — more context is always better 

B) This will exhaust context budget fast and hit lost-in-the-middle/compaction issues; better to use scratchpad files to persist findings incrementally and/or delegate module-level exploration to subagents that report back summaries 

C) The fix is to switch to the Batch API 

D) The fix is a longer system prompt

Answer: B.

**Q22.** Why write exploration findings to a scratchpad file instead of just keeping them in the conversation context? 

A) A scratchpad file persists findings durably and outside the token budget, avoiding the risk that important discoveries get lost to summarization or lost-in-the-middle effects as the session grows 

B) Files are faster to read than context 

C) Scratchpad files replace the need for tools entirely 

D) This has no advantage over keeping everything in context

Answer: A.

**Q23.** When exploring an unfamiliar large codebase, why delegate to subagents scoped by module rather than one agent reading the whole codebase sequentially? 

A) It's slower and offers no benefit 

B) Each subagent gets a focused, smaller context relevant to just its module, avoiding context pollution in the main session, and can work in parallel, reporting back a condensed summary 

C) Subagents cannot read code 

D) This violates MCP rules

Answer: B.

# Realistic Scenario Questions (cross-topic)

**Q24.** A long-running coding session in Claude Code shows degrading recall of a requirement stated 80 turns ago, coinciding with several rounds of automatic compaction. Separately, cache hit rates have also dropped because the team recently started injecting a live "current context window %" stat at the very top of the system prompt. Diagnose both issues. 

A) Both issues are actually the same root cause 

B) 
Issue 1: progressive/compounding summarization loss from repeated compaction eroding early details — mitigate with a scratchpad or persisted state for critical facts. 
Issue 2: the dynamic stat at the top of the prefix invalidates the cache for everything after it — move volatile content to the end 

C) Both are caused by lost-in-the-middle only 

D) Neither issue is fixable

Answer: B — combines compaction/summarization risk with cache_control ordering rules.

**Q25.** A multi-agent research system has a coordinator dispatching 6 subagents across a large codebase. One subagent times out. The coordinator has no idea why and just reports "task failed" to the user. What two Domain 5 principles were violated, and what's the fix for each? 

A) Only one principle was violated  

B) This is purely a token-budget issue 

C) This is unrelated to any Domain 5 concept

D) Structured error propagation was missing (the subagent's failure detail never reached the coordinator) and the coordinator's own error reporting to the user should also be structured/specific rather than generic — fix both by defining clear error schemas at each hop

Answer: D.

**Q26.** An agent's escalation logic is vague ("escalate when unsure"), and separately, its raw tool outputs (full API JSON dumps) are never trimmed, causing it to hit context limits mid-task on complex cases — which are exactly the cases most likely to need escalation. How do these two problems compound each other, and what's the combined fix? 

A) Untrimmed verbose tool output eats the token budget fastest precisely on complex, high-tool-use cases — the same cases the vague escalation rule fails to catch — so context pressure and escalation failures compound on the hardest cases; fix by adding explicit escalation criteria (with boundary-case few-shot examples) AND trimming tool output to preserve budget for exactly those harder cases 

B) They're unrelated; fix independently and in either order 

C) The only fix needed is a bigger context window 

D) Only the escalation rule needs fixing

Answer: A — deliberately compounding two topics the way exam scenarios reportedly do.

# Quick References


| Concept | One-line definition |
| --- | --- |
| Prompt caching | Reuses computed prefix representation to cut cost/latency |
| cache_control breakpoint | Marks how much of the prompt prefix should be cached |
| Stable-first ordering | Put unchanging content first, volatile content last, to preserve cache hits |
| Lost-in-the-middle | Content in the middle of long context gets less reliable attention |
| Progressive summarization risk | Re-summarizing summaries compounds information loss over rounds |
| Conversation compaction | Built-in mechanism condensing session state to reclaim context space |
| Tool output trimming | Stripping unneeded bulk from verbose tool responses before they enter context |
| Token budget management | Proactively planning token usage across input, tools, and output headroom |
| Multi-turn conversation design | Deciding what persists, prunes, or summarizes across many turns |
| Escalation criteria | Explicit, checkable thresholds (not vague judgment) for handing off to a human |
| Structured error propagation | Failures reported upward with what/why/attempted detail, not silently or vaguely |
| Scratchpad file | Durable, on-disk notes offloading findings outside the context window |
| Subagent delegation (codebase) | Scoping exploration of a module to a subagent with focused context |


*Recurring exam pattern in this domain: problems that look like "context ran out" or "agent forgot something" usually trace back to one of a small set of root causes — cache-breaking prefix ordering, compounding summarization, untrimmed tool output, or missing structured state. Practice diagnosing which one before jumping to a fix.*

Referring to these questions just gives you an idea how the exam looks like, and can vary. Share if you have any answers or questions not correctly placed or explained.