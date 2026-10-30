---
title: "System Design with Agentic AI - 1"
date: 2026-10-27T08:14:22+05:30
draft: false
featureImage: "images/df024c_d1e02e494979447e8cb767d5f7199892.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

Agentic AI fails less often because of the model and more often because the system around the model was vague. The agent was given too much freedom, too little context, weak tools, no memory strategy, and no clear way to recover when things went wrong.

A good agent is not a chatbot with extra prompts. It is a system that can plan, call tools, inspect results, revise its path, and stop at the right time. That means **system design** matters. The planner, tools, skills, hooks, memory, retrieval, guardrails, and evaluation loop all shape whether the agent behaves like a careful assistant or a noisy automation script.

This article looks at the design choices that matter most when building agentic AI systems. It also explains when Retrieval-Augmented Generation, or RAG, helps and when it adds cost or confusion without improving the outcome.

## Agentic system design starts with the work, not the model

The first design question is not “***Which model should we use?***” 
It is “***What work must the system complete, and how much judgement does each step require?***”

Agentic AI fits tasks where the path is not fixed in advance. If every step is known, a normal workflow engine or deterministic service may be safer and cheaper. Agents earn their place when the system must interpret a goal, choose among tools, react to feedback, and handle variation.

Good use cases include:
* Investigating customer support issues across logs, tickets, and policies
* Drafting technical migration plans from codebase signals and internal standards
* Analysing procurement documents and asking for missing information
* Monitoring data quality issues and proposing fixes
* Assisting developers by reading files, running tests, and editing code under review

Weak use cases include:
* Simple form filling
* Fixed approval routing
* Tasks that need exact arithmetic without a verified calculation tool
* High-risk decisions with no human review
* Workflows where latency and cost must be tightly bounded

The core pattern is simple. Give the agent judgement where judgement is useful. Use deterministic systems where precision, speed, and repeatability matter more than flexibility.

A useful planning exercise is to split the work into four zones.


| **Zone** | **Best handled by** | **Example** |
| --- | --- | --- |
| Fixed logic | Code or workflow engine | Validate a GSTIN format before submission |
| Knowledge lookup | Search, RAG, or database query | Find the latest internal leave policy |
| Judgement | LLM reasoning with constraints | Decide whether a customer complaint is urgent |
| Action | Tool call with confirmation rules | Create a ticket or send a draft response |


This split prevents a common mistake: asking the language model to do everything. 

The model should reason and communicate. 

Tools should calculate, fetch, write, verify, and execute.

## Define the agent’s operating contract (Harness)

An agent needs a contract before it needs more tools. The contract states what the agent is allowed to do, what success looks like, and how it should behave when it is uncertain.

A strong operating contract includes:
* The agent’s goal
* The expected inputs and outputs
* Allowed tools and data sources
* Actions that need approval
* Stopping rules
* Error handling rules
* Privacy and security limits
* Evaluation criteria

For example, a support triage agent might have this contract:

> Classify incoming support tickets, identify likely cause, attach relevant policy or product references, suggest the next best action, and escalate tickets that involve payments, security, legal risk, or unclear customer intent.

This contract does not just describe the task. It sets limits. The agent can classify and suggest. It cannot issue refunds or make legal interpretations. It knows which cases need escalation.

### Use roles as design boundaries, not theatrical prompts

Many agent prompts start with “You are an expert…” That can help tone, but it does not create safe behaviour by itself. The role should map to actual system boundaries.

A useful role definition says:
* What the agent owns
* What the agent must not own
* Which tools it can call
* Which evidence it must cite
* Which cases it must hand off

For example, a finance document agent can extract fields, compare invoice terms to purchase orders, and flag differences. It should not approve payment unless the approval system has explicit business rules and human sign-off.

### Keep the plan visible

If the agent creates a plan, save it. If it changes the plan, save the reason. This makes failures easier to debug and improves user trust.

A plan record might include:
* Goal
* Assumptions
* Chosen steps
* Tool calls
* Observations
* Decision points
* Final result
* Confidence or uncertainty notes

