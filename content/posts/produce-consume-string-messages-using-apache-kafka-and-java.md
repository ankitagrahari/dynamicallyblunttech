---
title: "Produce & Consume Messages Using Apache Kafka"
date: 2026-10-27T08:14:13+05:30
draft: false
featureImage: "images/df024c_a5726e451bc844f7881b2b72ba949c1c.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

In this post, we will create a Kafka producer which will produce string messages as Rest call and a consumer which will consume the produced messages.

## **Install/Setup Kafka**

To download Kafka refer to the [Apache Kafka Download website](https://kafka.apache.org/downloads).

Pick any of the desired package. For this post we chose 2.8.1
* Scala 2.12  - [*kafka_2.12-3.0.0.tgz*](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.0.0/kafka_2.12-3.0.0.tgz) ([*asc*](https://downloads.apache.org/kafka/3.0.0/kafka_2.12-3.0.0.tgz.asc), [*sha512*](https://downloads.apache.org/kafka/3.0.0/kafka_2.12-3.0.0.tgz.sha512))

#### **NOTE**: The version 2.13.3 is not working and will throw Connection Refused error.

### **Steps to Setup:**

Extract the tgz file to some directory.

Open *zookeeper.properties* file under *config* directory and provide the ***dataDir ***value. It is the data directory used by Kafka to store the data.

Open *server.properties* file under *config* directory and provide the ***logs-dir*** kafka logs directory.

Start the zookeeper by running following command:
* if Windows:
*.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties*
* if Unix:
*.\bin\zookeeper-server-start.sh .\config\zookeeper.properties*

**NOTE**:
**Problem: **If you are getting following error:

		"***input line is too long kafka***

		***The syntax is not correct"***

**Reason:** This is happening because the allowed characters in windows for classpath is only 8191 characters. But when the above command is executed, it sets each jar file found under the *lib* directory to the classpath variable. This make the statement increase the characters length threshold.

**Solution:** 
* Open the kafka-run-class.bat file under bin/windows directory.
* Search for "*rem Classpath addition for release**" *

*            ***Replace these line**
                *rem Classpath addition for release*

*                for %%i in ("%BASE_DIR%\libs\*") do (*
*                 	call :concat "%%i"*
*                )*

*           ***With these**
                *rem Classpath addition for release*
                *call :concat "%BASE_DIR%\libs\*;"*


Once the zookeeper is started successfully without any error, then start kafka server using below command:

***For Windows:***

        *.\bin\windows\kafka-server-start.bat .\config\server.properties*

***For Unix:***
        *.\bin\kafka-server-start.sh .\config\server.properties*

If you want to stop, then run the corresponding stop scripts for zookeeper and kafka server.

## **Create Kafka Topic**

When a message is sent to Kafka broker, it will send the message to a specific topic, which can be thought of as address where the post can be delivered. This way consumer can differentiate between the messages which are relevant to get consumed than all other messages.

We can create a kafka topic like this:

**For Unix:   **

```java
./kafka-topics.sh --create --topic mt -zookeeper localhost:2181 --replication-factor 1 --partitions 1
```

**For Windows**

```java
./windows/kafka-topics.bat --create --topic mt -zookeeper localhost:2181 --replication-factor 1 --partitions 1
```

## **Create Spring Project**

From the Spring Initializer, either from IDE or the website, create a spring maven project with the following dependency:
* Spring Web ([*Maven Repo*](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-web))
* Kafka - Spring ([*Maven Repo*](https://mvnrepository.com/artifact/org.springframework.kafka/spring-kafka))

### **Creating Producer Based on Configurations**

The project will have a producer which will produce the string messages.

```java
@Configuration
public class ProducerConfigs {

    private static final String KAFKA_BROKER = "localhost:9092";

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate(){
        return new KafkaTemplate<>(producerFactory());
    }

    @Bean
    public ProducerFactory<String, String> producerFactory(){
        return new DefaultKafkaProducerFactory<>(producerConfigurations());
    }

    @Bean
    public Map<String, Object> producerConfigurations(){
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA_BROKER);
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        return config;
    }
}
```

In the above code base, we are defining the producer configuration which states that the producer will be producing the messages to the ***KAFKA_BROKER *** URL defined, and the Key and Value of the message will be of type String.

Here the Kafka template is used to produce messages from producer created from the producer factory . The producer are created based on configurations given.

### **Creating Consumer Based on Configurations**

The project will have a consumer which will consumer the string messages.

```java
private static final String KAFKA_BROKER = "localhost:9092";
private static final String GROUP_ID = "kafka-sandbox";

@Bean
public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory(){
    ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(consumerFactory());
    return factory;
}

@Bean
public ConsumerFactory<String, String> consumerFactory(){
    return new DefaultKafkaConsumerFactory<>(consumerConfigurations());
}

@Bean
public Map<String, Object> consumerConfigurations(){
    Map<String, Object> config = new HashMap<>();
    config.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA_BROKER);
    config.put(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
    config.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    config.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);

    return config;
}
```

In the above code base, with the ***KAFKA_BROKER ***it will also require the ***GROUP_ID ***which is mandatory by Kafka for parallel data consumptions. Similarly the ***ConcurrentKafkaListenerContainerFactory ***is used to consume multiple messages by different threads.

Here the consumer configurations is given to connect to the ***KAFKA_BROKER ***with the ***GROUP_ID ***and the Key and Value deserialize class (here it is String).

### **Create Topic-wise Consumer for specific action**

This will be topic specific consumer where you can perform specific actions. Here we will listen to the kafka for any new messages produced on the kafka topic we created and will store it to a list. We will also create a ***getMessages()*** method to get the list of messages.

```java
private final List<String> messages = new ArrayList<>();

@KafkaListener(topics = "mt", groupId = "kafka-sandbox")
public void listen(String message){
    synchronized (message){
        messages.add(message);
    }
}

public List<String> getMessages(){
   return messages;
}
```

It listens on the topics mentioned and the group-id given.

### **Create Rest Controller to produce and consume messages**

In the Rest controller, we will create a produce method which will send the data via kafka template on the given topic. 

```java
@GetMapping("/kafka/produce")
public void produce(@RequestParam String message){
    kafkaTemplate.send("mt", message);
}
```

And will create a another method which will display all the messages produced by the producer.

```java
@GetMapping("/kafka/messages")
public List<String> getMessages(){
   return mtConsumer.getMessages();
}
```

Start the spring application and run the following get REST call to send any specific messages like this where we are sending 4 messages to kafka topic ***mt***:

*http://localhost:8080/kafka/produce?message="Kafka with Java on DynamicallyBluntTech1"*

*http://localhost:8080/kafka/produce?message="Kafka with Java on DynamicallyBluntTech2"*

*http://localhost:8080/kafka/produce?message="Kafka with Java on DynamicallyBluntTech3"*

*http://localhost:8080/kafka/produce?message="Kafka with Java on DynamicallyBluntTech4"*

Similarly, we can run the REST call for ***getMessages()*** to display all the messages which the consumer has consumed, like below:

*http://localhost:8080/kafka/messages*


which will display following 4 messages which was produced:

["\"Kafka with Java on DynamicallyBluntTech1\"", "\"Kafka with Java on DynamicallyBluntTech2\"", "\"Kafka with Java on DynamicallyBluntTech3\"", "\"Kafka with Java on DynamicallyBluntTech4\""]

In this way we can produce and consumer string messages. We can also produce and consume the JSON object as well, only change would be to use ***Jsonserializer ***and ***JsonDeserializer ***class as part of the configuration given to the producer and consumer. 
To get the entire code base of the above example, refer to this [*Github link*](https://github.com/ankitagrahari/JavaKafka/tree/main/src/main/java/example/kafka) here.


#### References
[https://developer.okta.com/blog/2019/11/19/java-kafka](https://developer.okta.com/blog/2019/11/19/java-kafka)
[https://www.geeksforgeeks.org/spring-boot-how-to-publish-string-messages-on-apache-kafka/](https://www.geeksforgeeks.org/spring-boot-how-to-publish-string-messages-on-apache-kafka/)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.