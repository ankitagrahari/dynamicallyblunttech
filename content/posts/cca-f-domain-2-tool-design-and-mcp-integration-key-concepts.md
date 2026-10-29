---
title: "CCA-F Domain 2: Tool Design and MCP Integration - Key Concepts"
date: 2026-10-27T08:14:13+05:30
draft: false
featureImage: "images/df024c_5399559a147b4ccf87b34be38643f27c.jpg"
tags: ['[]']
categories: ['["6a89342d6797a1f792f34566"]']
showReadingTime: true
---

### As we discussed in the previous post on [Domain 1-Agentic Architecture and Orchestration](/post/cca-f-domain1-agentic-architecture-orchestration-key-concepts), this part of the post will cover the Domain 2 which holds 18% weightage in the exam.

### If you have directly stumbled upon this page, I am preparing for the Claude Certified Architect — Foundations (CCA-F), and placing all types of practice questions that I encounter. This may help others, but objective is to keep track of key concept and some practice question that define the topics as well.

Where to Register: [https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification)

> Unofficial practice set, written to match publicly reported blueprint topics — not sourced from the real exam bank. Use for concept drilling, not as a guarantee of exam content.

#### ***Topics Covered***
* Tool Design Principles (descriptions, boundaries)
* Input Formats, Examples & Edge Cases
* Structured Error Handling
* Tool Distribution Across Agents
* Tool Choice Configuration (tool_choice)
* Tool Selection / Routing Behavior
* Model Context Protocol (MCP) — Core Concepts
* MCP Servers, Clients, and Resources
* MCP Transport (stdio vs SSE/HTTP) — Trade-offs
* Authentication Patterns for MCP
* Built-in Claude Tools
* Scoped Permissions & Safe Tool Usage
* Tool Schemas (writing reliable ones)
* Integrating MCP into Claude Code / Agent workflows

## 1. Tool Design Principles — Descriptions & Boundaries

A **tool description** is the plain-English explanation you give Claude about what a tool does, when to use it, and what it returns. 

**Boundaries** mean making clear what the tool is *for* and *not for*, so Claude doesn't reach for it in the wrong situation. Vague or overlapping descriptions cause Claude to pick the wrong tool.

**Key rule:** the description should read like documentation for a new team member — purpose, when to use it, and when NOT to use it.

**Q1.** Two tools exist: search_orders and lookup_order, with near-identical descriptions. What problem does this most likely cause? 

A) Faster tool selection 

B) Claude may call the wrong one, or waste a call trying both 

C) No effect — Claude always picks correctly 

D) It reduces token usage

Answer: B — overlapping/unclear boundaries between similarly-named tools cause tool-selection errors.

**Q2.** Which tool description is best? 

A) "get_data — gets data" 

B)  "invoice_tool — does invoice stuff, also sometimes orders" 

C) "get_customer_invoice — retrieves a single invoice by invoice ID; use only for invoice lookups, not for order or shipping data"

D) No description, rely on the function name

Answer: C — specific purpose, specific scope, explicit exclusion.

**Q3.** True/False: A tool's name alone (without a description) is usually sufficient for reliable tool selection.

Answer: False — names are ambiguous at scale; descriptions carry the real signal.

## 2. Input Formats, Examples & Edge Cases

Specifying the **exact shape of input** a tool expects (data types, required vs optional fields, formats like date strings), plus **example calls** and **known edge cases** (empty results, invalid IDs) so Claude knows how to call the tool correctly and what to expect back.

**Q4.** A get_weather tool expects a date as YYYY-MM-DD but the schema just says date: string. What's the risk? 

A) None, Claude always guesses correctly 

B) The tool will auto-correct any format 

C) Claude may pass an ambiguous format (e.g. "tomorrow" or "03/04/2026"), causing tool errors 

D) This only matters for numeric fields

Answer: B — always specify exact format expectations, ideally with an example in the description.

**Q5.** Why include example queries/example calls in a tool's description? 

A) They're required by the MCP spec 

B) They anchor Claude's understanding of correct usage, especially for less-common parameter combinations 

C) They replace the need for a schema 

D) They reduce the tool's latency

Answer: B.

**Q6.** A search_products tool has no defined behavior for "zero results found." What should the tool design account for? 