This record is useful for audit, testing, and product improvement. It also helps identify whether the agent made a poor plan, used the wrong tool, received bad data, or misunderstood the request.

## Skills turn broad agents into reliable specialists

A skill is a reusable capability with a clear purpose, inputs, outputs, and constraints. Instead of asking one agent to “handle procurement,” define smaller skills such as vendor comparison, contract clause extraction, compliance checklist generation, and exception detection.

Skills make agentic systems easier to test. They also reduce prompt sprawl because each skill can carry its own instructions and examples.

A good skill has five parts.


| **Skill element** | **What it means** | **Example** |
| --- | --- | --- |
| Trigger | When the skill should be used | Use when a document contains vendor payment terms |
| Inputs | The required data | Contract text, vendor name, policy version |
| Process | The reasoning or tool steps | Extract clause, compare with policy, flag mismatch |
| Output | The structured result | Clause summary, risk level, evidence |
| Guardrails | Limits and escalation rules | Escalate if clause is missing or ambiguous |


> Design skills around frequent decisions

Do not create skills for every tiny action. Create them around decisions that repeat and need consistency.

For example, a software maintenance agent may need these skills:
* **Repository scan**

  Read project structure, package files, and test commands.
* **Issue reproduction**

  Run relevant tests or scripts in a controlled environment.
* **Patch proposal**

  Suggest a minimal code change and explain the trade-offs.
* **Regression check**

  Run the test suite and summarise failures.
* **Pull request draft**

  Prepare a human-readable change summary with affected files.

Each skill can be tested with sample repositories. Each can fail safely. The patch proposal skill should not merge code. The regression check skill should not hide failed tests. The pull request draft skill should not claim success if tests were skipped.

### Use structured outputs where possible

Free-form text is pleasant for users, but structured outputs are better for systems. If another component needs the agent’s result, ask for JSON or a typed schema.

For a triage agent, a structured output could include:

```json

{

  "category": "billing",

  "urgency": "high",

  "needs_human_review": true,

  "evidence": [

    "Customer reports duplicate debit",

    "Transaction reference included"

  ],

  "suggested_next_step": "Route to payments support queue"

}

```

This does three things. It makes downstream routing easier. It makes testing easier. It reduces the risk that a useful detail gets buried in a paragraph.

![Skills should be small enough to test and useful enough to reuse](images/df024c_dffce15e497e4170a91db4e20e8f3507.jpg "Skills should be small enough to test and useful enough to reuse")

## Hooks let the system guide the agent at the right moments

Hooks are event-driven interventions in the agent loop. They run before or after key actions, such as a tool call, retrieval step, plan update, or final response. They help enforce policy, add context, check quality, and route control.

Think of hooks as system-level checkpoints. The model can reason, but hooks keep the process safe and consistent.

Common hook points include:
* Before planning
* After planning
* Before a tool call
* After a tool result
* Before retrieval
* After retrieval
* Before user-facing output
* After task completion

### Pre-planning hooks set the ground rules

A pre-planning hook can enrich the task with user permissions, tenant settings, feature flags, locale, and risk category. It can also reject tasks that should not reach the agent.

For example, a loan support assistant in India may receive a customer query about repayment charges. A pre-planning hook can attach the customer’s product type, language preference, and current policy version. It can also block the agent from giving personalised financial advice beyond approved support content.

### Tool hooks prevent costly or unsafe actions

A before-tool hook can check whether a proposed tool call is allowed. An after-tool hook can validate the result.

For example, before a ticketing agent creates a Jira issue, a hook can check:
* Does the user have permission?
* Is the project key valid?
* Is the title too vague?
* Does a similar issue already exist?
* Does this action need user confirmation?

After the tool call, another hook can verify the issue ID and store the event.

This pattern matters because agents may call tools based on partial understanding. Hooks give the system a second layer of control.

### Output hooks improve final quality

Before sending a final answer, an output hook can check whether the response:
* Cites required evidence
* Avoids restricted claims
* Includes uncertainty where needed
* Uses the right language and format
* Matches the requested schema
* Does not expose sensitive data

