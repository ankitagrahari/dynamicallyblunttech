---
title: "Building the Foundation: APIs, Prompts, and First Runs"
date: 2026-10-27T08:14:21+05:30
draft: false
featureImage: "images/df024c_2190cdd1a6a2492481ba54e64560921e.jpg"
tags: ['[]']
categories: ['["681676055d80aaac0c9329be"]']
showReadingTime: true
---

In [Part 1](https://www.dynamicallyblunttech.com/post/meet-smart-devops-assistant-vision-stack-and-journey-so-far) of this series, we introduced the **Smart DevOps Assistant (SDA)** — an AI-powered helper that reviews pull requests, generates tests, and writes scrum updates.

Now it’s time to get our hands dirty. In this post, we’ll:
* Scaffold core APIs (/generate-summary, /analyze-pr)
* Wire up our first **prompt templates**
* Connect Spring AI to an LLM
* Run our very first **end-to-end test**

By the end, you’ll have a working backend service that can summarize PRs and hint at improvements. 🚀

## **Step 1 — Project Setup**

Our stack stays the same: **Java 21, Spring Boot 3.x, Spring AI, ChromaDB**.

Add the related dependencies required for Spring AI starter (check [spring.io](http://spring.io)[ docs](https://docs.spring.io/spring-ai/reference/) for the latest):

```java
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-advisors-vector-store</artifactId>
</dependency>

<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-starter-model-ollama</artifactId>
</dependency>
```

We’ll also add the Chroma dependency (not used fully yet, but needed later for context injection):

```java
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-starter-vector-store-chroma</artifactId>
</dependency>
```

Application config (application.yml):

```java
# Ollama - Chat
spring.ai.ollama.base-url=http://localhost:11434
spring.ai.ollama.chat.options.model=llama3.2
spring.ai.ollama.chat.options.temperature=0.7

## Ollama - Embeddings
spring.ai.ollama.embedding.options.model=hf.co/mixedbread-ai/mxbai-embed-large-v1
spring.ai.ollama.embedding.base-url=http://localhost:11434
spring.ai.ollama.init.pull-model-strategy=when_missing
```

If you are using OpenAI, then use the following 

```java
# OpenAI
spring.ai.openai.api-key=YOUR_OPENAI_API_KEY
spring.ai.openai.base-url=http://localhost:12434/engines
spring.ai.openai.chat.options.model=ai/gemma3
```

Configuration related to the chromaDB vector store

```java
# Chroma Vector Store connection properties
spring.ai.vectorstore.chroma.client.host=http://localhost
spring.ai.vectorstore.chroma.client.port=8000

# Chroma Vector Store collection properties
spring.ai.vectorstore.chroma.initialize-schema=true
spring.ai.vectorstore.chroma.collection-name=prCollection
```

## **Step 2 — Define Core APIs**

We’ll have following endpoints:
* POST /ai/pr-summary → short overview of a PR
* POST /ai/pr-analyze → deeper review with suggestions
* POST /ai/vectorstore → store changed files in a PR to vector store.

```java
@RestController
@RequestMapping("/ai")
public class  AIController {

    private final AIService aiService;
    private final SDAVectorStoreService sdaVectorStoreService;

    public AIController(
			AIService aiService,
            SDAVectorStoreService sdaVectorStoreService) {
        this.aiService = aiService;
        this.sdaVectorStoreService = sdaVectorStoreService;
    }

    @PostMapping("/pr-summary")
    public ResponseEntity<PRSummaryResponse> generateSummary(
			@RequestBody PRSummaryRequest prSummaryRequest){
        return aiService.generateSummary(
			prSummaryRequest);
    }

    @PostMapping("/pr-analyze")
    public PRSuggestionResponse analyzePR(
			@RequestBody AnalyzePRRequest request){
        return aiService.analyzePR(
			request.prDiff(), 
			request.fileNames());
    }

    @PostMapping("/vectorstore")
    public void storeDataToVectorStore(
			@RequestBody List<GitChangedFile> gitChangedFileList){
        sdaVectorStoreService.populateVectorStore(
				gitChangedFileList);
    }
}
```

This keeps things API-first, and our endpoints are defined here. 

## **Step 3 — Prompt Templates**

Spring AI’s PromptTemplate lets us define reusable, dynamic prompts.

```java
PromptTemplate summaryTemplate = new PromptTemplate("""
    You are a senior software reviewer.
    Summarize the following PR in 2-3 sentences.
    Highlight potential risks if visible.
    PR Title: {title}
    PR Description: {description}
    PR Diff: {diff}
""");
```

We can now inject title, description, and diff dynamically.

For analysis:

```java
PromptTemplate analyzeTemplate = new PromptTemplate("""
    You are a senior software engineer.
    Given this PR diff: {diff}, 
    provide:
    1. A short summary
    2. Suggestions for improvements
    3. Risks to watch for
    Respond in JSON:
    {
      "summary": "...",
      "suggestions": ["..."],
      "risks": ["..."]
    }
""");
```

## **Step 4 — Connect with the LLM**

Spring AI makes this easy using ChatClient.

```java
public PRSummaryResponse generateAISummary(
		PRSummaryRequest prSummaryRequest){

   PromptTemplate summaryTemplate = new PromptTemplate("""
           You are a senior software reviewer.
               Summarize the following PR in 2-3 sentences.
               Highlight potential risks if visible.
               PR Title: {title}
               PR Description: {description}
               PR Diff: {diff}
           """)
   return chatClient
           .prompt(summaryTemplate.create(Map.of(
                  "title", prSummaryRequest.getTitle(),
                  "description", prSummaryRequest.getDescription(),
                  "diff", prSummaryRequest.getDiff())))
              .call()
              .entity(PRSummaryResponse.class);
}
```

Notice how the response is mapped into a DTO (PRSummaryResponse) — no parsing headaches and dynamic substitution in the prompt.

## **Step 5 — A Taste of Context Injection**

```java
public PRSuggestionResponse analyzePR(String prDiff, List<String> fileNames){
        PromptTemplate analyzePRTemplate = new PromptTemplate("""
                You are a senior software engineer.
                    Given this PR diff: {diff},
                    provide:
                    1. A short summary
                    2. Suggestions for improvements
                    3. Risks to watch for
                    Respond in JSON:
                    {
                      "summary": "...",
                      "suggestions": ["..."],
                      "risks": ["..."]
                    }
                """)

        String files = String.join("','", fileNames);
        //This query will list down the file content from vector db, and inject it with the prompt to provide context-aware suggestion
        QuestionAnswerAdvisor qaAdvisor = QuestionAnswerAdvisor
			.builder(vectorStore)
			.searchRequest(SearchRequest.builder()
                .similarityThreshold(SIMILARITY_THRESHOLD)
                .filterExpression("path in ['"+ String.join("','", fileNames) + "']")
                .topK(5)
                .build())
             .build();

        PRSuggestionResponse response = chatClient
            .prompt(analyzePRTemplate.create(
                     Map.of("diff", prDiff)))
                .advisors(qaAdvisor)
                .call()
                .entity(PRSuggestionResponse.class);

        logger.debug("Response:{}", response);
        return response;
}
```

This ensures only **relevant code snippets** (like [UserService.java](http://UserService.java)) are injected into the model’s context.

The Spring AI framework creates an ChatClientRequest from user’s Prompt along with an empty advisor context object.

Each advisor in the chain processes the request, potentially modifying it. Alternatively, it can choose to block the request by not making the call to invoke the next entity. In the latter case, the advisor is responsible for filling out the response.

The final advisor, provided by the framework, sends the request to the Chat Model.

The Chat Model’s response is then passed back through the advisor chain and converted into ChatClientResponse. Later includes the shared advisor context instance.

Each advisor can process or modify the response.

The final ChatClientResponse is returned to the client by extracting the ChatCompletion.

*source: *[*https://docs.spring.io/spring-ai/reference/api/advisors.html*](https://docs.spring.io/spring-ai/reference/api/advisors.html)* *

QuestionAnswerAdvisor provides capabilities to utilize a vector store to answer the queries implementing Retrieval Augment Generation (RAG) pattern. 	

## **Step 6 — First End-to-End Run**

Example request to /generate-summary:

```java
{
  "title": "Add new API generate-summary",
  "description": "Adding new API to get PR summary connecting to LLM .",
  "pr_Url": "https://github.com/ankitagrahari/smart-devops-assistant/pull/3"
}
```

Example response:

```java
{
"summary": "This PR (#3) adds a new API `/generate-summary` to the Smart DevOps Assistant. It introduces DTOs (PRSummaryRequest/Response), a new GitService to fetch diffs via GitHub API, and extends AIService to generate PR summaries. The controller and webhook service are updated to orchestrate diff fetching and AI calls. Documentation is updated and test utilities are added.",
"risk": [
    "GitHub PAT may expose security risks if not scoped minimally",
	"Large PR diffs may exceed AI token/prompt limits, causing failures",
	"Blocking synchronous RestTemplate calls may slow webhook responses",
	"Error handling is inconsistent (null returns, generic 404s/500s)",
	"Appending .diff to PR URLs may break for enterprise/custom GitHub setups",
	"Lack of tests for the new /generate-summary endpoint and service logic",
	"AI outputs may hallucinate or generate inaccurate summaries"
],
}
```

Boom 💥 — your assistant just summarized your PR.

## **Step 7 — Gotchas**
* **Dependency drift**: Spring AI evolves quickly — check docs for version bumps.
* **Prompt drift**: Always enforce strict JSON output when expecting structured data.
* **Response failures**: Add logging to catch when the model doesn’t respect schema.

## **Step 8 — What’s Next**

Now that we have a working API + prompt flow, in **Blog 3** we’ll:
* Embed our repo into ChromaDB
* Chunk & index code/docs
* Run **true RAG queries** for context-rich reviews

That’s where SDA starts feeling *intelligent*, not just chatty.

Do share your thoughts about any improvements. 

Github repo: [https://github.com/ankitagrahari/smart-devops-assistant](https://github.com/ankitagrahari/smart-devops-assistant/pull/3/files)