---
title: "Building DevOps Intelligence using MCP Server with Spring AI: Tools, Challenges & Solutions"
date: 2026-10-27T08:14:24+05:30
draft: false
featureImage: "images/df024c_f14bf2fc595446eebc628214a8897012.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"', '"6249579158f0bd10b2a57273"', '"681676055d80aaac0c9329be"]']
showReadingTime: true
---

Devops Intelligence

Today, I successfully built and deployed a **Model Context Protocol (MCP) server** using Spring AI that exposes real DevOps infrastructure through intelligent tools. But the journey? Let's just say it involved more debugging than coding.

In this post, I'll walk you through:
* What we built (the DevOps Intelligence Platform)
* The tools we created (K8s, Prometheus, Logs, Deployments)
* Every challenge we faced (and how we solved them)
* Why Spring AI 2.0.0-M2 is the sweet spot (M3 has still in development and after hours of debugging, settled with M2)

**TL;DR:** Built an MCP server with 5+ DevOps tools. Spent 6 hours debugging. Spring AI 2.0.0-M2 is your friend. No manual bean configuration needed if you know what to configure.

## What is MCP?

**Model Context Protocol** lets Claude (or any AI) directly access your tools through a standardized interface.

Instead of:

```java
Me → "Claude, what's my cluster health?"
Claude → "I don't know, you need to tell me"
```

Now:

```java
Me → "Claude, what's my cluster health?"
Claude → *calls k8s_cluster_health tool* → Returns real data
```

That's the power of MCP. Your AI gets **direct access** to your infrastructure.

## The DevOps Intelligence Platform: What We Built 🛠️

We created a Spring Boot application that exposes **real DevOps infrastructure** as MCP tools:

### Tools Implemented:

**K8s Tools** (KubernetesTools)
* k8s_cluster_health - Overall cluster status
* k8s_list_pods - List all pods with filtering
* k8s_recent_events - Recent cluster events

**Prometheus Tools** (PrometheusTools)
* prometheus_query_cpu - Query CPU metrics
* prometheus_query_memory - Query memory metrics
* prometheus_alerts - Active alerts

**Logs Tools** (LogsTools)
* logs_search - Search application logs
* logs_errors - Get recent errors
* logs_by_service - Filter logs by service

**Deployment Tools** (DeploymentTools)
* deployment_history - Deployment history
* deployment_rollback - Rollback mechanism
* deployment_status - Current deployment status

Here's what the MCP Inspector shows when fully connected:

*The DevOps Intelligence server with all tools discovered and ready to execute*

## Architecture: How It All Fits Together

## Challenge #1: Tomcat Web Server Pollution

**The Problem:**

```java
mvn spring-boot:run

20:01:48.612 [main] INFO o.s.boot.tomcat.TomcatWebServer - Tomcat initialized with port 8080
20:01:48.616 [main] INFO o.a.catalina.core.StandardService - Starting service [Tomcat]
```

When you add spring-boot-starter-web, Spring Boot starts **Tomcat HTTP server automatically**. But MCP STDIO protocol needs **pure process I/O**, not HTTP.

**The Solution:** Remove spring-boot-starter-web from pom.xml:

```java
<!-- REMOVE THIS -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

Keep only:

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server</artifactId>
    <version>2.0.0-M2</version>
</dependency>
```

> **Lesson:** MCP STDIO doesn't need a web server. It communicates directly via stdin/stdout.

## Challenge #2: Process Exits Immediately ⚡💀

**The Problem:**

```java
Started DevopsIntelligenceApplication in 0.301 seconds
[INFO] BUILD SUCCESS
(process exits)
```

Without Tomcat (or WebFlux), Spring Boot has nothing to keep the process alive.

**The Solution:**

**Option A:** Add spring-boot-starter-webflux (for light reactive server):

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

**Option B:** Keep process alive manually:

```java
public static void main(String[] args) {
    SpringApplication.run(
        DevopsIntelligenceApplication.class, args);
    try {
        Thread.currentThread().join();
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
}
```

I went with **Option A (WebFlux)** because it's the Spring Boot standard.

> **Lesson:** Something must keep the Spring Boot process alive. Either a server component or explicit thread joining.

