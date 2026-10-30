---
title: "CCA-F Domain 4: Prompt Engineering and Structured Output"
date: 2026-10-27T08:14:16+05:30
draft: false
tags: ['CCAF', 'Claude', 'GenAI']
categories: ['Claude', 'CCAF']
showReadingTime: true
---

### As we discussed in the previous post on [Domain 3: Claude Code Configuration and Workflow](/post/cca-f-domain-3-claude-code-configuration-and-workflows-key-concepts), this part of the post will cover the Domain 4 which holds 20% weightage in the exam.

### If you have directly stumbled upon this page, I am preparing for the Claude Certified Architect — Foundations (CCA-F), and placing all types of practice questions that I encounter. This may help others, but objective is to keep track of key concept and some practice question that define the topics as well.

Where to Register: [https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)

> Unofficial practice set, written to match publicly reported blueprint topics — not sourced from the real exam bank. Use for concept drilling, not as a guarantee of exam content.

#### ***Topics Covered***

Explicit Criteria in Prompts (reducing false positives)

Few-Shot Prompting

Structured Output Enforcement (tool_use + JSON Schema)

tool_choice Modes (recap, applied to structured output)

Validation & Retry Loops

Batch Processing (Message Batches API)

Multi-Instance Review Architectures

Multi-Pass Review Architectures

## 1. Explicit Criteria in Prompts

Replacing vague instructions ("be conservative," "use good judgment") with **concrete, checkable thresholds and definitions** — exact numbers, explicit categories, clear boundaries. Vague criteria cause inconsistent behavior because "conservative" means something different call to call.

**Q1.** A fraud-review prompt says "flag transactions that seem risky." Reviewers report wildly inconsistent flagging. What's the root cause? 

A) The model is too weak for this task 

B) "Seems risky" is a vague criterion with no concrete threshold — different runs interpret it differently 

C) The prompt is too long 

D) This requires a multi-agent system, not a prompt fix

Answer: B — fix is to define explicit thresholds, e.g., "flag if amount > $10,000 AND shipping country ≠ billing country."

**Q2.** Which instruction is better designed to reduce false positives? 

A) "Only escalate if you're really sure it's a problem" 

B) "Escalate only if at least 2 of these 3 conditions are met: [explicit list]. If fewer than 2 are met, do not escalate even if something feels off." 

C) "Use your best judgment on escalation" 

D) "Escalate conservatively"

Answer: B — explicit, checkable conditions instead of subjective language.

**Q3.** True/False: Making criteria explicit primarily helps semantic correctness (getting the right answer), not just format consistency.

Answer: True — explicit criteria reduce inconsistent judgment calls, which is a correctness/precision problem, separate from output formatting.

## 2. Few-Shot Prompting

Providing **2–4 targeted examples** (input → correct output, ideally with brief reasoning) rather than relying purely on descriptive instructions. Most effective when examples target the cases the model **actually gets wrong** — ambiguous or overlapping categories — not just easy "happy path" cases.

**Q4.** A classification prompt has a long paragraph describing each category but still misclassifies edge cases. What's the more effective fix? 

A) Add 2–4 few-shot examples focused specifically on the ambiguous/boundary cases, including the reasoning for the correct label 

B) Make the paragraph even longer 

C) Remove all instructions and rely on zero-shot 

D) Increase max_tokens

Answer: A — few-shot examples targeted at hard cases beat longer descriptive instructions for consistency.

**Q5.** Why include the *rationale* in a few-shot example, not just the input/output pair? 

A) It's optional decoration 

B) The rationale teaches the model *why* that answer is correct, which generalizes better to new ambiguous cases than the answer alone 

C) Rationale is required by the API 

D) It has no effect on output quality

Answer: B.

**Q6.** A team writes 4 few-shot examples, all clear-cut "easy" cases with obvious answers. Classification accuracy barely improves. Why? 

A) Few-shot prompting doesn't work 

B) 4 examples is too many 

C) The examples should have been longer

D) Examples should target where the model actually struggles (ambiguous/overlapping cases); easy-case examples add little signal since the model already handles those correctly 

Answer: D.

