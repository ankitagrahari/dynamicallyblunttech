---
title: "Reactive Programming in Java"
date: 2026-10-27T08:14:13+05:30
draft: false
featureImage: "images/df024c_67132d7c8df4416b97856a3cb317f28a.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"', '"6249579158f0bd10b2a57273"]']
showReadingTime: true
---

In this post, we will try to understand the basics of the ***Reactive programming***, what are the core features of it and how to handle the errors in reactive programming. This post will be more on the explanation section and less on coding something. That will come later. 

According to Wikipedia, Reactive Programming is defined as:

> Reactive programming is an asynchronous programming paradigm concerned with data streams and the propagation of change. This means that it becomes possible to express static (e.g. arrays) or dynamic (e.g. event emitters) data streams with ease via the employed programming language(s).

Reactive programming paradigm is often presented in object oriented languages as an extension of the Observer design pattern. It can also be compared to familiar iterator design pattern, with one difference where Iterator is **pull** based, while reactive streams are **push **based.

Reactive streams follows the *Publisher-Subscriber* pattern, where the publisher notifies the subscribers of newly available values as they come, and this push aspect is the key to being reactive. Also, operations applied to pushed values are expressed declaratively rather than imperatively. The programmer expressed the logic of the computation rather than describing its exact control flow. 

In addition to pushing values, the error-handling and completion aspects are also covered in a well defined manner. A *Publisher* can push new values to its *Subscriber *(by calling *onNext*) but can also signal an error (by calling *onError*) or completion (by calling *onComplete*). Both errors and completion terminate the sequence.

### **Why Reactive**