This is especially useful when agents combine internal data, retrieved documents, and generated reasoning. The final answer is the point where errors become user-visible.

## Memory needs design, not accumulation

Many agent projects treat memory as a bin where everything gets stored. That creates noise, privacy risk, and strange future behaviour.

Memory should answer a design question: What should the agent remember to do future work better?

There are several memory types.


| **Memory type** | **Purpose** | **Example** |
| --- | --- | --- |
| Session memory | Keep context during one task | User already said the invoice period is April 2025 |
| User preference memory | Carry stable preferences | User wants summaries in bullet points |
| Task memory | Track progress | Three files were already checked |
| Domain memory | Store reusable knowledge | Internal escalation policy |
| Episodic memory | Learn from past cases | Similar error appeared after package upgrade |


Each type needs different retention rules. Session memory can expire quickly. Domain memory needs governance and versioning. User preference memory should be editable. Episodic memory should be curated because bad memories can pollute future work.

### Do not confuse memory with truth

Stored memory is not automatically correct. A user may state something wrong. A past task may have reached a poor result. An old policy may no longer apply.

Design memory with freshness and evidence. Attach dates, source references, and confidence where needed. Give the agent rules for when to trust memory and when to verify.

For example, a travel policy assistant should not rely on a remembered meal allowance from last year. It should check the current policy source before answering.

## RAG helps when the agent needs external knowledge

Retrieval-Augmented Generation connects a model to external documents or data. The system retrieves relevant content, gives it to the model, and asks the model to answer using that context.

RAG is valuable when the answer depends on knowledge that is too large, too private, too new, or too changeable to live in the model’s training data.

Good RAG scenarios include:
* Internal policy question answering
* Product support over changing documentation
* Legal or compliance research with citation needs
* Technical support using logs, tickets, and runbooks
* Knowledge assistants for large document repositories
* Agents that need evidence before taking action

For example, an HR assistant for a nationwide Indian company may need to answer questions about leave, probation, reimbursements, and regional holidays. The model should not guess. It should retrieve the current HR policy, cite the relevant section, and respond in plain language.

RAG also helps when the agent must show evidence. A generated answer without sources may sound confident but be hard to trust. Retrieved passages give users and reviewers something to inspect.

### Use RAG as part of the agent loop

In agentic systems, retrieval should not be a one-time step before generation. The agent may need to search, inspect, refine the query, and search again.

A common pattern is:

Interpret the user’s goal.

Decide what knowledge is needed.

Retrieve documents.

Inspect whether the documents are sufficient.

Ask a narrower follow-up query if needed.

Answer with citations or take the next tool action.

A procurement agent reviewing a vendor agreement may first retrieve the contract policy. Then it may retrieve approved clause examples. Then it may retrieve past exception decisions. Each retrieval has a purpose.

## RAG is not useful for every agent

RAG can make a system slower, more expensive, and harder to debug. It can also introduce irrelevant context that distracts the model.

Use RAG when the task needs grounded knowledge. Skip it when the task mainly needs reasoning over information already in the prompt, a direct database lookup, or tool execution.

RAG may not be beneficial in these cases.

### The answer should come from a structured system

If the agent needs an order status, account balance, inventory count, or booking state, use an API or database query. Do not retrieve a document that describes where the data might be.

A customer asking “Where is my order?” needs live order data. RAG over shipping policy pages may explain delivery timelines, but it cannot replace the order management system.

### The knowledge is small and stable

If the task needs a short, stable rule set, place it directly in the system prompt or configuration. RAG adds needless retrieval risk.

For example, if an internal bot must always format dates as `DD MMM YYYY` and amounts in Indian numbering style, this rule can live in the prompt or output formatter.

### The task needs exact computation

RAG does not calculate. If the agent needs to compute tax, compare large tables, or validate totals, use a calculator, code execution, or a verified business service. Retrieved documents may explain the formula, but a tool should perform the calculation.