## 3. Structured Output Enforcement (tool_use + JSON Schema)

Using a **tool call with a defined JSON Schema** (rather than asking Claude to "please output JSON" in prose) to force output into a fixed, parseable structure. 
* This guarantees **syntactic correctness** — no missing braces, no malformed JSON
* But does **NOT** guarantee **semantic correctness** — the structure can be perfectly valid and still contain a wrong answer.

**Q7.** A team asks Claude to "respond only in JSON" via plain prompt instructions, but production logs show occasional malformed JSON breaking the parser. What's the fix? 

A) Add more emphatic language like "IMPORTANT: only JSON!!" 

B) Switch to XML instead 

C) There is no fix; malformed output is unavoidable

D) Enforce structure via tool_use with a defined JSON Schema instead of relying on prompt-based formatting instructions 

Answer: D — programmatic enforcement (schema) vs. prompt-based guidance is a core distinction this domain tests directly.

**Q8.** A resume-parsing tool uses a JSON Schema and never produces malformed JSON. However, it sometimes extracts the wrong candidate's phone number into the phone field. What does this demonstrate? 

A) The schema is broken 

B) JSON Schema enforcement guarantees syntactic validity but not semantic correctness — the output can be well-formed and still wrong 

C) tool_use cannot be used for extraction tasks 

D) This means few-shot prompting failed

Answer: B — a specifically high-yield exam point per reported test-taker notes.

**Q9.** When designing a schema field for a category that might not cleanly fit any known option, which pattern is best? 

A) Include an "other" enum value paired with a free-text detail_string field to capture what didn't fit 

B) Force it into the closest existing enum value regardless of fit 

C) Leave the field out of the schema entirely 

D) Make every field nullable with no enum at all

Answer: A — schema design tip: `"other" + detail_string` avoids forcing bad fits into rigid categories, and also avoids losing information entirely.

**Q10.** Why might a schema field be marked nullable rather than always-required? 

A) Nullable fields are never allowed in JSON Schema 

B) Some information genuinely may not be present in the source input; forcing a required field invites the model to fabricate a value rather than honestly report "not found" 

C) It reduces token cost 

D) It has no practical purpose

Answer: B.

**Q11.** An extraction schema uses an "unclear" enum option for a confidence-sensitive field. What problem is this designed to prevent? 

A) The model guessing/fabricating a confident-sounding answer when the source data is genuinely ambiguous, instead of being able to honestly flag uncertainty 

B) Slower response times 

C) JSON parsing errors 

D) Tool selection errors

Answer: A.

## 4. tool_choice Modes Applied to Structured Output

(Builds on Domain 2) In structured-output contexts specifically: use a **forced/specific tool_choice** when the output must always conform to one schema; use auto when Claude should decide whether structured output or free text is appropriate for that turn; any when some tool call is required but which one is flexible.

**Q12.** A data-extraction pipeline must always return results in exactly one schema, with zero chance of a free-text response. Which tool_choice setting is correct? 

A) auto 

B) A forced/specific named tool 

C) none 

D) any

Answer: B.

**Q13.** A general-purpose assistant sometimes needs to extract structured data and sometimes just needs to chat normally. Which tool_choice setting fits this mixed use case? 

A) A forced specific tool always 

B) auto — letting Claude decide per-turn whether structured output is needed 

C) none at all times 

D) any

Answer: B.

## 5. Validation & Retry Loops

When extraction/output fails validation, **send back the original input + the specific validation error + the failed attempt**, and ask the model to correct it — rather than just re-asking from scratch. 

Important limitation: retry loops fix cases where the **correct data exists but was mis-extracted**; they do **NOT** help when the information simply **isn't present** in the source — no amount of retrying recovers data that was never there.

**Q14.** A validation-retry loop is built for a document-extraction system, but for a subset of documents the field being extracted was never present in the source text at all. Retries don't help. What's the correct diagnosis? 

A) The retry loop is poorly implemented and needs more attempts 

B) Retry loops fix mis-extraction of present data, not absence of data; more retries won't manufacture information that isn't in the source 

C) This means JSON Schema enforcement is broken 

D) The model needs a larger context window