There is a detailed explanation about why it is used on the [*official site*](https://projectreactor.io/docs/core/release/reference/#intro-reactive). 

> By writing asynchronous, non-blocking code, you let the execution switch to another active task that uses the same underlying resources and later comes back to the current process when the asynchronous processing has finished.

Reactor libraries, such as Reactor, aim to address these drawbacks of *classic* asynchronous approaches on the JVM:
* Composability and readability
* Data as a flow manipulated with a rich vocabulary of operators.
* Nothing happens until you subscribe
* Backpressure or the ability for the customer to signal thte producer that the rate of emission is too high.
* High level but high values abstraction that is concurrency-agnostics.

### **Reactor Core Features**

You can use the following maven dependency in your project to use reactive features.

```java
<!-- https://mvnrepository.com/artifact/io.projectreactor/reactor-core -->
<dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-core</artifactId>
    <version>3.4.22</version>
</dependency>
```

In reactive paradigm, there are two types of response

- Single Object(Mono), or 

- List of Objects(Flux)

A *Flux* object represents a reactive sequence of *0..N* items, while a *Mono *object represents a single-value-or-empty(*0..1*) result.

### ***Flux*****, an Asynchronous Sequence of 0..N Items**

The following image shows how a `Flux` transforms items:

A *Flux<T>* is a standard *Publisher<T>* that represents an asynchronous sequence of 0 to N emitted items, optionally terminated by either a completion signal or an error. As in the Reactive Streams spec, these three types of signal translate to calls to a downstream Subscriber’s *onNext*, *onComplete*, and *onError* methods.

### ***Mono*****, an Asynchronous 0-1 Result**

The following image shows how a `Mono` transforms an item:

A *Mono<T>* is a specialized *Publisher<T>* that emits at most one item _via_ the *onNext* signal then terminates with an *onComplete* signal (successful *Mono*, with or without value), or only emits a single *onError* signal (failed *Mono*).

### **Simple ways to create Mono and Flux**
* Mono.empty() or Flux.empty() provide an empty Mono or Flux objects respectively.
* Mono.just(T) or Flux.just(T ...data) provide a mono of T object or Flux of T object respectively.

You can find following options to create Mono or Flux from either Publisher, Supplier, Stream, Array or Iterables.

### **Handling Errors**

These items below will allow you to easily identify the scenario and which operator to use.
* I want to create an erroring sequence: *error* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#error-java.lang.Throwable-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#error-java.lang.Throwable-))
* to replace the completion of a successful [*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html): *.concat(Flux.error(e))*
* to replace the emission of a successful [*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html)): *.then(Mono.error(e))*
* if too much time elapses between *onNexts*: *timeout* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#timeout-java.time.Duration-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#timeout-java.time.Duration-))
* lazily: *error(Supplier<Throwable>)* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#error-java.util.function.Supplier-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#error-java.util.function.Supplier-))
* I want the try/catch equivalent of: 
* throwing: *error **(*[*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#error-java.lang.Throwable-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#error-java.lang.Throwable-))
* catching an exception:
* and falling back to a default value: *onErrorReturn **(*[*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onErrorReturn-java.lang.Class-T-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#onErrorReturn-java.lang.Class-T-))
* and falling back to another [*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html) or [*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html): *onErrorResume* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onErrorResume-java.lang.Class-java.util.function.Function-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#onErrorResume-java.lang.Class-java.util.function.Function-))
* and wrapping and re-throwing: *.onErrorMap(t → new RuntimeException(t))* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onErrorMap-java.util.function.Function-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#onErrorMap-java.util.function.Function-))
* the finally block: *doFinally* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#doFinally-java.util.function.Consumer-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#doFinally-java.util.function.Consumer-))
* the using pattern from Java 7: *using **(*[*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#using-java.util.concurrent.Callable-java.util.function.Function-java.util.function.Consumer-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#using-java.util.concurrent.Callable-java.util.function.Function-java.util.function.Consumer-)) factory method
* I want to recover from errors
* by falling back:
* to a value: *onErrorReturn* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onErrorReturn-java.lang.Class-T-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#onErrorReturn-java.lang.Class-T-))
* to a [*Publisher*](https://www.reactive-streams.org/reactive-streams-1.0.3-javadoc/org/reactivestreams/Publisher.html?is-external=true) or [*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html), possibly different ones depending on the error: [*Flux#onErrorResume*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onErrorResume-java.lang.Class-java.util.function.Function-) and [*Mono#onErrorResume*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#onErrorResume-java.lang.Class-java.util.function.Function-)
* by retrying
* with a simple policy (max number of attempts): *retry()* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#retry--)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#retry--)), *retry(long)* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#retry-long-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#retry-long-))
* triggered by a companion control Flux: *retryWhen* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#retryWhen-reactor.util.retry.Retry-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#retryWhen-reactor.util.retry.Retry-))
* using a standard backoff strategy (exponential backoff with jitter): *retryWhen(Retry.backoff(…​))* ([*Flux*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#retryWhen-reactor.util.retry.Retry-)*|*[*Mono*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html#retryWhen-reactor.util.retry.Retry-)) (see also other factory methods in [*Retry*](https://projectreactor.io/docs/core/release/api/reactor/util/retry/Retry.html))
* I want to deal with backpressure "errors" (request max from upstream and apply the strategy when downstream does not produce enough request)    
* by throwing a special [*IllegalStateException*](https://docs.oracle.com/javase/8/docs/api/java/lang/IllegalStateException.html?is-external=true): [*Flux#onBackpressureError*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onBackpressureError--)
* by dropping excess values: [*Flux#onBackpressureDrop*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onBackpressureDrop--)
* except the last one seen: [*Flux#onBackpressureLatest*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onBackpressureLatest--)
* by buffering excess values (bounded or unbounded): [*Flux#onBackpressureBuffer*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onBackpressureBuffer--)
* and applying a strategy when bounded buffer also overflows: [*Flux#onBackpressureBuffer*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html#onBackpressureBuffer-int-reactor.core.publisher.BufferOverflowStrategy-) with a [*BufferOverflowStrategy*](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/BufferOverflowStrategy.html)

Refer to the operators needed [*here*](https://projectreactor.io/docs/core/release/reference/#which-operator)

***References***: [*https://projectreactor.io/docs/core/release/reference*](https://projectreactor.io/docs/core/release/reference) 

I hope this will help in understanding and getting a brief idea about the Reactive programming. Most of the content is taken from the official documentation with some explanation here and there. More on the reactive programming with the some examples will be covered in the upcoming posts.

You can find my [*Github*](https://github.com/ankitagrahari/)* *profile. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.