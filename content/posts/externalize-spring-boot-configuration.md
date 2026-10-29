---
title: "Externalize Spring Boot Configuration"
date: 2026-10-27T08:14:30+05:30
draft: false
featureImage: "images/df024c_89158371d37b4e4a93bbda5b54eb02da.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"', '"6249579158f0bd10b2a57273"]']
showReadingTime: true
---

In this post, we will discuss on fetching the Spring boot configuration values from outside the application jar file. We will discuss on dockerizing the application which will take the property values from an external configuration file. We will also use different Profiles to get the message 
based on the profile we choose. 

We have also discussed on Spring boot configuration files and how to get the values from it in this post [*spring-boot-application-external-configurations*](https://www.dynamicallyblunttech.com/post/spring-boot-application-external-configurations)*.*

To start with, we will need a Spring boot application, which will have one endpoint */api/message* to get the message from the spring configuration file. To get the spring boot application, you can directly go to [*https://start.spring.io/*](https://start.spring.io/) website and create a spring project with maven and choose the Spring Web dependency. It is a small demonstration where no other dependency is required. 

### **Profile**

Now that we have the spring boot application which will have the required dependencies, we have to create different maven profile and respective *application-{profile}.properties* files under the resources directory. 

To add the maven profile, we need to add the following profile tag in the pom.xml file. 

We have two profiles *dev* and *cloud *and marked the ***dev*** profile as the default profile. 

The *application.properties* file will define the active profile. 

```java
server.port=9898
spring.profiles.active=@activatedProperties@
dbt.message=DynamicallyBluntTech
```

The *spring.profiles.active* will have the variable (*activatedProperties*) which will be getting the value from external parameter defined by user during the startup. 

Similarly, the other profile configuration file will have different message for the key *dbt.message**.*

##### *application-cloud.properties*

```java
dbt.message=Cloud-DBTech
```

##### *application-dev.properties*

```java
dbt.message=Dev-DBTech
```

### **Controller**

The Rest controller will have one endpoint which will get the value for this *dbt.message* key.

Once the controller is ready, we can start our spring boot application, which will take the dev profile as the default to start with. And the call to */api/message* will also fetch the *dbt.message* value from *application-dev.properties* file. 

And the API endpoint call will give this

Now, lets the run the spring boot application as jar file with the active profile set to cloud

And now the API endpoint call will give this

Till this point we were getting the values from the configuration values based on the profile which we are choosing during the startup of the project. If we define the cloud profile, the values present in the cloud configuration file is fetched. 

Now lets say we are working on the project, where we want to spawn multiple instance of the same application, but with different messages for each instances. This could be different database connection parameters or different Kafka topics to consume data from. 

How would we take the configurable parameters during the startup of the application dynamically ?

### **Dockerize**

So lets first create our Dockerfile which will push the artifact to the docker hub. 

We are 

taking the openjdk version 11, and 

marking /dbt as the work directory 

Copying the application jar file to the docker container with the name application.jar

Exposing the port 9898 for accessing application outside the docker container.

Defining the command to execute the jar file by passing the value of the *dbt.message* key.

By doing this, we are just overriding the specific configuration parameter key while starting the application. But lets say I have bunch of parameters that needs to be changed for each instance spawned. Adding all these parameters in the ENTRYPOINT command will make it more confusing and will become error prone. 

In these scenarios, we can also create the profile specific configuration file where the jar file is added. And then add the respective active profile in the run command. So, now the Dockerfile  will look like this 

This will override the *application-cloud.properties* configuration present in the application.jar file by the *application-cloud.properties* file we copied. 

We will build and push the docker image using the above Dockerfile

```java
docker build -f .\src\main\java\dockerize\Dockerfile -t dockerize:tb1
```

And run the docker image dockerize:tb1 on the port 9898

```java
docker run -p 9898:9898 dockerize:dbt1
```

The endpoint from the docker image will fetch the data for *dbt.message* key from the value set in the Dockerfile

Now lets answer this question: 

Q> How would we take the configurable parameters during the startup of the application dynamically ?

A> We can use the configuration file or we can use specific property in the Entrypoint command of our Dockerfile to pass the values during the docker run. 

You can find the code in my [*Github*](https://github.com/ankitagrahari/Dockerize) repo. Hope this helps in understanding the external configuration of the spring boot application and how we can override the configuration specific values or the entire configuration file. 

This was more on the static configuration of the Spring boot application, because once the application is started, you cannot change the configuration parameters and its values. To change it during the runtime, Spring has provided Spring Cloud configuration which will fetch the configuration values from the external files stored in some cloud repository like Github or Gitlab, etc. More on this in the next post of the external configuration of Spring boot applications. 

Hope this will help you in your learning process. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.