A) Nothing — Claude will assume success 

B) The tool should throw a fatal error

C) Zero-result cases can't happen 

D) An explicit edge case: define what's returned (e.g., empty array + message) so Claude doesn't misinterpret it as an error or hallucinate results 

Answer: D.

## 3. Structured Error Handling

Instead of returning a raw crash or a vague failure, a well-designed tool returns **structured, informative error responses** (e.g., {"error": "invalid_order_id", "message": "..."}) so Claude can understand *what* went wrong and decide what to do next (retry, ask user, try a different tool).

**Q7.** A tool fails and returns just "Error" with no detail. What's the consequence for the agent loop? 

A) Claude will always retry correctly 

B) No consequence, the loop still terminates properly 

C) Claude lacks enough information to decide the right recovery action (retry vs. abort vs. ask for clarification) 

D) This is the correct way to signal failure

Answer: C.

**Q8.** Which is a well-structured tool error response? 

A) "failed" 

B) {"status": "error", "error_code": "insufficient_funds", "message": "Account balance is $12, requested $50", "retryable": false} 

C) An HTTP 500 with no body 

D) Silently returning an empty string

Answer: B — structured, specific, and tells Claude whether retrying makes sense.</details> 

**Q9.** Why should error responses indicate whether a failure is retryable? 

A) It's purely cosmetic 

B) MCP requires this field 

C) It has no effect on agent behavior

D) It lets Claude (or the orchestrating code) decide whether to retry automatically or escalate/stop 

Answer: D.

## 4. Tool Distribution Across Agents

Deciding **which tools go to which agent/subagent** in a multi-agent system. Related to "scoped tool access" from Domain 1, but here it's specifically about designing the tool *set* per role.

**Q10.** In a hub-and-spoke system, a "billing subagent" and a "shipping subagent" both get the exact same full toolset of 20 tools. What's the design flaw? 

A) None — more tools is always better 

B) Tools should be distributed by role; giving both agents the same broad set increases confusion and misuse risk instead of scoping tools to each agent's actual job 

C) This is required by MCP 

D) Subagents cannot have different toolsets

Answer: B.

**Q11.** What's a good principle for distributing tools across a multi-agent system? 

A) Every agent gets every tool "just in case" 

B) Each agent gets the minimal set of tools required for its specific responsibility 

C) Only the coordinator should have any tools 

D) Tool distribution doesn't affect reliability

Answer: B.

## 5. Tool Choice Configuration (tool_choice)

An API-level setting controlling **how Claude is allowed to use tools** in a given call:
* auto — Claude decides whether to call a tool or just respond in text
* any — Claude must call *some* tool, but picks which one
* tool (specific) — Claude is forced to call one named tool
* none — Claude must not call any tool

**Q12.** You want to force Claude to always extract data using exactly one specific tool, never respond in free text. Which tool_choice setting fits? 

A) auto 

B) any 

C) A specific named tool (tool choice) 

D) none

Answer: C.

**Q13.** In an open-ended research agent where Claude should decide for itself whether a tool is needed at each step, which setting is correct? 

A) auto 

B) none 

C) A specific forced tool 

D) any

Answer: A.

**Q14.** When would tool_choice: none make sense? 

A) When you want Claude to guarantee a tool call 

B) When you want a plain text-only response for this turn, with no tool use, even though tools are defined 

C) When no tools exist at all 

D) Never — this option doesn't exist

Answer: B.

## 6. Tool Selection / Routing Behavior

How Claude decides **which tool (of many available) to call** for a given task — driven by description quality, boundaries, and how distinct the tools are from each other. "Routing" here means the agent choosing the correct path/tool based on the input.

**Q15.** A customer query "Where's my order?" could match both track_shipment and get_order_status. What causes ambiguous routing here? 

A) Descriptions/boundaries that don't clearly differentiate the two tools' purposes 

B) Claude cannot handle 2 similar tools 

C) MCP protocol limitation 

D) The query is too long

Answer: A.

**Q16.** What's the best fix for chronically incorrect tool routing between two similar tools? 

A) Delete both tools 

B) Increase temperature 

C) Sharpen the descriptions to clarify distinct purpose/scope, or merge them if they're truly redundant 

