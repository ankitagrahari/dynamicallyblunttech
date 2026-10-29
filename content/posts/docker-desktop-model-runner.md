---
title: "Docker Desktop Model Runner"
date: 2026-10-27T08:14:18+05:30
draft: false
featureImage: "images/df024c_01c95619b9114c40930c5673d29a2457.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In today's rapidly evolving tech landscape, the availability of diverse AI models for everyday users marks a significant shift in how we interact with technology. However, with this convenience comes a critical responsibility: *ensuring data privacy remains intact*. Enter Docker Desktop, a powerful tool that revolutionised application deployment by packaging large applications as lightweight images, which can be executed in isolated environments called containers.

One of the standout features of Docker Desktop is the **Docker Model Runner**. This innovative addition empowers developers to run AI models locally on their machines. By leveraging this feature, users can harness the capabilities of advanced AI without the need to share sensitive data or manage complex API keys. With Docker Model Runner, you can focus on development and experimentation while maintaining control over your data privacy.

In this blog post, we will explore how Docker Model Runner works, its benefits, and how it can enhance your AI development experience while safeguarding your data.

### **Docker Model Runner**

These are some important points about Docker Model Runner plugin:
* Available as Beta from v4.40 of Docker Desktop on Macbooks with Apple Silicon or Windows with Nvidia GPUs
* No Cost constraints.
* Useful for running, managing, and interacting with AI models directly from the command line.
* Models are pulled from Docker hub for first time which can take some time based on the size of the models, loads into memory only at runtime when a request is made, and unloaded when not in use. After the first time, these models are cached locally for faster access.
* You can use below OpenAI compatible APIs to interact with these models.

```java
# Docker Model management
    POST /models/create
    GET /models
    GET /models/{namespace}/{name}
    DELETE /models/{namespace}/{name}

    # OpenAI endpoints
    GET /engines/llama.cpp/v1/models
    GET /engines/llama.cpp/v1/models/{namespace}/{name}
    POST /engines/llama.cpp/v1/chat/completions
    POST /engines/llama.cpp/v1/completions
    POST /engines/llama.cpp/v1/embeddings

    Note: You can also omit llama.cpp.
    E.g., POST /engines/v1/chat/completions.
```

Note: You can also remove llama.cpp from the endpoint

e.g: GET /engines/v1/models/{namespace}/{name}

### **Enabling Docker Model Runner**

After enabling it, you will have to Apply and Restart.

Be mindful of the model you are trying to pull and run. Since Docker desktop caches these models, it will effect the performance of your system, if the model is huge. It was advisable to have a small effective model to use. We are going to run Google Gemma 3. 

To view all the available commands with Docker model runner, you can run 

```java
docker model help
```

Here we are pulling Google Gemma 3. 

When we run the model, it will run an interactive chat session like below:

This will help a lot of developers in learning and growing with AI models. I will be using this in developing application which will interact with AI models without running the Ollama server as we did in the previous post [https://www.dynamicallyblunttech.com/post/spring-ai-with-ollama](https://www.dynamicallyblunttech.com/post/spring-ai-with-ollama). 

Reference:

-[https://docs.docker.com/model-runner/](https://docs.docker.com/model-runner/)