### The corpus is low quality

RAG only helps when the source content is useful. If documents are outdated, duplicated, contradictory, or poorly chunked, retrieval may return convincing nonsense. Fix the corpus before adding more agent logic.

Bad RAG often looks like a model problem. The real issue is source quality.

### The user needs a creative or strategic draft

If a user asks for a brainstorming list, a rewrite, or a high-level planning draft based on information in the prompt, RAG may not add value. It can even make the output stiff by forcing irrelevant retrieved text into the response.

## Build a retrieval strategy before choosing a vector database

Many teams start RAG design by picking a vector store. That is backward. Start with the retrieval behaviour the agent needs.

Key decisions include:
* Which sources are trusted?
* How often do they change?
* What metadata matters?
* How should documents be chunked?
* Should retrieval use keyword search, vector search, or both?
* How many passages should be returned?
* Should the agent rerank results?
* How should citations appear?
* What should happen when retrieval finds nothing useful?

### Good chunking reflects the task

Chunking is not just splitting documents every few hundred tokens. The chunk should match how people use the information.

For policies, chunk by clause or section. For API docs, chunk by endpoint. For troubleshooting guides, chunk by symptom and fix. For legal documents, preserve section numbers and definitions.

A chunk should be large enough to contain meaning but small enough to avoid burying the relevant line.

### Metadata improves retrieval quality

Metadata helps the system filter before ranking. Useful metadata may include:
* Document type
* Department
* Product version
* Region
* Effective date
* Access level
* Owner
* Language
* Status

For a nationwide support system, region and policy version often matter. An agent answering a payroll question should not mix old and new policy versions, or confuse one state-specific rule with another.

### Retrieval needs failure behaviour

The agent should know what to do when retrieval fails. It should not invent.

Good failure responses include:
* Ask a clarifying question
* Say the relevant source was not found
* Route to a human reviewer
* Use a safe general response with clear limits
* Trigger a document quality issue for the content team

Failure behaviour is a product decision, not just a model setting.

## Planning needs control over depth and cost

Agentic systems can overthink. A task that needs one search becomes six tool calls, three reflections, and a costly final answer. A task that needs careful analysis gets a shallow response.

Design the planning loop with limits and escalation.

Useful controls include:
* Maximum number of steps
* Maximum tool calls by tool type
* Time budget
* Cost budget
* Required evidence threshold
* Confidence threshold
* Human review triggers
* Retry limits
* Stop conditions

For example, a log analysis agent could follow this rule:

If the agent cannot identify a likely cause after three relevant log queries and one runbook search, it must summarise findings and escalate.

This stops the agent from wandering. It also gives engineers a clear failure packet.

### Use different planning modes

Not every task needs the same agent loop. Three modes work well in practice.


| **Mode** | **Use when** | **Behaviour** |
| --- | --- | --- |
| Fast path | The task is simple and low risk | Answer or act with minimal tool use |
| Standard path | The task needs evidence or several steps | Plan, retrieve, use tools, verify |
| Careful path | The task is high impact or ambiguous | Add review, stronger checks, and stricter citations |


A support bot might use the fast path for “How do I reset my password?” It should use the careful path for “I was charged twice and need my money back.”

## Evaluation should test behaviour, not just answers

Agentic AI evaluation must cover the full loop. A correct final answer can hide a poor process. A poor final answer may come from a good plan with bad retrieval.

Evaluate these layers separately:
* Intent understanding
* Plan quality
* Tool selection
* Tool argument correctness
* Retrieval relevance
* Evidence use
* Safety and policy compliance
* Final answer quality
* Cost and latency
* Recovery from failure

Create test cases from real tasks, anonymised where needed. Include normal cases, edge cases, missing data cases, permission failures, and conflicting document cases.

### Track traces for every run

A trace is the agent’s execution record. It should show prompts, tool calls, retrieved chunks, intermediate decisions, hook outcomes, and final output.