D) Add more unrelated tools to dilute the choice

Answer: C.

## 7. Model Context Protocol (MCP) — Core Concepts

MCP is an **open standard/protocol** that lets AI applications connect to external tools, data sources, and systems in a consistent way. Three core roles:
* **Host** — the application the user interacts with (e.g., Claude Code, Claude Desktop)
* **Client** — lives inside the host, manages one connection to one MCP server
* **Server** — exposes tools, resources, and prompts to the client

**Q17.** What is the relationship between an MCP host and an MCP client? 

A) They are the same thing 

B) The host application contains one or more clients, each client maintaining a 1:1 connection to a server 

C) The client is external to the host 

D) A host can only ever have one client

Answer: B.

**Q18.** What does an MCP **server** expose to a client? 

A) Only raw text 

B) Tools, resources, and prompts 

C) Only the model weights 

D) Nothing — servers are passive

Answer: B.

**Q19.** Why does MCP exist as a standard, rather than every integration being custom-built? 

A) To make integrations harder 

B) To give a consistent, reusable way for any AI app to connect to any tool/data source, instead of N×M custom integrations 

C) It's only for Anthropic's internal use 

D) It replaces the need for tool schemas

Answer: B.

## 8. MCP Servers, Clients & Resources

Beyond tools, MCP servers can expose **resources** (read-only data the client can fetch, like files or records) and **prompts** (reusable prompt templates the server provides). A **server** is typically a discrete process/service tied to one system (e.g., a GitHub MCP server, a Postgres MCP server).

**Q20.** What's the difference between an MCP **tool** and an MCP **resource**? 

A) No difference 

B) A tool is an action Claude can invoke (with side effects or computation); a resource is more like readable data/context the client can pull in 

C) Resources can only be used by the server, never the client 

D) Tools are read-only, resources are write-only

Answer: B.

**Q21.** A team wants to connect Claude to both a GitHub repo and a company Postgres database. What's the correct MCP architecture? 

A) One server handling both, undifferentiated 

B) MCP doesn't support databases 

C) A single client with no server

D) Separate MCP servers, one per system, each exposing tools/resources scoped to that system

Answer: D — MCP servers are typically scoped to one system/integration. 

## 9. MCP Transport — stdio vs SSE/HTTP Trade-offs

**Transport** is *how* the client and server communicate. Common options:
* **stdio** — local process communication (client launches server as a subprocess); simple, fast, good for local tools, but tied to one machine.
* **SSE / HTTP (remote/streamable HTTP)** — server runs remotely, communicates over network; enables remote/shared servers, multiple clients, but adds network latency, auth complexity, and connection management concerns.

**Q22.** You're building an MCP server that must be shared across many users' Claude Code instances from a central deployed service. Which transport fits better? 

A) stdio 

B) SSE/HTTP (remote transport) 

C) Neither — MCP doesn't support remote servers 

D) It doesn't matter

Answer: B — remote/shared access needs a network transport, not a local subprocess. 

**Q23.** What's a trade-off of choosing stdio transport for an MCP server? 

A) It requires complex authentication 

B) It's local-only — tied to the machine running the client, not shareable across users/services 

C) It's always slower than SSE 

D) It can't expose tools

Answer: B.

**Q24.** What's a key operational concern introduced specifically by SSE/HTTP transport that stdio doesn't have? 

A) Tool schema design 

B) Authentication, network reliability, and connection/session management over the wire 

C) The need for tool descriptions 

D) Structured error handling

Answer: B.

## 10. Authentication Patterns for MCP

How an MCP **client proves its identity / gets authorized access** to a server, especially for remote servers. Patterns include API keys, OAuth flows, and scoped tokens — chosen based on whether the server is local/trusted or remote/multi-tenant.

**Q25.** A remote MCP server exposes access to a company's internal ticketing system for multiple external users. What's the most appropriate authentication approach? 

A) No authentication needed since it's "just a tool" 

B) A proper auth flow (e.g., OAuth or scoped tokens) so each user only accesses data they're authorized for 

C) A single shared static API key hardcoded into every client 

D) Authentication is handled automatically by MCP with no configuration

Answer: B.

