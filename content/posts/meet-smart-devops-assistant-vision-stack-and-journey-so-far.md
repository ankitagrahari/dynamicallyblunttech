---
title: "Meet Smart Devops Assistant: Vision, Stack and Journey so far"
date: 2026-10-27T08:14:14+05:30
draft: false
featureImage: "images/df024c_3d9beee05bb34ba18a65da736358c037.jpg"
tags: ['[]']
categories: ['["6249579158f0bd10b2a57273"', '"681676055d80aaac0c9329be"]']
showReadingTime: true
---

> *PRs that review themselves. Tests that write themselves. Stand-ups that summarise themselves.*

Say hello to **Smart DevOps Assistant (SDA)** — an AI-augmented helper that plugs into your developer workflow and reduces review/summary/test friction to near-zero.

## **Why this project exists (and who it’s for)**

Modern teams drown in pull requests, context switching, and “Did we test that?” moments. SDA is for engineers who want:
* **Signal over noise on PRs** — what changed, why it matters, risks, and ownership hints.
* **Safer, faster merges** — auto-suggested unit tests raise the quality floor.
* **Continuous team awareness** — crisp, Scrum-style updates distilled from commits and PRs.
* **Project-aware AI** — responses grounded in *your* codebase with retrieval-augmented generation (RAG), not generic advice.

## **What SDA does (core capabilities)**
* **PR Analyzer** → Summarizes changes, highlights hotspots, suggests improvements.
* **Test Generator** → Emits JUnit 5/Mockito test stubs tailored to the changed code.
* **Scrum Assistant** → Produces “yesterday / today / blockers” standup notes from PRs & commits.
* **Context-aware via RAG** → Indexes your repo/docs into a vector store, fetches the most relevant chunks for each prompt.

## **Architecture at a glance**
* **Backend:** Java 24, Spring Boot 3.x, **Spring AI** for model + embeddings integration.
* **Vector Store:** **ChromaDB** for semantic search over your code & docs (great for quick local iteration).
* **LLM:** OpenAI, Hugging Face (pluggable via Spring AI; you can swap providers later).
* **Integrations:** GitHub (PR metadata + unified .diff), optional Slack for notifications.
* **Agents:** Lightweight services (Code Reviewer, Test Generator, Scrum Assistant) orchestrated by a Spring service; parallelised with @Async + CompletableFuture for speed.

**High-level flow**

PR opened/updated → 

Fetch PR title/description/diff →

Retrieve relevant code/docs from vector store →

Run specialised agents (in parallel) →

Aggregate results → 

Post to Slack / expose via API.

## **Our build journey (the 5-part roadmap)**

**Phase 1 — Foundations**
* Spring Boot API endpoints:
* POST /analyze-pr (deep review)
* POST /generate-summary (short overview)
* A Java microservice talks to the LLM with clean, role-anchored prompts.
* Output is structured JSON so the UI/bots can consume it reliably.

**Phase 2 — Make it visible**
* Wire GitHub webhook / Action to trigger analysis on PR events.
* Post summaries/suggestions to Slack.

**Phase 3 — Make it smart with RAG**
* Chunk & embed code/docs → store in **Chroma** via Spring AI.
* On each PR: retrieve top-K relevant snippets and feed them into prompts alongside the diff.

**Phase 4 — Multi-agent brains**
* Agents for Review, TestGen, Scrum.
* **Parallel execution** with CompletableFuture and a simple orchestrator that aggregates outputs.

**Phase 5 — UX & Ops polish**
* Slack/Teams formatting, PR badges, audit logs, and quality-of-life prompts.

## **Tech Stack (and why we chose it)**
* **Spring AI** – Gives Spring-native abstractions (Boot starters, config props) to talk to LLMs and embedding models. If you’re a Spring dev, it feels like home.
* **ChromaDB** – Simple, fast local vector DB with good ecosystem support, perfect for repo-scale RAG experiments.
* **JUnit 5 + Mockito** – Test generation targets familiar Java tooling out of the box.
* **GitHub Webhooks/Actions** – Trigger analysis where the devs already live.

> Alternatives you can explore later: PGVector/MariaDB/Milvus vector stores, or running embeddings locally via Ollama. Spring AI plays nicely with multiple stores/providers.

## **Prompting strategy (how we keep it crisp and useful)**
* **Role-anchored prompts**: “Senior Reviewer,” “Senior Java Test Engineer,” “Scrum Assistant.”
* **Strict JSON outputs**: machine-readable, blog-ready, easy to diff in PR comments.
* **RAG-aware composition**: *“Given retrieved context + this diff, do X.”*
* **Guardrails**: explicit frameworks (JUnit/Mockito), concise tone, edge-case nudges.

