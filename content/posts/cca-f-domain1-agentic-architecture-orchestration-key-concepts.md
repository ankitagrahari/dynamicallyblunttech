---
title: "CCA-F Domain1: Agentic Architecture & Orchestration - Key Concepts"
date: 2026-10-27T08:14:28+05:30
draft: false
featureImage: "images/df024c_5399559a147b4ccf87b34be38643f27c.jpg"
tags: ['[]']
categories: ['["6a89342d6797a1f792f34566"]']
showReadingTime: true
---

### I am preparing for the Claude Certified Architect — Foundations (CCA-F), and placing all types of practice questions that I encounter. This may help others, but objective is to keep track of key concept and some practice question that define the topics as well.

Where to Register: [https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)

### Topics Covered
* agentic vs workflow vs conversational systems,
* the agentic loop (gather context → act → verify),
* task decomposition,
* sequential vs parallel execution,
* multi-agent orchestration (hub-and-spoke, coordinator/subagent patterns),
* hooks vs prompts,
* session resumption, and
* common anti-patterns.

> *Unofficial practice set, written to match publicly reported blueprint topics — not sourced from the real exam bank. Use for concept drilling, not as a guarantee of exam content.*

## Section A: Agentic Systems vs Simpler Patterns

#### ***Agentic System***: A system where **Claude decides its own next action** based on what happened before, instead of following a fixed script. The number of steps isn't known in advance — Claude figures it out as it goes.

*Think:* "Go find out X" (agentic) vs. "Do step 1, then step 2, then step 3" (not agentic).

#### ***Workflow (vs Agent): ***A **workflow** is a fixed, predictable sequence of steps written by a human. Claude might be used inside one step (like classifying something), but Claude doesn't decide the overall structure.

*Rule of thumb:* If you can draw the exact steps on a whiteboard beforehand, it's a workflow, not an agent.

#### ***Conversational System: ***The simplest pattern — a back-and-forth chat with no autonomous tool use or looping. One prompt in, one answer out.

**Q1.** A support workflow always follows the same 4 steps: classify ticket → fetch order → apply refund rule → send templated reply. Which architecture fits best? 

A) Fully autonomous agent with open-ended tool access 

B) A deterministic workflow with Claude used only at the classification step 

C) Multi-agent hub-and-spoke system 

D) A single conversational session with no tools

Answer: B — Fixed, predictable steps don't need agentic autonomy. Reserve agentic loops for tasks with unpredictable branching or unknown step count.

**Q2.** Which property is NOT a defining trait of an agentic system? 

A) The model decides its own next action based on tool results 

B) The number of steps is unknown in advance 

C) Output is generated in a single forward pass with no tool calls 

D) The loop continues until a task-completion condition is met

Answer: C — that describes a plain conversational/completion pattern, not an agentic one.

**Q3.** A team wants Claude to research a topic across an unknown number of sources and compile a report. What's the strongest justification for an agentic (vs workflow) approach here? 

A) Agentic systems are always cheaper 

B) The number and choice of sources can't be predicted ahead of time, so the model must decide dynamically 

C) Workflows can't call tools 

D) Agentic systems don't require verification steps

Answer: B.

## Section B: The Agentic Loop (Gather Context → Take Action → Verify)

## The Agentic Loop

The core cycle every agentic system runs through, repeatedly, until done:

**Gather context** – collect the info needed (read a file, call an API, search)

**Take action** – do something (call a tool, make a change)

**Verify** – check if that action actually worked / got closer to the goal

Repeat, or stop if the goal is met.

*Key idea:* this loop should keep going until a **real, checkable finish line** is hit — not until Claude just "feels" done.

**Q4.** In a well-formed agentic loop, what should determine when the loop terminates? 

A) A fixed number of turns set in the system prompt 

B) An explicit, checkable completion condition (e.g., tool result matches success criteria) 

C) The model's own natural-language judgment that it is "done" 

D) A hard timeout only

Answer: B — relying purely on the model saying "I'm done" (natural-language loop termination) is a known anti-pattern; termination should be verifiable.

**Q5.** An agent keeps calling a search tool even after finding the answer, because there's no verification step. What's missing from the loop? 

A) A retry policy 

B) A verify/check stage that confirms the goal state before exiting 

C) A system prompt 

D) Prompt caching

Answer: B.

**Q6.** Which is the best example of "verify results" in an agentic loop for a code-fixing agent? 

A) The agent states it believes the bug is fixed 

B) The agent re-runs the test suite and checks for a pass/fail signal 

C) The agent asks the user if it looks right 

D) The agent moves to the next task after one edit

Answer: B — verification should be a deterministic, checkable action, not a self-report.

**Q7.** True/False: Increasing max iterations in an agentic loop is a substitute for proper stop conditions.

