---
title: "Built a Webhook Inspector from Scratch and Shipped It — Here's Everything That Went Wrong"
date: 2026-10-27T08:14:26+05:30
draft: false
featureImage: "images/df024c_ee14681cc40a493eac97f60765582adff000.jpg"
tags: ['[]']
categories: ['["6249579158f0bd10b2a57273"', '"69928c20ed328546cacbfdd1"]']
showReadingTime: true
---

> **Live at:** [https://hookspy.in](https://hookspy.in)HookSpy - Walk Through

Every developer integrating Stripe, Razorpay, or GitHub has been there. You set up a webhook, fire a test event, and... nothing. The endpoint didn't respond. Or it did but your handler crashed silently. Or you just want to see the exact payload the service sends before writing a single line of handler code.

Tools like *RequestBin* and *Webhook.site* exist. But I wanted to build my own — one I understood end to end, could deploy myself, and could use as a real product to learn distributed systems in practice. That's ***HookSpy***.

This is the full story — architecture decisions, a painful Vaadin mistake, 18 production bugs, and what I'd do differently.

## **What HookSpy Does**

You register, get a unique webhook URL like [*https://hookspy.in/h/{slug}*](https://hookspy.in/h/{slug}), and point any service at it. Every incoming request appears in your dashboard in real time. You can inspect headers, body, query params — replay the request to any target URL — and export it as a ready-to-run cURL command.

Three tiers: 
* ***Free*** (1 endpoint, 100 requests/day),
* ***Pro*** (₹299/month, 10 endpoints, 30-day retention),
* ***Team*** (₹799/month, 50 endpoints, 90-day retention).

## **The Architecture**

Three Spring Boot microservices connected via Kafka.

```java
External Service (Stripe, Razorpay etc.)
        │
        │  POST https://hookspy.in/h/{slug}
        ▼
┌─────────────────────────────────────┐
│  capture-service :8080              │
│  Spring Boot WebFlux + Kafka Binder │
│  Returns 200 immediately            │
│  Publishes to Kafka topic           │
└─────────────────────────────────────┘
        │ Kafka KRaft (no Zookeeper)
        ▼
┌─────────────────────────────────────┐
│  processor-service :8081            │
│  @KafkaListener                     │
│  Validates tier limits              │
│  Saves to PostgreSQL                │
│  RetryableTopic (3 retries + DLT)   │
└─────────────────────────────────────┘
        │ PostgreSQL 16
        ▼
┌─────────────────────────────────────┐
│  ui-service :8082                   │
│  Spring Boot REST + React 18        │
│  SSE live updates                   │
│  Auth, replay, Razorpay payments    │
└─────────────────────────────────────┘
```

#### **Why three services?**

The most critical constraint: Stripe and Razorpay expect a 200 response within 5 seconds. If processing is slow, they retry — duplicate events. capture-service returns 200 immediately and hands off to Kafka. The caller never waits.

**Why Kafka and not write directly to DB?**

I wanted to learn Kafka in a real context. But it's also architecturally sound — capture can scale independently from the processor. Flash sale burst of webhooks? Kafka absorbs the spike. The processor works through the backlog at its own pace.

**Kafka KRaft — no Zookeeper**

Kafka's KRaft mode removes the Zookeeper dependency entirely. One less service, one less thing to fail. The docker-compose setup is clean:

```java
kafka:
  image: confluentinc/cp-kafka:7.7.0
  environment:
    KAFKA_NODE_ID: 1
    KAFKA_PROCESS_ROLES: broker,controller
    KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
```

**Two different Kafka client styles — intentionally**
* *capture-service* uses Spring Cloud Stream Kafka Binder — a reactive *Supplier<Flux<WebhookEventDto>>* backed by *Sinks.Many*. The Binder wires it to the topic automatically.
* *processor-service* uses Spring Kafka directly — *@KafkaListener* with manual acknowledgement and *@RetryableTopic* for fine-grained reliability. Three retries with exponential backoff, then dead letter topic.

Mixing both taught me where each approach shines — Binder for reactive fire-and-forget producers, plain Spring Kafka for consumers that need reliability control.

## **The Vaadin Mistake**

I vibe coded the UI in Vaadin 24 first. Java all the way down, no context switching, built-in push support for live updates. Seemed reasonable.

> It was a mistake.
* Vaadin's shadow DOM makes CSS control nearly impossible.
* Every rule needs !important.
* Dark mode is unreliable.
* Heavy JS bundle.
* The UI fought the framework constantly.

After shipping the backend, I ripped out Vaadin entirely and rebuilt in React 18 + Vite + TailwindCSS. The frontend is a separate Vite project that builds into *ui-service/src/main/resources/static/*. Spring Boot serves React at / and the REST API at /api/*. One process in production, clean separation in development.

The migration took a week. The backend didn't change at all — same entities, same services, same Kafka pipeline. Only ui-service changed.

> **Lesson:** For any developer-facing product with design ambition, Vaadin will fight you the whole way. Start with React.

## **SSE Instead of Polling**

The Vaadin UI polled the database every 3 seconds. The React version uses Server-Sent Events.

The SSE endpoint holds a long-lived connection per slug. When processor-service saves a new webhook, a second Kafka consumer in ui-service receives the same event and pushes it to all open SSE emitters for that slug. New requests appear instantly.

```java
@GetMapping(value = "/endpoints/{slug}/requests/stream",
            produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public SseEmitter stream(@PathVariable String slug) {
    var emitter = new SseEmitter(Long.MAX_VALUE);
    emitterRegistry.register(slug, emitter);

    // Send a keep-alive comment every 15s — prevents idle disconnect
    ScheduledFuture<?> ping = scheduler.scheduleAtFixedRate(() -> {
        try {
            emitter.send(SseEmitter.event().comment("ping"));
        } catch (IOException e) {
            emitter.completeWithError(e);
        }
    }, Instant.now(), Duration.ofSeconds(15));

    emitter.onCompletion(() -> {
        emitterRegistry.remove(slug, emitter);
        ping.cancel(true);
    });
    emitter.onTimeout(() -> {
        emitterRegistry.remove(slug, emitter);
        ping.cancel(true);
    });
    emitter.onError((e) -> {
        emitterRegistry.remove(slug, emitter);
        ping.cancel(true);
    });

    return emitter;
}
```

On the React side:

```java
useEffect(() => {
    const source = new EventSource(
        `/api/endpoints/${slug}/requests/stream`,
        { withCredentials: true }
    )
    source.onmessage = (e) => {
        const newReq = JSON.parse(e.data)
        queryClient.setQueryData(['requests', slug], (old = []) => [newReq, ...old])
    }
    return () => source.close()
}, [slug])
```

**SSE is underrated for developer tools.** Simpler than WebSockets, perfect for one-directional live data. The only gotcha is nginx buffering — solved with proxy_buffering off.

## **18 Bugs That Cost Me Time**

### **1. CSRF Blocking Every POST Request**

Every POST to /api/** returned 403. 

No logs, no error. Spring Security's default CSRF protection. One line fix:

```java
.csrf(csrf -> csrf.ignoringRequestMatchers("/api/**"))
```

### **2. SSE Leaking Content-Type Into Exception Handler**

The SSE endpoint produces text/event-stream. Spring MVC cached this and applied it to error handler responses. GlobalExceptionHandler crashed with HttpMessageNotWritableException: No converter for ApiError with preset Content-Type 'text/event-stream'.

**Fix:** write directly to HttpServletResponse, skip SSE requests entirely. Move SSE to its own controller class so the produces type doesn't leak.

### **3. Vite Proxy Hanging on SSE**

Socket hang up errors on the SSE stream. 

Vite's HTTP proxy buffers responses — SSE frames were never flushed. 

**Fix:** separate proxy rule for SSE endpoints with x-accel-buffering: no header, plus spring.mvc.async.request-timeout: -1 in application.yml.

### **4. Razorpay Authentication Failed — Three Causes, Same Error**

This one took the longest. Curl worked, SDK didn't.
* Cause 1: *RazorpayClient* instantiated at bean creation time before @Value injected. 
**Fix:** constructor parameters.
* Cause 2: *application.yml* had *${RAZORPAY_KEY_ID:placeholder}* — the default value was overriding the actual env var. 
**Fix:** remove all defaults for production secrets.
* Cause 3: Invisible trailing whitespace in copy-pasted keys. 
**Fix:** .trim() on both values.

### **5. Razorpay JS SDK Undefined**

*<script>* tags inside React JSX don't execute. *window.Razorpay* was always undefined. 

**Fix:** load in index.html before React mounts.

### **6. Razorpay Order Response Shape Wrong**

Order created successfully but *"could not initiate payment"*. Backend was returning the raw Razorpay Order object — Jackson serialised it as the full Razorpay payload. 

Frontend expected *{ orderId, keyId }* but got *{ id, amount, currency, ... }*. 

**Fix:** explicit Map.of("orderId", ..., "keyId", ...) in the controller.

### **7. @Value Null in Component**

*captureBaseUrl* was null. The mapper was being instantiated with new *MapperFromEntityToDTO()* — Spring never touched it. @Value only works on Spring-managed beans. Always inject via constructor.

### **8. Tier Lowercase Mismatch**

Upgrade button not showing for FREE users. Backend returned "free", frontend compared against "TEAM". 

**Fix:** *user?.tier?.toUpperCase()* everywhere.

### **9. Docker Services Connecting to localhost**

Inside a Docker network, services must use container service names, not localhost. application.yml had hardcoded localhost for DB and Kafka. 

**Fix:** environment variable overrides in [docker-compose.prod](http://docker-compose.prod).yml:

```java
SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/${DB_NAME}
SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka:9092
```

### **10. Razorpay Env Vars Not Reaching Container**

Could not resolve placeholder '*RAZORPAY_KEY_ID*'. 

Docker Compose environment: does variable substitution at compose level but doesn't inject into the container. 

**Fix:** add *env_file: - .env* to every service that needs secrets.

### **11. nginx Certificate Not Found**

nginx crash-looping. [docker-compose.prod](http://docker-compose.prod).yml had ./nginx/certs as cert path — certs were at /etc/letsencrypt. 

**Fix:** mount the actual letsencrypt directory:

```java
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

### **12. Wrong JAR Running in Container**

*ui-service* logs showed Started *CaptureServiceApplication*. 

Dockerfile used COPY target/*.jar app.jar — wildcard picked up the wrong JAR. 

**Fix:** specific artifact name in each Dockerfile:

```java
COPY target/ui-service-*.jar app.jar
```

### **13. Maven Not Found**

mvn: command not found. 

IntelliJ uses a bundled Maven — system terminal doesn't have it. 

**Fix:** brew install maven.

### **14. Maven Compiler Plugin 3.14.1 Bug With Java 21 + Lombok**

*ExceptionInInitializerError: TypeTag :: UNKNOWN*. Known bug. 

**Fix:** pin to 3.13.0, upgrade Lombok to 1.18.34.

### **15. SCP Copying node_modules**

File transfer taking 20+ minutes. scp -r copies everything. 

**Fix:** use rsync with excludes:

```java
rsync -av --exclude='node_modules' --exclude='target' --exclude='.git' ...
```

### **16. Docker Images Not Found on Server**

*hookspy/ui-service* image not found. [docker-compose.prod](http://docker-compose.prod).yml used image: references — images were never pushed to a registry. 

**Fix:** switch to build: with context pointing to each service directory.

### **17. AuthenticatedUser Broke After Vaadin Removed**

AuthenticationContext not found after removing Vaadin. 

**Fix:** rewrite to use SecurityContextHolder:

```java
var auth = SecurityContextHolder.getContext().getAuthentication();
```

### **18. Registration Failing in Browser, Working via curl**

No backend errors. Browser was serving a cached old JS bundle. Hard refresh (Cmd+Shift+R) resolved it. 

Production deployment lesson: always hard refresh after deploying new frontend.

## **Production Stack**


| Layer | Technology |
| --- | --- |
| Language | Java 21 |
| Framework | Spring Boot 4.0.5 |
| Reactive producer | Spring Cloud Stream Kafka Binder |
| Reliable consumer | Spring Kafka + @RetryableTopic |
| Message broker | Kafka KRaft (no Zookeeper) |
| Database | PostgreSQL 16 + Flyway |
| ORM | Spring Data JPA |
| Auth | Spring Security + BCrypt + HTTP Sessions |
| Frontend | React 18 + Vite + TailwindCSS |
| Live updates | Server-Sent Events (SSE) |
| Payments | Razorpay (HMAC-SHA256 verification) |
| Reverse proxy | nginx |
| Hosting | Hetzner CX23, Helsinki (~₹465/month) |
| SSL | Let's Encrypt (auto-renewing) |


## **What I'd Do Differently**

**Start with React.** The Vaadin migration week was completely avoidable.

**Use a proper internal event bus.** ui-service has a second Kafka consumer just for SSE notifications. That's processor-service's concern leaking into ui-service. Better design: Spring ApplicationEvent for internal communication, Kafka as transport only.

**One service, one responsibility — strictly.** When a service grows a second Kafka consumer for a UI concern, that's a smell worth stopping.

**Remove YAML default values for all secrets.** ${SECRET:default} seems safe but the default silently wins when the env var isn't loaded. Fail fast on missing secrets instead.

## **Try It**

> HookSpy is live at [https://hookspy.in](https://hookspy.in) — free tier, free forever.

Follow along at [@backendbrilliance](https://www.instagram.com/backendbrilliance).

Technical blog: [dynamicallyblunttech.com](http://dynamicallyblunttech.com)