## **How SDA works**

SDA depends on collections of microservices which interact with each other to provide summary or generate test case. All services are registered via Eureka (Service Discovery) and each request goes through Spring cloud Gateway (API Gateway).

There is a separate service for handling all operation with Github, e.g. 
* Finding PR metadata
* Finding the PR difference
* Fetching all changed files in a PR
* Fetching any file content in the project
* Share data with AI service

And then there is a service to interact with AI Agents. Based on the data it gets from the Git service, it will try to 
* Summary of the PR
* Analyses PR for any risk, suggestions and improvements
* APIs to manage data in ChromaDB Vector store.
* Have a counterpart with multiple agents like
* Code Reviewer Agent - which provide meaningful context based suggestion on the PR
* Test Generator Agent - which generates the Junit test cases based on the PR and project as the context.
* Scrum Assistant Agent - which will use the PR to provide SCRUM update on what was done yesterday, what is planned for today and tomorrow.

Dividing the project in phases facilitate in bringing the project from bottom to top, with ground work done in phase 1, and then integrating with AI agents and providing essential time for the project to evolve. Faced a lot of issues and sometimes need to backtrack to enhance the requirement. 

> This project is for learning purpose. Some parts may have some issues, which is getting fixed as you read through.

As part of Phase 1, the project has all the services interweaved in one single microservice. The Git Webhook is used to trigger a request to the application.
* So, if a PR is raised on the project, then the request from Git Webhook is redirected to the application,
* then SDA will picks up the required metadata from the Github and
* then it initialise the Vector store with the changed files coming from the PR.
* then it collects the PR difference and
* sends the data to AI agents with prompt to get suggestions/improvements on PR.

## **NGROK - Flexible API Gateway**

Since the application is not hosted on any domain, rather sits in my [localhost](http://localhost), we have to somehow redirect the request coming from Github Webhook to our application. Or it can be said that, the Github Webhook needs a URL or host to send the request. 

This is where the [https://ngrok.com/](https://ngrok.com/) application comes in to play. It launches its server which can accept the API request from Github Webhook, and redirects it to our application running on [localhost](http://localhost). 

So, lets say my application is running on port 8389, then we need to run 

```java
ngrok http http://localhost:8389
```

which will launch a server and provide URL that can be used with Github webhook. 

The URL as part of Forwarding can be used now in Github Webhook. 

In the Github, under the settings tab, go to Webhooks, click on Add Webhook, and fill out the details like Payload URL (in this case [https://aab4835964fe.ngrok-free.app](https://aab4835964fe.ngrok-free.app)) and Content Type (application/json). You can also enable SSL verification for more secure routing. 

Once enabled, it will send the POST request with the payload to SDA.

## **API /analyzepr**

SDA has and endpoint which will accept the POST request from the Github Webhook, and send the payload to 
* fetch the PR difference
* fetch the changed files name in the PR
* filter for Java files and skip the removed files in the PR
* fetch the entire file content and
* store in ChromaDb Vector Store

The file content will act as the context for the AI agent to analyse the PR and provide suggestions/improvements. 

Then the SDA prepares the prompt with the PR difference and injects the QuestionAnswerAdvisor of Spring AI to prevents model from generating a general PR summary, instead a more context aware response related to the files changed in the PR. And AI will generate a structure response like 

## **Gotchas we hit (so you don’t)**
* **Spring AI dependency names & properties evolve.** Prefer the latest docs and BOM; older guides might use milestone artifacts or different property names. Pin compatible versions and read the starter docs when integrating Chroma.
* **Vector store/API drift.** Ensure your Chroma server and client expectations match; upgrade pairs together.
* **Agents ≠ framework magic.** Spring AI doesn’t ship a multi-agent runtime; we implemented a lean orchestrator and parallelised with @Async + CompletableFuture.

## **What’s next in the series**
* **Part 2:** Scaffolding the APIs & clean prompts (with sample payloads).
* **Part 3:** RAG in Java — chunking, embedding, retrieval with Spring AI + Chroma.
* **Part 4:** Multi-agent coordination + parallel execution patterns.
* **Part 5:** CI hooks, Slack summaries, and real-world ops tips.

## **Try it / follow along**

Clone the repo, run the services, and start with POST /generate-summary on any PR (or paste a unified .diff). Then layer in RAG and multi-agent outputs as we progress through the series.

You can refer to the Github project here 

### **A final word**

SDA isn’t about replacing reviewers; it’s about giving them *superpowers*. Less time expanding diffs, more time debating design, correctness, and the “gotchas” that matter.

Do comment for any suggestions or topics you want to be addressed. Follow for more tech related content.

> *Learn with Every Commit*