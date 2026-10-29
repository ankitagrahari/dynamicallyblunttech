---
title: "Using Twilio for Sending WhatsApp Message in Java"
date: 2026-10-27T08:14:22+05:30
draft: false
featureImage: "images/df024c_792ebe5e0a3d490cb4d343575fca93f5.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this blog post, we will try to send WhatsApp message in Java using [*Twilio account*](https://www.twilio.com/docs/whatsapp). 

**Prerequisite: **

Create a free account in Twilio.

Once verified, you will have your own account SID and authorization token.

Thereafter, you need to activate the Sandbox.

Now add the number +14155238886 in you mobile account and send a message "***join up-post***" (without quotes).  

This will register your mobile number with Twilio sandbox and now you are eligible to send WhatsApp messages. The sandbox will look like below:

Now we will write simple java code to initiate the engine and send message using program to any registered number.

### **Maven Dependency**

Add maven dependency for Twilio java library

```java
<dependency>
    <groupId>com.twilio.sdk</groupId>
    <artifactId>twilio</artifactId>
    <version>7.51.0</version>
</dependency>
```

After adding the maven dependency, create a new program with the below method and global variables.

```java
private String ACCOUNT_SID="ABCDEFGHIJKLMNOPQRSTVWXYZ";
private String AUTH_TOKEN="123abc456def789ghi";

private void sendMessageUsingTwilio(){
    Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
    Message message = Message.creator(
            new com.twilio.type.PhoneNumber("whatsapp:+xxxxxxxxxxx"),
            new com.twilio.type.PhoneNumber("whatsapp:+14155238886"),
            "Hello there!")
            .create();

    System.out.println(message.getSid());
}
```

The *Message.creator* takes three arguments: ***to***, ***from*** and ***message. ***You can get the account SID and Auth token from the Twilio dashboard. 

### **Custom HTTP Client**

The Twilio Java helper library also provide custom ***HttpClient ***which can be created like this. Twilio used ***org.apache.http.client*** package for its custom ***HttpClient***. Add the below lines before creating and sending the message like ***Message.creator()*** method.

```java
ProxiedTwilioClientCreator clientCreator = new ProxiedTwilioClientCreator(
        ACCOUNT_SID, AUTH_TOKEN, PROXY_HOST, PROXY_PORT);
TwilioRestClient twilioRestClient = clientCreator.getClient();
Twilio.setRestClient(twilioRestClient);
```

You can find the entire code here on my [Github ](https://github.com/ankitagrahari/Tryouts/tree/master/src/main/java/com/watsapp)repository.

#### **References**
* [*https://www.twilio.com/blog/what-does-twilio-do*](https://www.twilio.com/blog/what-does-twilio-do)
* [*https://www.twilio.com/docs/whatsapp/quickstart/java*](https://www.twilio.com/docs/whatsapp/quickstart/java)
* [*https://www.twilio.com/docs/libraries/java*](https://www.twilio.com/docs/libraries/java)
* [*https://www.twilio.com/docs/libraries/java/custom-http-clients-java*](https://www.twilio.com/docs/libraries/java/custom-http-clients-java)

#### **NOTE**:
* This is a fun project but always remember not to share your SID or authorization token details. You should also verify that you don't mistakenly shared it with the code.
* Twilio is not free and is having a trial period of 14 days.

Hope you will enjoy as much as I enjoyed trying it out. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.