Answer: False — a high iteration cap without real completion/failure conditions leads to runaway loops and wasted cost; it doesn't fix a missing termination signal.</details> 

## Section C: Task Decomposition & Sequential vs Parallel Execution

#### ***Task Decomposition:***

Breaking one big, messy task into **smaller pieces that can each be done and checked on their own**. Good decomposition splits along natural, independent chunks of work — not just "split the words in half."

#### ***Sequential Execution***

Steps run **one after another**, because each step needs the result of the one before it (e.g., you can't load data before you've validated it).

#### ***Parallel Execution***

Steps run **at the same time**, because they don't depend on each other (e.g., fetching data from two unrelated APIs). Parallel execution saves time but adds a challenge: someone has to **combine the results afterward**.

**Q8.** A task requires: 

(1) fetch data from API A, 

(2) fetch data from API B, 

(3) merge and summarize both. 

Which execution structure minimizes latency without sacrificing correctness? 

A) Fully sequential: A → B → merge 

B) A and B run in parallel (independent), then merge runs after both complete 

C) Fully parallel including merge 

D) Random order

Answer: B — independent subtasks parallelize; the dependent step (merge) must wait.

**Q9.** When decomposing a large task into subtasks for an agent, which is the strongest criterion for splitting? 

A) Split by number of words in the instructions 

B) Split along independent, verifiable units of work with clear success criteria 

C) Always split into exactly 3 subtasks 

D) Never split — one large task is more reliable

Answer: B.

**Q10.** A data-pipeline agent must 

(1) validate schema, 

(2) transform records, 

(3) load to warehouse — each step depends on the prior succeeding. 

What orchestration pattern is this? 

A) Parallel fan-out 

B) Sequential pipeline with dependency gating 

C) Hub-and-spoke 

D) Map-reduce

Answer: B.

**Q11.** Why might over-decomposing a task into too many tiny subagent calls hurt a system? 

A) It always improves accuracy 

B) It increases coordination overhead, latency, and cost without proportional benefit 

C) Claude cannot handle more than 2 subtasks 

D) It removes the need for verification

Answer: B.

## Section D: Multi-Agent Orchestration (Hub-and-Spoke, Coordinator/Subagent)

#### ***Multi-Agent Orchestration***

Using **more than one agent** to solve a task, instead of one agent doing everything. Usually one agent manages, others execute.

#### ***Hub-and-Spoke Pattern***

A specific multi-agent setup:
* **Hub (coordinator):** breaks the task down, hands out pieces to other agents, and combines their answers at the end.
* **Spokes (subagents):** each does one focused piece of work and reports back.

*Why use it:* keeps each subagent's job small and focused, so it doesn't get confused doing ten things at once.

#### ***Subagent***

A smaller, specialized agent that gets **its own separate context window** (its own "workspace") to do one job. Keeping it separate from the main agent stops irrelevant information from cluttering things up — this is called avoiding **context pollution**.

#### ***Coordinator***

Another name for the "hub" in hub-and-spoke — the agent in charge of splitting work up, sending it out, and merging results back together. Doesn't usually do the hands-on work itself.

#### ***Scoped Tool Access***

Giving each agent/subagent **only the tools it actually needs** for its job, not the entire toolbox. This limits how much damage a mistake can cause (smaller "blast radius") and keeps the agent focused.

**Q12.** In a hub-and-spoke multi-agent design, what is the role of the hub (coordinator)? 

A) It performs all the actual domain work itself 

B) It decomposes the task, dispatches to specialized subagents, and integrates their results 

C) It only logs errors 

D) It replaces the need for tool use

Answer: B.

**Q13.** Why use isolated subagents (separate context windows) instead of one large agent doing everything in a single context? 

A) Isolation prevents any tool use 

B) It keeps each subagent's context focused, reduces context pollution, and allows specialization 

C) It's required by the Claude API 

D) It removes the need for a coordinator

Answer: B.

**Q14.** A coordinator dispatches 5 subagents to research 5 competitors in parallel, then synthesizes a report. What risk does this pattern specifically introduce that a sequential single-agent approach wouldn't? 

A) Increased latency 

B) Inconsistent formatting/conflicting findings across subagents that the coordinator must reconcile 

C) Inability to use tools 

D) Loss of the system prompt

Answer: B — parallel independent subagents can return inconsistent or conflicting outputs; the coordinator's integration step must handle this.

**Q15.** Which scenario is the WEAKEST fit for multi-agent orchestration? 

A) Researching 10 independent topics in parallel 

B) A simple two-step task: fetch one value, format it into a sentence 

C) Reviewing a large codebase where each subagent audits a different module 

D) Running independent evaluations across multiple test scenarios