Answer: B — a specifically called-out exam trap: know what retry loops can and can't fix before building one.

**Q15.** What should a well-designed retry prompt include after a validation failure? 

A) Just the original prompt again, unchanged 

B) A completely different prompt with no reference to the failure 

C) The original input, the specific validation error, and the failed attempt — giving the model concrete context on what went wrong 

D) Nothing — just increase temperature and retry

Answer: C.

**Q16.** A team keeps adding more retry attempts (now at 10 retries) to fix a persistently low extraction success rate, with no improvement. What should they check first? 

A) Whether the source documents actually contain the data being requested 

B) Whether temperature is set high enough 

C) Whether the schema has too many fields 

D) Whether tool_choice is set to auto

Answer: A — directly tests the retry-loop limitation above. 

## 6. Batch Processing (Message Batches API)

An API mode for processing **large volumes of independent requests asynchronously** — roughly **50% cost savings**, but with **up to a 24-hour processing window and no latency SLA**. 
* Right for large, non-urgent, non-blocking workloads (overnight reports, bulk classification).
* Wrong for anything a user or pipeline is actively waiting on.

**Q17.** A team wants to classify 500,000 historical support tickets overnight for an analytics dashboard, with no user waiting on the result. What's the appropriate approach? 

A) Real-time synchronous API calls for all 500,000, one at a time 

B) The Message Batches API — cost savings matter more than latency here, and there's no blocking wait 

C) A blocking CI/CD pipeline step 

D) Plan Mode

Answer: B.

**Q18.** A pre-merge CI check needs Claude's review before a developer can merge their PR (they're actively waiting). Should this use the Batch API? 

A) Yes, always use Batch API for cost savings 

B) No — batch processing has no latency SLA (up to 24 hours); blocking, developer-waiting workflows need synchronous calls, not batch 

C) Yes, because CI/CD always requires batch mode 

D) It doesn't matter which is used

Answer: B — explicitly called out: keep blocking workflows synchronous.

**Q19.** What is the main trade-off of using the Message Batches API? 

A) Higher cost, faster response 

B) No cost difference, just simpler code 

C) ~50% lower cost, but no latency guarantee — some requests may take up to 24 hours 

D) It only supports single requests, not batches

Answer: C.

## 7. Multi-Instance Review Architectures

Running **multiple independent instances/calls** of Claude on the same input (e.g., in parallel, with no shared context) and comparing/aggregating their outputs — used to catch inconsistency or improve confidence via consensus, since independent instances won't share the same blind spot.

**Q20.** A high-stakes classification task wants to reduce the chance of a single flawed judgment slipping through. What's a multi-instance approach to this? 

A) Run the same prompt once, trust the result 

B) Increase the prompt length once 

C) Use the Batch API instead

D) Run the same input through multiple independent Claude calls (no shared context) and compare results — e.g., flag for human review if they disagree 

Answer: D.

**Q21.** Why does an independent instance without prior generation context catch more errors during review than the same instance reviewing its own earlier output? 

A) Independent instances are always smarter 

B) The generating instance tends to rationalize/defend its own prior decisions; a fresh instance with no investment in the earlier output evaluates it more objectively 

C) There's no actual difference 

D) Independent instances have access to more tools

Answer: B — directly ties back to Domain 1's "same-session self-review" anti-pattern, tested again here from the structured-output angle.

## 8. Multi-Pass Review Architectures

Running review as **sequential passes**, each with a distinct, narrower purpose (e.g., pass 1: extract, pass 2: validate against source, pass 3: format/finalize) — rather than trying to do extraction, validation, and formatting all in one shot. Different from multi-instance (parallel, independent) — multi-pass is sequential and each pass builds on/checks the previous one.

**Q22.** An extraction pipeline currently tries to extract, self-validate, and format output all in a single prompt/call, with mixed reliability. What's a multi-pass redesign? 

A) Combine everything into an even longer single prompt 

B) Split into sequential passes — e.g., extract first, then a separate pass validates the extraction against the source, then a final pass formats — each with a narrow, focused job 

C) Run the same single-call prompt multiple times in parallel 

D) Switch to Batch API

