---
title: "Building Production-Grade Apache Kafka Consumer Patterns"
date: 2026-10-27T08:14:15+05:30
draft: false
featureImage: "images/df024c_c2c2fee99fa24ba88276633124e8fcde.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"', '"6249579158f0bd10b2a57273"', '"69928c20ed328546cacbfdd1"', '"69a5166ca84159d4b5dd8ff1"]']
showReadingTime: true
---

**Part 2 of the StreamMetrics Series**

*Previous parts: *[*Part 1: Kafka Producer*](https://www.dynamicallyblunttech.com/post/building-a-production-kafka-producer)* | *[*Part 3: Real-time Aggregation *](https://www.dynamicallyblunttech.com/post/real-time-aggregations-with-kafka-streams-at-10k-events-sec)* | *[*Part 4: From *](https://www.dynamicallyblunttech.com/post/from-localhost-to-kubernetes-deploying-streammetrics-at-scale)[*Localhost*](http://Localhost)[* to Kubernetes*](https://www.dynamicallyblunttech.com/post/from-localhost-to-kubernetes-deploying-streammetrics-at-scale)

*A deep-dive into manual offset management, dead letter queues, and observability with Spring Boot + Apache Kafka. This is part 2 of the series Stream Metrics application. *In [Part 1](https://www.dynamicallyblunttech.com/post/building-a-production-kafka-producer) we built the producer, today we add the consumer.

#### **Why This Matters**

Most tutorials show you how to build a Kafka consumer. They show you @KafkaListener, they show you how to read a message, and they call it production-ready. It is not!

Production Kafka consumers need to answer hard questions: 
* What happens when your database is down and you can't process a message?
* What happens when a malformed event enters your topic?
* How do you know if your consumer is falling behind?
* How do you trace a message from producer to consumer?

This post answers all of those questions with code from StreamMetrics, a real-time analytics platform I built to process 10,000+ events per second from multiple microservices.

**Architecture Overview**

Before diving into code, here is the data flow StreamMetrics uses:

The consumer group has 3 threads, each owning 2 partitions from the 6-partition topic. This gives us parallelism while maintaining partition-level ordering guarantees.

## **1. Manual Offset Management: Why Auto-Commit Will Eventually Burn You**

Spring Kafka's default is *enable.auto.commit=true*, which commits offsets every 5 seconds regardless of whether your processing succeeded. This creates a silent data loss scenario that is extremely hard to debug in production.

**The Problem with Auto-Commit**

Consider this sequence of events with auto-commit enabled:
* Consumer polls 500 records from Kafka
* Auto-commit timer fires at 3rd second, commits offset for all 500 records
* At second 4, your database goes down, processing failed for records 301-500
* Consumer restarts - but offsets are already committed
* Records 301-500 are silently lost forever.


| *Auto-commit is optimistic. Manual offset management is pessimistic. For financial metrics, audit logs, or any data you cannot afford to lose, always use manual commits.* |
| --- |


#### **Configuration:**

```java
# application.yml
spring:
  kafka:
    consumer:
      enable-auto-commit: false         # Manual control
      auto-offset-reset: earliest       # Start from beginning on
                                        #    new group
      max-poll-records: 500             # Batch size per poll
      max-poll-interval-ms: 300000      # 5 min max processing time
      session-timeout-ms: 10000         # Broker considers consumer 
                                        #    dead after 10s
      heartbeat-interval-ms: 3000       # Send heartbeat every 3s
      isolation-level: read_committed     # Only read committed transactions
```

*max-poll-records: 500* — This is your throughput knob. 
* Higher = better throughput,
* lower = faster failure recovery.
* At 500, if processing fails, you re-process at most 500 records.

*isolation-level: read_committed* — Critical if your producers use transactions. Without this, you will read uncommitted messages that might be rolled back.

*session-timeout-ms: 10000* — If your consumer does not send a heartbeat for 10 seconds, the broker triggers a rebalance. *Set this higher than your max processing time for a single batch*.

#### **The Listener Container Configuration**

```java
@Bean
public ConcurrentKafkaListenerContainerFactory<String, MetricEvent>
    kafkaListenerContainerFactory() {

  ConcurrentKafkaListenerContainerFactory<String, MetricEvent> factory =
      new ConcurrentKafkaListenerContainerFactory<>();

  factory.setConsumerFactory(consumerFactory());
  factory.setConcurrency(3); // 3 threads for 6 partitions = 2 partitions/thread

  // CRITICAL: Manual acknowledgment mode
  factory.getContainerProperties()
      .setAckMode(ContainerProperties.AckMode.MANUAL);

  return factory;
```

#### **Committing Offsets in the Listener**

```java
@KafkaListener(
    topics = "${app.kafka.topic.metrics-events}",
    groupId = "${spring.kafka.consumer.group-id}",
    containerFactory = "kafkaListenerContainerFactory"
)
public void consumeMetric(
    @Payload ConsumerRecord<String, MetricEvent> record,
    @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
    @Header(KafkaHeaders.OFFSET) long offset,
    Acknowledgment acknowledgment) {  // Injected by Spring

  MetricEvent event = record.value();

  try {
    metricProcessor.process(event);

    // Only commit AFTER successful processing
    acknowledgment.acknowledge();

  } catch (Exception e) {
    // Send to DLQ, then commit to avoid poison pill
    sendToDeadLetterQueue(event, e.getMessage(), "PROCESSING_ERROR");
    acknowledgment.acknowledge();
  }
}
```


| ***Key insight:**** Even when processing fails, we commit the offset after sending to DLQ. This prevents a single bad message (****poison pill)**** from blocking the entire partition forever.* |
| --- |


## **2. The Dead Letter Queue Pattern**

A Dead Letter Queue (DLQ) is where messages go when they cannot be processed. 

Without a DLQ, you have two terrible options: 
* drop the message (data loss) or
* retry forever (partition stall).

The DLQ gives you a third option: park the message safely, keep the main pipeline moving, and investigate later.

#### **Two Categories of Failures**

**Validation Failures**

The message arrived but is semantically wrong. A null *serviceId*, a negative metric value, a missing required field. These will never succeed no matter how many times you retry. Send immediately to DLQ.

**Processing Failures**

The message is valid but something downstream failed. Redis is unavailable, database connection timed out, network blip. These might succeed on retry - but for simplicity in this implementation, we also send to DLQ and handle retry separately.

#### **Validation Before Processing**

```java
// Validate using Jakarta Bean Validation
Set<ConstraintViolation<MetricEvent>> violations = validator.validate(event);

if (!violations.isEmpty()) {
    String errorMsg = "Validation failed: " + violations.toString();
    log.error("Invalid metric event: eventId={}, errors={}",
              event.getEventId(), errorMsg);

    sendToDeadLetterQueue(event, errorMsg, "VALIDATION_ERROR");
    acknowledgment.acknowledge(); // Commit and move on
    return;
}
```

#### **The DLQ Sender**

```java
private void sendToDeadLetterQueue(
    MetricEvent event, String reason, String errorType) {

  // Enrich event with failure metadata before sending to DLQ
  Map<String, String> metadata = event.getMetadata();
  if (metadata == null) {
    metadata = new HashMap<>();
    event.setMetadata(metadata);
  }

  metadata.put("dlq_reason", reason);
  metadata.put("dlq_error_type", errorType);
  metadata.put("dlq_timestamp",
      String.valueOf(System.currentTimeMillis()));
  metadata.put("dlq_original_topic", inputTopic);

  deadLetterProducer
      .send(deadLetterTopic, event.getEventId(), event)
      .whenComplete((result, ex) -> {
          if (ex == null) {
              log.info("Sent to DLQ: eventId={}", event.getEventId());
          } else {
              // Critical: DLQ itself failed
              log.error("DLQ send failed: eventId={}",
                        event.getEventId(), ex);
          }
      });
}
```


| *Always enrich DLQ messages with failure metadata before sending. When you investigate failures 3 days later, you need to know WHY the message failed, WHEN it failed, and WHERE it came from.* |
| --- |


#### **Monitoring Your DLQ**

A growing DLQ is a production alert. In Kafka UI (or any Kafka management tool), watch the message count on your dead-letter topic. If it grows faster than your team can investigate, you have a systemic problem.

In StreamMetrics, we track this with a custom Micrometer counter:

```java
// Increment on every DLQ send
Counter.builder("metrics.failed")
    .tag("service", event.getServiceId())
    .tag("reason", errorType)
    .register(meterRegistry)
    .increment();
```

## **3. Observability: You Cannot Fix What You Cannot See**

The observability stack in StreamMetrics has three layers: 
* metrics (what happened),
* tracing (how it happened), and
* logging (why it happened).

This section focuses on metrics and tracing since those are the hardest to set up correctly with Kafka.

**The Stack**
* Micrometer — metrics facade (same API regardless of backend)
* Prometheus — metrics storage and query engine
* Grafana — dashboards and alerting
* Zipkin — distributed tracing (optional, gracefully degraded)

#### **Spring Boot Actuator Configuration**

```java
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
    distribution:
      percentiles-histogram:
        http.server.requests: true
      percentiles:
        http.server.requests: 0.5, 0.95, 0.99
```

The *tags.application* tag is critical. Without it, all your metrics from different services look identical in Prometheus. Always tag with the application name.

#### **The Key Apache Kafka Metrics**

After starting both producer and consumer, hit */actuator/prometheus* and look for these:

```java
# Producer: How many messages sent and at what latency
spring_kafka_template_seconds_count{result="success"}
spring_kafka_template_seconds_max

# Consumer: Records consumed per second
kafka_consumer_records_consumed_total

# Circuit breaker state (if using Resilience4j)
resilience4j_circuitbreaker_state
resilience4j_circuitbreaker_calls_seconds_count
```

#### **Grafana Queries That Actually Matter**

These are the three panels on the StreamMetrics dashboard:

```java
# Panel 1: Producer throughput (messages/sec)
rate(spring_kafka_template_seconds_count{result="success"}[1m])

# Panel 2: Max send latency
spring_kafka_template_seconds_max

# Panel 3: JVM heap pressure
jvm_memory_used_bytes{area="heap"}
```

#### **Distributed Tracing: Making Tracer Optional**

One lesson learned the hard way: never make your critical path depend on your observability infrastructure. If Zipkin is down, your Kafka producer should still work. Make the Tracer optional:

```java
@Service
@RequiredArgsConstructor
public class MetricProducerService {

  private final KafkaTemplate<String, MetricEvent> kafkaTemplate;
  private final Optional<Tracer> tracer; // Optional - won't fail if Zipkin is down

  public CompletableFuture<SendResult<String, MetricEvent>>
      sendMetric(MetricEvent event) {

    // Only add trace context if tracer is available
    tracer.ifPresent(t -> {
      if (t.currentSpan() != null) {
        String traceId = t.currentSpan().context().traceId();
        event.getMetadata().put("traceId", traceId);
      }
    });

    return kafkaTemplate.send(topic, event.getServiceId(), event);
  }
}
```


| *This is a general principle: observability tools should observe your system, not be a dependency of it. If your tracing library throws an exception and crashes your producer, you have made your system less reliable in the name of observability.* |
| --- |


## **4. Hard-Won Lessons from Building This**

#### **Kafka Docker Listener Configuration Is Unintuitive**

The single biggest time sink in this project was Kafka's listener configuration in Docker. When running Kafka in Docker and your Spring Boot app on the host machine, you need two separate listeners: one for internal *broker-to-broker* communication, and one for *external* clients.

```java
# docker-compose.yml — The config that finally worked
KAFKA_LISTENERS: 'PLAINTEXT://kafka1:19092,EXTERNAL://0.0.0.0:9092,CONTROLLER://kafka1:9093'
KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka1:19092,EXTERNAL://localhost:9092'
```
* The PLAINTEXT listener (port 19092) handles broker-to-broker traffic inside the Docker network.
* The EXTERNAL listener (port 9092) is what your Spring Boot app connects to via localhost.

Both are necessary.

#### **Stale Kafka Data Causes Mysterious Errors**

After changing Kafka configuration, always delete the data directories before restarting. Old cluster metadata causes ***DUPLICATE_BROKER_REGISTRATION*** errors that are confusing if you do not know what to look for.

```java
docker-compose down
rm -rf kafka1/data kafka2/data kafka3/data
docker-compose up -d
```

#### **Multi-Module Maven Requires Careful Ordering**

In a multi-module Maven project, the parent POM's module list determines build order. Common module must be listed first, or the producer will fail to find MetricEvent even though the dependency is declared correctly.

## **5. Results**

After implementing all of the above, StreamMetrics processes over 10,000 events per second through a 3-broker Kafka cluster with:
* Zero message loss (verified by tracking event IDs end to end)
* Failed messages safely parked in DLQ with full failure context
* Real-time throughput and latency visible in Grafana
* Optional distributed tracing through Zipkin
* Manual offset commits ensuring exactly-once processing semantics

## **What's Next**

Part 3 will cover Kafka Streams for real-time aggregations: computing 1-minute and 5-minute rolling averages of metric values, handling late-arriving data, and storing aggregated results back to Kafka and Redis.

The full code is available at: [github.com/ankitagrahari/StreamAnalytics](http://github.com/ankitagrahari/StreamAnalytics)

You can find my:

Github: 

Instagram: 

Medium:

Share your thoughts whether you liked or disliked it. Do let me know if you having any queries or suggestions. Never forget, Learning is the primary goal.

Learn with every commit.