**Q26.** Why is a single shared credential across all users of a remote MCP server considered a poor pattern? 

A) It's more efficient 

B) MCP forbids shared credentials technically 

C) It removes per-user access boundaries — one compromised client exposes everyone's access, and you can't scope permissions per user 

D) It's actually the recommended pattern

Answer: C.

## 11. Built-in Claude Tools

Tools Claude/Claude Code ships with out of the box, without needing an MCP server — e.g., file tools (**Read, Edit, Write, Glob, Grep**), and execution tools (**Bash**). These handle common local dev tasks; MCP is for *external/custom* integrations beyond these.

**Q27.** When should you build a custom MCP tool instead of relying on Claude Code's built-in file tools? 

A) Never — built-ins cover every case 

B) Built-in tools should always be replaced by MCP 

C) MCP tools are only for file operations too

D) When the task needs access to something outside the local filesystem/shell — e.g., an external API, database, or SaaS product 

Answer: D.

**Q28.** What is Grep (as a built-in tool) primarily used for? 

A) Editing files 

B) Searching file contents for patterns 

C) Making network requests 

D) Running shell scripts

Answer: B.

**Q29.** User is requesting to look for all *.md files which are present in folder to read the architecture prepared by Claude. Which tool will be used for file name search ?

A) glob

B) grep 

C) bash

D) wildcard search not possible