Answer: B — trivial, tightly coupled two-step tasks don't need orchestration overhead; a single call suffices.

**Q16.** What is a key architectural reason to give subagents restricted/scoped tool access rather than the full toolset? 

A) It's required by the API 

B) It limits blast radius and keeps each subagent's decision space aligned to its specific job 

C) It speeds up token generation 

D) It removes the need for permission checks

Answer: B.

## Section E: Hooks vs Prompts

#### ***Hooks***

**Hard, code-level rules** that run outside of Claude's own reasoning and can block, modify, or intercept an action *before it happens* — no matter what Claude "decides." Used when something absolutely must never happen (e.g., never delete production data).

*Key idea:* Hooks are **guaranteed**. They don't rely on Claude following instructions correctly.

#### ***Prompts (as a control mechanism)***

**Instructions written in plain language** that guide Claude's behavior by influence, not force. Good for soft preferences (tone, style) — but Claude *could* still deviate, especially under confusing input. Not safe for hard rules.

*Key contrast:* Hooks = guaranteed / deterministic. Prompts = likely / probabilistic.

**Q17.** You need to GUARANTEE that no agent ever writes to a production database, even if the model misunderstands instructions. What's the right mechanism? 

A) Add a strong instruction in the system prompt 

B) A deterministic hook/guardrail that blocks or intercepts the tool call before execution 

C) Ask the model to double-check itself 

D) Increase temperature to 0

Answer: B — prompts are persuasive, not enforced; hooks (or equivalent deterministic checks) are needed for hard guarantees.

**Q18.** When should you prefer a prompt-based instruction over a hook for controlling agent behavior? 

A) When the behavior must be 100% deterministic and safety-critical 

B) When the desired behavior is a matter of style, tone, or soft preference, not a hard constraint 

C) Never — hooks are always better 

D) When there is no tool use involved

Answer: B.

**Q19.** True/False: Hooks execute deterministically outside the model's reasoning, while prompts only influence the model's probabilistic behavior.

Answer: True.

## Section F: Session Resumption & State

#### ***Session Resumption***

The ability to **pick a long task back up where it left off** (e.g., after a crash or interruption) instead of starting over from scratch.

#### ***Checkpointing***

**Saving progress at intervals** during a long task, so that if something breaks, the system can resume from the last saved point instead of redoing already-finished (and already-verified) work.

#### ***stop_reason (the real termination signal)***

Every Claude API response includes a **stop_reason** field — this is the *correct, reliable* way to know whether Claude wants to keep going (e.g. tool_use) or has actually finished (end_turn). The exam treats checking stop_reason as the right answer, and **parsing Claude's text for phrases like "I'm done"** as the wrong one. This is the concrete, code-level version of "natural-language loop termination" below — good to know both the plain-English idea *and* this exact API term.

#### ***Context Sharing (for subagents)***

A design decision about **how much of the main agent's context a subagent gets to see** when it's spawned — full history, a summary, or just the specific inputs it needs. Too much shared context defeats the purpose of isolation; too little and the subagent lacks what it needs to do its job.

#### ***Spawning Strategy***

The rule for **when and how many subagents get created** — e.g., spawn one per independent subtask up front (parallel fan-out) vs. spawn subagents dynamically as the coordinator discovers new work.

#### ***Forking (workflows)***

Splitting an in-progress session into **multiple independent branches** that can each continue separately (e.g., to try two different approaches from the same checkpoint). Different from resumption — resumption continues *one* path after a stop; forking creates *multiple* paths from one point.

#### ***Workflow Handoffs***

The **hand-off point where one agent/session passes control (and relevant state) to another** — e.g., a triage agent handing a ticket to a specialist agent. Design questions here: what state transfers, what gets dropped, and how the receiving agent knows what already happened.

#### ***Over-Engineering (the #1 way this domain loses marks)***

Reaching for a **complex pattern (multi-agent orchestration, elaborate loops) when a simpler workflow or single agent call would solve the task just as well.** The exam specifically tests whether you can recognize when the simple answer is correct — not just whether you know the advanced patterns exist.

**Q20.** A long-running agentic task gets interrupted mid-way (process crash). What architectural feature allows it to continue without redoing completed work? 

A) A higher max_tokens setting 

B) Persisted session/task state that can be resumed from the last checkpoint 

C) A larger context window 

D) Prompt caching alone

Answer: B.

**Q21.** Why is checkpointing progress important in long multi-step agentic workflows? 

A) It reduces the model's temperature 

B) It allows recovery and resumption without re-executing already-verified steps, saving cost and avoiding duplicate side effects 

C) It's only relevant for parallel agents 

D) It replaces the need for verification

Answer: B.

## Section G: Anti-Patterns (High-Yield)

