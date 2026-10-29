---
title: "Chatbot using Spring AI and OpenAI"
date: 2026-10-27T08:14:16+05:30
draft: false
featureImage: "images/df024c_c62e7dc6cc2040be9ac8ce6da1991841.jpg"
tags: ['[]']
categories: ['["681676055d80aaac0c9329be"]']
showReadingTime: true
---

In the previous post about utilizing Spring AI with Ollama and employing Docker Model Runner to execute AI models locally, this post will expand on that by developing a chatbot. This chatbot will retain interaction data in memory, facilitating more meaningful communication.

In this post, we will use the Docker Model Runner to run Google's Gemma AI model in our local machine with OpenAI, and create a spring boot AI chat application which will generate responses based on the previous context. 

Let's first setup our Docker, and run the Google AI model gemma in our local. 

### **Running AI model Gemma locally**

So, first step will be to open terminal and run command

```java
docker model list
```

which will list down existing AI model present in your local. We have already downloaded and ran ai/gemma3 in the last post. Here, we will only look into the connection parameters that will be required in the spring boot project. 

When we enabled the docker model runner, there is a enable host-side TCP support check-box, which enabled the TCP port, using which we will connect to the already running AI model. 

So, we will be using this port, and the base-url for the open-ai parameter will be [http://localhost:12434/engines](http://localhost:12434/engines)

### **Setup Spring AI Project**

Lets navigate to [start.spring.io](http://start.spring.io) to initialise a spring boot project which will have OpenAI and Spring Web as the dependencies.

We will have the following [application.properties](http://application.properties) file. 

```java
spring.application.name=chatbot

spring.ai.openai.base-url=http://localhost:12434/engines
spring.ai.openai.chat.options.model=ai/gemma3
spring.ai.openai.api-key=test

# Docker Model Runner doesn't support embeddings, so we need to disable them.
spring.ai.openai.embedding.enabled=false
```

***NOTE:*** The api-key is given as test, and not a specific API key. This is only possible when you have the AI model running locally, else it is mandatory to create an API key from OpenAI. 

### **Creating Chat Client Configuration**

We need to create ChatClient object to communicate to any AI model in Spring AI. In the previous post we have created a ChatClient object which took a default system prompt, that was configurable. This time, when we are trying to store the chat history in memory, we will be using Advisors. 

Advisor is a powerful tool which helps in intercepting and modifying the AI request and response. It also helps in adding more context to the interaction, by adding functionalities like logging, memory management, data transformation without changing applications core logic. 

Types of Spring AI Advisors:
* Call Around Advisors
* Chat Memory Advisors,
* Retrievers Advisors
* Logging Advisors

So, in order to create a Chat memory advisor for our project, we will use the ChatClient builder to set the default advisor for our application.

```java
@Autowired
ChatMemory chatMemory;

@Bean
ChatClient client(ChatClient.Builder builder){
    return builder.defaultAdvisors(
           MessageChatMemoryAdvisor.builder(chatMemory).build())
           .build();
}
```

With the new upgrade from Spring, *InMemoryChatMemory* was deprecated, and now Spring auto-configures *ChatMemory* bean when any AI model starters is used. By default it comes with *MessageWindowChatMemory* implementation which stores the conversation history in memory based on the default window maximum size. To manage the conversational history, the storage mechanism is decoupled from *ChatMemory* interface, and is now handled by *ChatMemoryRepository* interface. 

After creating the ChatClient bean, we can use it by auto-wiring it or by constructor injection in our Controller, where we will create a Get API, that will send the AI model with the message coming as request param. 

Lets try to test this application, where we will ask the AI model with two separate GET request,  which is supposed to be stateless, but in our use case the AI model, will be having a history of the conversation, therefore will be able to answer the next question. AI communication which remembers my name!

This can be extended to a nicer UI which will be much easier to work with, instead of sending multiple API request. Also, this is a very simple usage of how we can create a chat bot, which can have the context of the conversation history. 

### **References**
* [https://docs.spring.io/spring-ai/reference/1.0/upgrade-notes.html](https://docs.spring.io/spring-ai/reference/1.0/upgrade-notes.html)
* [https://docs.spring.io/spring-ai/reference/api/advisors.html](https://docs.spring.io/spring-ai/reference/api/advisors.html)
* [https://docs.spring.io/spring-ai/reference/api/chat/dmr-chat.html](https://docs.spring.io/spring-ai/reference/api/chat/dmr-chat.html)

The project is added to my [Github repo](https://github.com/ankitagrahari/chatbot-ai), if you want to explore more. Hoping this will be helpful in learning Spring AI and using different AI models. Please comment down your thoughts or suggestions to improve.