Traces help answer practical questions:
* Did the agent search the right source?
* Did retrieval return the right passage?
* Did the model ignore the evidence?
* Did a hook block the right action?
* Did the agent stop too early?
* Did it ask for human review when needed?

Without traces, debugging becomes guesswork.

### Use human review where judgement is expensive

Some tasks should not be fully automated. Human review is part of good system design, not a sign of failure.

Review is useful when:
* The action has financial, legal, or safety impact
* The agent’s confidence is low
* Source documents conflict
* The user disputes the result
* The task falls outside known patterns
* The agent proposes an irreversible action

A well-designed system routes only the right cases to humans. It should include the agent’s evidence, plan, and uncertainty so the reviewer does not start from zero.

## A practical design pattern for an agentic system

A strong agentic architecture often has these components:

**Task intake**

Parse the user goal, collect required fields, and assign risk level.

**Context builder**

Add user permissions, tenant settings, locale, session history, and relevant memory.

**Planner**

Decide the steps, tools, and retrieval needs.

**Skill router**

Select reusable skills instead of one giant prompt.

**Retrieval layer**

Search trusted knowledge sources when needed.

**Tool layer**

Call APIs, databases, code runners, ticketing systems, or calculators.

**Hook layer**

Enforce policy before and after key actions.

**Verifier**

Check evidence, output format, and task completion.

**Human review**

Route risky or unclear cases with full trace context.

10. **Learning loop**

    Use traces, feedback, and test failures to improve skills, hooks, retrieval, and prompts.

Here is a practical example.

A field service agent receives this request:

“Create a plan to fix repeated inverter shutdowns at Site A. Check past incidents, current device logs, and maintenance notes.”

The system could work like this:
* Intake classifies the task as technical diagnosis.
* Context builder adds site access permissions and device type.
* Planner decides it needs incident history, logs, and maintenance records.
* Retrieval gets maintenance notes and runbooks.
* Tool calls fetch recent telemetry and event logs.
* A diagnostic skill compares symptoms with known failure patterns.
* A hook blocks the agent from scheduling physical work without approval.
* The verifier checks whether the plan cites evidence.
* The final response gives likely causes, recommended checks, required parts, and open uncertainties.
* Human review is triggered if the recommendation includes safety-sensitive electrical work.

This is agentic AI used well. The model reasons across messy inputs. Tools fetch live facts. RAG grounds the answer in trusted documents. Hooks prevent unsafe action. Review catches high-impact cases.

## Tips for building agents that behave well in production

Start narrow. Choose a task with clear value, visible outcomes, and examples of past work. Avoid starting with a broad “AI assistant for everything.”

Write down the agent contract before writing prompts. If the boundaries are unclear in design, they will be unclear in production.

Prefer small skills over one large prompt. Skills can be tested, reused, and improved without changing the whole system.

Give tools strict schemas. Validate tool arguments before execution. Treat every tool call as a system boundary.

Use RAG only when the answer needs grounded knowledge. Build source quality, metadata, and failure handling before worrying about model tricks.

Add hooks early. Retrofitting policy checks after the agent has grown usually creates brittle patches.

Log traces from day one. The first production issue will need them.

Measure cost and latency by task type. A careful agent is useful only if it fits the product experience and budget.

Keep humans in the loop for high-risk work. The best systems combine machine speed with human responsibility.

## The takeaway

Planning system design with Agentic AI Skills Hooks and Smart RAG Use is about assigning responsibility clearly. The model should reason, but it should not carry the whole system. Skills package repeatable expertise. Hooks enforce rules at the right moments. Tools handle facts and actions. RAG grounds answers when external knowledge is needed, but it should not replace databases, calculators, or clean workflow design.

The most reliable agentic systems are not the ones with the most freedom. They are the ones with the clearest contracts, the best evidence paths, the smallest useful skills, and the strongest feedback loops. Build the system so the agent can succeed, and design every boundary so it can fail safely.

Hopefully this will add more order in the chaos of the AI world, where if you see everything is a prompt. You can also follow my work on my github account [https://github.com/ankitagrahari](https://github.com/ankitagrahari)