#### ***Natural-Language Loop Termination***

Ending an agentic loop just because **Claude says "I'm done"** in plain text, instead of checking a real, verifiable condition (like a test passing or a value matching). Risky because Claude can be wrong about its own completion.

#### ***Same-Session Self-Review***

Having the **same agent, in the same context**, both do the work AND grade whether the work is correct. Risky because it's checking its own homework — it shares the same blind spots and assumptions that led to the original output.

*Better approach:* verify with a separate process, a fresh context, or an independent check.

#### ***Tool Sprawl***

Giving an agent **too many tools**, especially ones that overlap or sound similar. This makes it harder for Claude to pick the *right* tool, wastes context space listing all the tool descriptions, and increases mistakes.

**Q22.** "Natural-language loop termination" refers to which anti-pattern? 

A) Ending a loop based on the model saying it's finished, rather than a checkable condition 

B) Using JSON instead of prose 

C) Terminating a loop after exactly one tool call 

D) Using hooks to stop a loop

Answer: A.

**Q23.** "Same-session self-review" as an anti-pattern means: 

A) The agent reviews its own output for tone 

B) The same agent instance/context that produced an output also grades/verifies its own correctness, introducing bias and blind spots 

C) Two subagents reviewing each other 

D) A human reviewing agent output

Answer: B — verification is more reliable when done by an independent process/context (or fresh session) than by the same context that generated the work.</details> 

**Q24.** "Tool sprawl" describes: 

A) Giving an agent too many tools with overlapping or unclear purposes, degrading its tool-selection accuracy 

B) Using too few tools 

C) A tool that calls other tools 

D) Parallel tool execution

Answer: A.

**Q25.** A team gives their agent 40 tools "just in case," many with similar names and overlapping functionality. What's the most likely consequence? 

A) Improved accuracy from more options 

B) Increased tool-selection errors and wasted context on tool schemas 

C) Lower latency 

D) No effect

Answer: B.

## Section H: Scenario-Style (Exam-Realistic)

**Q26.** You're designing an agent to triage incoming support tickets, and escalate to a human for billing disputes over $500 but auto-resolve everything else. Which combination of concepts from this domain applies MOST directly? 

A) Task decomposition only 

B) A workflow/agent hybrid with a deterministic guardrail (hook) enforcing the escalation threshold, not just a prompt instruction 

C) Pure conversational pattern 

D) Hub-and-spoke with 10 subagents

Answer: B — the $500 threshold is a hard business rule; it should be enforced deterministically (hook/code check), not left to the model's prompt-following.

**Q27.** An agent's loop keeps re-fetching the same API data 15 times because its "am I done?" check is a vague self-assessment prompt. Identify the two problems present. 

A) Tool sprawl and hub-and-spoke misuse 

B) Natural-language loop termination and missing verification step 

C) Session resumption failure and hook misuse 

D) Sequential vs parallel confusion

Answer: B.

**Q28.** A codebase-review system uses one coordinator to assign each subagent a different module, run them in parallel, then merge findings into one report, flagging conflicting recommendations for human review. Which best describes the design quality? 

A) Poor — should be sequential 

B) Good — matches hub-and-spoke pattern with parallel independent work and appropriate conflict handling at integration 

C) Poor — subagents should share one context 

D) Poor — no tools should be used

Answer: B.

## Quick Contrast Table


| Term | Term | Key Difference |
| --- | --- | --- |
| Agent | Workflow | Agent decides its own steps; workflow has fixed steps |
| Sequential | Parallel | Sequential = dependent steps; Parallel = independent steps, needs merging |
| Hooks | Prompts | Hooks = enforced by code; Prompts = suggested to the model |
| Hub | Spoke | Hub coordinates/merges; Spoke executes one focused job |
| Verification | Self-report | Verification = checkable proof; Self-report = Claude's own claim ("I'm done") |


## Quick Reference: Key Terms to Know Cold
* **Agentic loop:** gather context → take action → verify → repeat/terminate
* **Workflow vs agent:** fixed predictable steps vs model-driven dynamic steps
* **Hub-and-spoke:** coordinator decomposes + dispatches + integrates; subagents execute scoped work
* **Hooks vs prompts:** hooks = deterministic enforcement; prompts = probabilistic guidance
* **Session resumption:** checkpointed state enabling recovery without redoing work
* **Anti-patterns:** natural-language loop termination, same-session self-review, tool sprawl

*Study tip: for a 27%-weighted domain, expect scenario questions ("what's wrong with this design?") more than definition recall. Practice spotting anti-patterns in a described system.*

In next post we will look for [Domain 2: Tool design and MCP Integration.](/post/cca-f-domain-2-tool-design-and-mcp-integration-key-concepts)