## Challenge #3: JSON Protocol Corruption

**The Problem:**

```java
STDIO transport: command=...jar
Error in /stdio route: SyntaxError: Unexpected non-whitespace character after JSON at position 2
Error from MCP server: SyntaxError: Unexpected token '.', "  .   ____  "... is not valid JSON
```

**What was happening:** 

Spring Boot was printing startup banners and logs to STDOUT, which **corrupted the MCP protocol messages**. MCP STDIO uses stdin/stdout exclusively. 

ANY other output breaks the JSON-RPC protocol.

**The Solution:**

Configure application.yml to suppress all output:

yaml

```java
spring:
  main:
    banner-mode: "off"           # No ASCII art
    log-startup-info: false      # No startup messages
  application:
    name: devops-intelligence-mcp
  ai:
    mcp:
      server:
        name: devops-intelligence
        version: 1.0.0
        type: SYNC
        protocol: STDIO

logging:
  level:
    root: OFF                     # Turn off ALL logging
  file:
    name: mcp-server.log         # Send logs to file instead
```

**Key Settings:**
* banner-mode: "off" - No Spring Boot ASCII art
* log-startup-info: false - No startup logs
* logging.level.root: OFF - Suppress all logs
* [file.name](http://file.name): mcp-server.log - Redirect logs to file

> **Lesson:** For STDIO protocol, STDOUT must be **completely clean**. Even whitespace or warning messages break it.

## Challenge #4: Permission Denied (EACCES)

**The Problem:**

```java
Error: spawn /Users/.../target/devops-intelligence-0.0.1-SNAPSHOT.jar EACCES
errno: -13
code: 'EACCES' (permission denied)
```

**The Solution:**

```java
chmod +x target/devops-intelligence-0.0.1-SNAPSHOT.jar
```

BUT this still didn't work because **JAR files aren't executable binaries**.

**Real Solution:** Use java -jar instead in MCP Inspector UI:

```java
Command: java
Arguments: -jar /full/path/to/target/devops-intelligence-0.0.1-SNAPSHOT.jar
```

> **Lesson:** JAR files need java -jar to execute, not direct execution.

## Challenge #5: Request Timeout (32001)

**The Problem:**

```java
MCPError: 32001: Request timed out
Connection Error - Check if your MCP server is running and proxy token is correct
```

**Root Cause:** The server was running, but the **MCP Server bean wasn't being initialized**. The annotation scanner found tools, but there was no actual server to respond to protocol messages.

**The "****Fix****" I Tried (Didn't Work):**

```java
@Bean
public McpSyncServer mcpSyncServer() {
    return McpSyncServer.builder()  // ← This doesn't exist in M2!
        .name("devops-intelligence")
        .build();
}
```

Error:

```java
There is no builder with io.modelcontextprotocol.server.McpSyncServer
```

**The Real Fix:** Upgrade to **Spring AI 2.0.0-M2** (not M1 or M3)

In M2, the annotation scanner + auto-configuration handles everything:

```java
spring:
  ai:
    mcp:
      server:
        name: devops-intelligence
        version: 1.0.0
        type: SYNC
        protocol: STDIO
```

That's it. No manual bean creation needed.

> **Lesson:** Spring AI versions matter. M2 has the sweet spot. M1 is outdated, M3 has bugs.

## Challenge #6: Tools Not Discovered

**The Problem:** Server connected but tools tab was greyed out. No tools were visible.

**Diagnosis:**

```java
[✗] MCP Server bean NOT found
[✓] Found: org.springframework.ai.mcp.server.common.autoconfigure.annotations.McpServerAnnotationScannerAutoConfiguration
[✓] Found tool bean: k8sTools
[✓] Found tool bean: prometheusTools
```

Tools were registered as Spring beans, but the MCP Server wasn't being created.

**The Root Cause:** In Spring AI 2.0.0-M2, the auto-configuration for MCP server **isn't fully automatic**. The annotation scanner finds tools, but you need to ensure all components are properly wired.

**Solution 1 (Tried First - Overcomplicated):** Created a custom McpServerConfiguration with manual tool registration. Didn't work because the API wasn't right.

**Solution 2 (What Actually Worked - SIMPLE):** Just ensure:

✅ @Component on tool classes

✅ @McpTool on tool methods

✅ Proper application.yml

✅ Dependency: spring-ai-starter-mcp-server:2.0.0-M2

Spring AI M2 handles the rest automatically.

> **Lesson:** Less is more. Don't overthink it. Spring AI M2 is designed to auto-discover tools if configured correctly.

## The Final Solution: application.yml

Here's the **complete, minimal configuration** that works:

```java
spring:
  main:
    web-application-type: none
    banner-mode: "off"
#    log-startup-info: false
  application:
    name: devops-intelligence-mcp
  ai:
    mcp:
      server:
        name: devops-intelligence
        version: 1.0.0
#        type: SYNC
#        protocol: STDIO
        stdio: true

logging:
  level:
    root: INFO
  file:
    name: mcp-server.log

server:
  port: 8080
```

**That's it. Everything else is default.**

## Tool Implementation Example: K8sTools

Here's how a tool class looks:

```java
@Component
public class K8sTools {

    private final K8sMockClient k8sClient;

    public K8sTools(K8sMockClient k8sClient) {
        this.k8sClient = k8sClient;
    }

    @McpTool(
            name = "k8s_cluster_health",
            description = "Get overall Kubernetes cluster health including node and pod status"
    )
    public String describeClusterHealth() {
        var pods = k8sClient.listPods();
        var nodes = k8sClient.listNodes();

        long healthyPods = pods.stream()
                .filter(p -> "Running".equals(p.status()) && "1/1".equals(p.ready()))
                .count();

        long readyNodes = nodes.stream()
                .filter(n -> "Ready".equals(n.status()))
                .count();

        StringBuilder sb = new StringBuilder();
        sb.append("Cluster Health Summary:\n");
        sb.append(String.format("Nodes: %d/%d Ready\n", readyNodes, nodes.size()));
        sb.append(String.format("Pods: %d/%d Running\n", healthyPods, pods.size()));

        return sb.toString();
    }

    @McpTool(
            name = "k8s_list_pods",
            description = "List all Kubernetes pods with their status"
    )
    public String listPods(
            @McpToolParam(description = "Filter by namespace (optional)", required = false)
            String namespace) {
        var pods = k8sClient.listPods();

        if (namespace != null && !namespace.isEmpty()) {
            pods = pods.stream()
                    .filter(p -> p.namespace().equals(namespace))
                    .collect(Collectors.toList());
        }

        StringBuilder sb = new StringBuilder("Kubernetes Pods:\n");
        pods.forEach(p ->
                sb.append(String.format(
                        "  %s/%s - Status: %s, Ready: %s\n",
                        p.namespace(), p.name(), p.status(), p.ready()
                ))
        );

        return sb.toString();
    }
}
```

**Key Points:**
* @Component - Spring discovers this as a bean
* @McpTool - Spring AI discovers this as an MCP tool
* Tool methods return String (serialized to JSON-RPC)
* @McpToolParam - Optional parameters for tools
* Constructor injection for dependencies

Since these are getting mock data, we can use the client libraries for Kuberentes, or ELK, or Github, to fetch data from the infrastructure you are going to connect this tool with. 

For example using the Kubernetes client libraries

```java
/**
 *
 * Ref Source: https://github.com/kubernetes-client/java/blob/master/examples/
 */
public interface KubernetesClient {

    static Class<? extends KubernetesObject> getClassForKind(String kind) {
        return switch (kind) {
            case "pod", "pods" -> V1Pod.class;
            case "deployment", "deployments" -> V1Deployment.class;
            case "service", "services" -> V1Service.class;
            case "node", "nodes" -> V1Node.class;
            case "replicationcontroller", "replicationcontrollers" -> V1ReplicationController.class;
            default -> null;
        };
    }

    String PADDING = "                              ";

    private static String pad(String value) {
        while (value.length() < PADDING.length()) {
            value += " ";
        }
        return value;
    }

    default KubernetesObject delete(String kind, String ns, String name) throws KubectlException {
        return Kubectl.delete(getClassForKind(kind))
                .namespace(ns)
                .name(name)
                .execute();
    }

    default KubernetesObject drain(ApiClient apiClient, String name) throws KubectlException, IOException {
        return Kubectl.drain()
                .apiClient(apiClient)
                .name(name)
                .execute();
    }

    default void portForwarding(ApiClient apiClient, String ns, String name, String port) throws KubectlException {
        //port: 8080:8080
        KubectlPortForward forward = Kubectl.portforward()
                .apiClient(apiClient)
                .name(name)
                .namespace(ns);

        String[] ports = port.split(":");
        System.out.println("Forwarding " + ns + "/" + name + " " + ports[0] + "->" + ports[1]);
        forward.ports(Integer.parseInt(ports[0]), Integer.parseInt(ports[1]));
        forward.execute();
    }

    default void scale(ApiClient apiClient, String kind, String ns, String name, Integer replicas) throws KubectlException {
        Kubectl.scale(getClassForKind(kind))
                .apiClient(apiClient)
                .namespace(ns)
                .name(name)
                .replicas(replicas)
                .execute();
    }

    default String getVersion(ApiClient apiClient) throws KubectlException {
        return Kubectl.version()
                .apiClient(apiClient)
                .execute()
                .toString();
    }

    default Integer execute(ApiClient apiClient, String ns, String name, String container, String[] command) throws KubectlException {
        return Kubectl.exec()
                .apiClient(apiClient)
                .namespace(ns)
                .name(name)
                .command(command)
                .container(container)
                .execute();
    }
    .
    .
    .
    .

}
```

Refer to the repo for the complete code base. Similarly ELK and Github should be using their client libraries. 

## Testing with MCP Inspector

Once connected, you can:

**See all tools** in the Tools tab

**Click a tool** to view its parameters

**Execute the tool** and see results in real-time

**Check History** of all tool calls

The Inspector shows exactly what Claude sees when using your tools.

## GitHub Repository

Full source code available: 🔗 [https://github.com/ankitagrahari/devops-intelligence](https://github.com/ankitagrahari/devops-intelligence)

Key files:
* *src/main/java/org/backendbrilliance/devopsintelligence/tools* - All tool implementations
* *src/main/resources/application.yml* - Configuration
* *src/main/java/org/backendbrilliance/devopsintelligence/clients/mocks* - Mock clients
* *src/main/java/org/backendbrilliance/devopsintelligence/clients* - Actual client implementation.

## Lessons Learned 📚

**Spring AI 2.0.0-M2 is the sweet spot** - M1 is old, M3 is not completely ready as it is still under snapshot view. 

**MCP STDIO needs pure I/O** - No logs, no web servers, no output to STDOUT

**Auto-configuration > Manual beans** - Let Spring do the heavy lifting

**Annotation scanner is powerful** - @Component + @McpTool is all you need

**Test with MCP Inspector first** - Then integrate with Claude Desktop

**Mock clients for development** - Real infrastructure comes later

## What's Next?
* ✅ MCP server running with 5+ tools
* ✅ Inspector can discover and execute tools
* ✅ Ready to integrate with Claude Desktop
* 🔜 Real K8s/Prometheus integration
* 🔜 Autonomous incident response
* 🔜 Cost optimization analysis

## Final Thoughts

Building an MCP server is **surprisingly straightforward** once you know the gotchas:
* Remove web servers (STDIO needs pure I/O)
* Suppress all logging (STDOUT is sacred)
* Use Spring AI 2.0.0-M2 (sweet spot version)
* Keep configuration minimal (auto-discovery works)

The debugging journey was long, but the end result is clean, maintainable code that gives Claude **direct access to your infrastructure**. That's powerful.

Next stop: Making Claude your autonomous DevOps sidekick. 🚀

## Stay Updated

Follow me for more:
* 📝 Blog: [dynamicallyblunttech.com](http://dynamicallyblunttech.com)
* 📷 Instagram: [@backendbrilliance](https://instagram.com/backendbrilliance)
* 💼 LinkedIn: [ankitagrahari](https://linkedin.com/in/ankitagrahari)
* 💻 Medium: [ankitagrahari.rkgit](https://medium.com/@ankitagrahari.rkgit)

## Happy building!