Answer: A - **Glob** finds files **by name pattern** — you give it something like *.java or **/*[Controller.java](http://Controller.java) and it returns a list of matching file paths. It doesn't look inside the files at all.

## 12. Scoped Permissions & Safe Tool Usage

Restricting **what a tool/agent is allowed to do** — e.g., read-only vs. write access, which directories/records it can touch, or requiring approval before high-risk actions run. This is the practical safety layer around tool use.

**Q30.** A code-review agent should be able to read any file in a repo but should NEVER be allowed to push to the remote or delete branches. How should this be enforced? 

A) A prompt instruction asking it nicely not to 

B) Trust the model's judgment alone 

C) Scoped permissions / hooks that technically restrict which tools or actions are available, not just prompt-level requests 

D) Give it all tools and monitor after the fact only

Answer: C — consistent with Domain 1's hooks-vs-prompts distinction: hard restrictions need enforcement, not persuasion.

**Q31.** What does "safe tool usage" mean in the context of an agent with filesystem access? 

A) Giving it unrestricted access for convenience 

B) Disabling all tools 

C) Only using tools that have no side effects, ever

D) Scoping access to only the necessary directories/files and requiring confirmation for destructive actions 

Answer: D.

## 13. Tool Schemas (Writing Reliable Ones)

The **formal, structured definition** of a tool's inputs (JSON Schema-style: types, required fields, enums, descriptions per field) that Claude uses to know exactly how to call it. Good schemas reduce malformed calls and validation failures.

**Q32.** A schema defines status as a free-text string, but only 4 valid values actually exist (pending, shipped, delivered, cancelled). What's the fix? 

A) Leave it as a free string 

B) Remove the field entirely 

C) Use an enum constraining status to those 4 exact values, so Claude can't pass an invalid one 

D) Make it a boolean

Answer: C.

**Q33.** Why mark fields as required vs optional explicitly in a tool schema? 

A) It has no functional effect 

B) It tells Claude precisely which inputs must always be provided vs. which can be omitted, reducing malformed calls 

C) All fields should always be optional 

D) MCP ignores the required field

Answer: B.

**Q34.** A tool schema has 25 required parameters for a single call. What design problem does this likely cause? 

A) High cognitive load / error rate — Claude is more likely to omit or mis-fill parameters; consider breaking into multiple simpler tools or reducing required fields 

B) None, more parameters means more precision 

C) MCP has no parameter limit so it's fine 

D) It reduces the chance of tool-selection errors

Answer: A.

## 14. Integrating MCP into Claude Code / Agent Workflows

Connecting MCP servers into an actual Claude Code project or agent system — configuring which servers are available, at what scope (project vs. user level), and how their tools combine with built-in tools during real workflows.

**Q35.** A company wants an MCP server (e.g., Jira integration) available to everyone on a project, checked into version control, vs. a developer's personal Slack MCP server only for themselves. What's the right configuration split? 

A) Both should be user-level only 

B) Project-level config (e.g. .mcp.json checked into the repo) for the shared Jira server; user/personal-level config for the individual's Slack server 

C) Both should be project-level 

D) MCP doesn't support per-project configuration

Answer: B — matches the project-level vs. user-level MCP config split.

**Q36.** Why scope some MCP servers at the project level rather than always at the user level? 

A) Project-level is always slower 

B) So the whole team automatically gets consistent, shared tool access tied to that specific project/repo, without each person configuring it manually 

C) User-level configs are deprecated 

D) It has no practical benefit

Answer: B.

# SCENARIO QUESTIONS (mixed topics, exam-realistic)

**Q37.** An MCP server for a payments system lets any authenticated client call issue_refund with no scoping. A support agent using this server can now refund any amount to any account. What are the TWO design flaws? 

A) Bad tool naming; missing examples 

B) Missing scoped permissions (e.g., refund limits/approval) and inadequate authentication/authorization boundaries 

C) Wrong transport choice 

D) Missing enum in schema

Answer: B. 

**Q38.** A tool process_payment sometimes fails silently and returns null. Claude interprets this as success and tells the user their payment went through when it didn't. What domain-2 principle was violated? 

A) Structured error handling — failures must be clearly signaled, not returned as ambiguous/null success-like responses 

B) Tool distribution 

C) Transport selection 

D) Tool choice configuration

Answer: A.

**Q39.** A team builds 15 separate near-duplicate tools (get_user_v1, get_user_v2, fetch_user, user_lookup...) accumulated over time. What Domain 1 anti-pattern does this create, and what Domain 2 fix addresses it? 

A) Anti-pattern: same-session self-review. Fix: hooks 

B) Anti-pattern: tool sprawl. Fix: consolidate/redesign tool boundaries and descriptions so each tool has one clear, non-overlapping purpose 

C) Anti-pattern: natural-language termination. Fix: stop_reason 

D) No anti-pattern present

Answer: B — ties Domain 1's tool sprawl anti-pattern directly to Domain 2's tool design fix.

**Q40.** You're designing an MCP server for a healthcare records system used by multiple hospitals remotely. Which combination of choices is most appropriate? 

A) stdio transport, no authentication, single shared tool with 30 parameters 

B) Remote (SSE/HTTP) transport, per-user OAuth-based authentication, scoped permissions per hospital/role, and well-defined schemas with enums for constrained fields 

C) stdio transport, shared static API key, unscoped access 

D) No MCP server needed, use built-in tools only

Answer: B — remote + multi-tenant + sensitive data demands network transport, real auth, and scoping.

**Q41.** A search_flights tool's description says only "searches flights." Claude keeps calling it with malformed date ranges and gets confused about round-trip vs one-way. What are the missing elements? 

A) MCP transport configuration 

B) Authentication pattern 

C) Tool distribution across agents

D) Clear input format specification, examples, and edge-case handling in the schema/description 

Answer: D.

# QUICK REFERENCE TABLE


| Concept | One-line definition |
| --- | --- |
| Tool description | Plain-English explanation of what a tool does and when to use it |
| Tool boundaries | What a tool is/isn't for, to avoid overlap with other tools |
| Structured error | Machine-readable failure response with code/message/retryable flag |
| Tool distribution | Deciding which tools go to which agent/subagent |
| tool_choice | API setting: auto / any / specific tool / none |
| MCP Host | The application the user uses (e.g. Claude Code) |
| MCP Client | Lives in host; 1:1 connection to a server |
| MCP Server | Exposes tools/resources/prompts to a client |
| Resource (MCP) | Read-only data exposed by a server |
| stdio transport | Local subprocess communication; simple, single-machine |
| SSE/HTTP transport | Remote/networked; supports shared, multi-client access |
| Scoped permissions | Restricting what actions/data a tool or agent can touch |
| Tool schema | Structured input definition (types, required fields, enums) |
| Project-level MCP config | Shared team config (e.g. .mcp.json in repo) |
| User-level MCP config | Personal config, not shared with the team |


Referring to these questions just gives you an idea how the exam looks like, and can vary. Share if you have any answers or questions not correctly placed or explained.