Answer: B.

**Q23.** What's the key structural difference between multi-instance and multi-pass review architectures? 

A) Multi-instance runs independent parallel copies on the same input for comparison; multi-pass runs sequential, dependent stages where each stage has a distinct narrower job 

B) They are the same thing 

C) Multi-pass is always cheaper 

D) Multi-instance requires the Batch API

Answer: A.

# Realistic Scenario Based Questions (cross-topic)

**Q24.** A legal-document extraction system uses tool_use with a strict JSON Schema. QA reports zero malformed JSON in six months, but a recent audit found the system had been extracting the wrong party's name into the counterparty field for certain contract formats. What's the correct diagnosis and next architectural step? 

A) The schema is broken; add more required fields 

B) This is a semantic correctness issue, not a syntactic one — JSON Schema guarantees valid structure, not accuracy. Add few-shot examples targeting that ambiguous contract format, and/or a validation pass checking extracted values against the source 

C) Switch to prompt-based JSON instructions instead of tool_use 

D) This means the Batch API was misconfigured

Answer: B — combines Q7–8's core lesson with the fix from few-shot (Q4) and multi-pass validation (Q22).

**Q25.** A support-ticket triage system needs: 

(1) consistent escalation decisions instead of ad hoc judgment calls, and 

(2) recovery when a first extraction attempt mis-parses a field that IS present in the ticket text. 

Which two techniques directly address these two needs respectively? 

A) Batch API for both 

B) Multi-instance review for both 

C) Few-shot prompting for #1 only, nothing for #2

D) Explicit criteria (concrete escalation thresholds) for #1, and a validation-retry loop for #2 

Answer: D.

**Q26.** A pipeline classifies 2 million product listings nightly (no one waiting) and separately powers a live chat feature answering customer questions in real time. Which processing approach fits each, and why? 

A) Batch API for both, since batch always saves money 

B) Synchronous calls for both 

C) Batch API for the nightly 2M-listing job (non-blocking, cost matters more than latency); synchronous real-time calls for the live chat (user is actively waiting, no latency SLA is acceptable) 

D) Batch API for chat, synchronous for the nightly job

Answer: C

**Q27.** A code-review agent generates a fix, then reviews its own fix in the same session and approves it. A separate audit shows a different, fresh Claude instance catches issues the original missed. What principle explains this, and what architecture should the team adopt? 

A) The first instance is defective; replace the model 

B) Same-session self-review tends to rationalize prior output; adopt a multi-instance (independent reviewer) architecture instead of self-review 

C) This means multi-pass architecture is broken 

D) No architectural change is needed

Answer: B.

# Quick Reference Table


| Concept | One-line definition |
| --- | --- |
| Explicit criteria | Concrete, checkable thresholds instead of vague instructions |
| Few-shot prompting | 2–4 targeted examples (with reasoning) aimed at hard/ambiguous cases |
| tool_use + JSON Schema | Enforces syntactic structure; does NOT guarantee semantic correctness |
| "other" + detail_string | Schema pattern for values that don't fit existing enums |
| Nullable field | Lets the model honestly report "not found" instead of fabricating |
| "unclear" enum | Lets the model flag genuine ambiguity instead of guessing confidently |
| Validation-retry loop | Send input + error + failed attempt back; fixes mis-extraction, not absent data |
| Message Batches API | ~50% cheaper, up to 24hr window, no latency SLA — for non-blocking bulk work |
| Multi-instance review | Independent parallel calls compared/aggregated for consensus |
| Multi-pass review | Sequential stages, each with a narrow, distinct job |


*High-yield traps reported by past test-takers: *

*(1) JSON Schema = syntax only, not correctness (Q7-8, Q24); *

*(2) retry loops can't recover data that isn't in the source (Q14, Q16); *

*(3) Batch API vs synchronous is a latency/blocking decision, not just a cost decision (Q17-19, Q26); *

*(4) same-session self-review vs independent review reappears here from Domain 1, now framed around structured-output QA (Q21, Q27).*

Referring to these questions just gives you an idea how the exam looks like, and can vary. Share if you have any answers or questions not correctly placed or explained.