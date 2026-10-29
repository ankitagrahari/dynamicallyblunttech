---
title: "Testing in Microservices"
date: 2026-10-27T08:14:20+05:30
draft: false
featureImage: "images/df024c_86bd74d688bd45d8b3da7eae9f2405a9.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

In this post we will go through the integration testing of the controller of any Spring Boot project. We will be using an existing Spring boot project which was created for the [*previous post*](https://www.dynamicallyblunttech.com/post/read-write-excel-using-apache-poi-java). First lets go through the types of testing that can be done in Microservices environment.

## **Types of Testing in Microservices**

In Microservices architecture, where different servcies interact with each other it becomes a bit complex to test all the services and keeping the automated test cases will help in recognizing any shared services and the impact of change on one another services.

These following are different types of testing which can be done in any Microservices architecture:

Unit Testing 

Component Testing

Integration Testing

End-to-End Testing

### **End-to-End/System testing **

It covers the entire flow to test, e.g. in Amazon e-commerce website, from selecting an item to adding to the cart, and going through the payment gateway and placing an order with the order details shared with customer is all one flow, where a blockage at any endpoint will result in failure of the entire flow and will have restart again. So, lets say if some developer has changed something in the Add to cart functionality and now users are only able to add items of the same category. These kind of scenarios can be caught early in development phase using the end-to-end testing. 

### **Integration Testing**

During an integration testing, all the services are tested which are interacting with it. Considering the number of modules which are referenced, it can become very complex also. It test that my service is working when added to the entire Microservices present.

### **Component Testing**

In component testing, Microservices is executed as black box unknown to outer world, testing the interface behavior. It tests that every single Microservice is working as per the requirements.

### **Unit Testing**

It includes testing of all the utilities, services or any other helping classes, which are used by the Service or Controller classes. It make the code more agile and improves the code quality. In IntelliJ or any other IDE, you can generate the Test Case for the entire class or for some specific methods.

## **Writing Test for Spring Boot Project**

When we create our project initially from [*Spring Initializr*](https://start.spring.io/), we can see there are *spring-boot-starter* and *spring-boot-starter-test* dependency already added to the pom file. The microservices architecture will look something like this. Here endpoints will be from different services performing different task.

### **Dependency**

We will be using the our own Junit and not the one clubbed together with the Spring starter

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-engine</artifactId>
    <scope>test</scope>
</dependency>
```

Check for the *src/test* package, which will have a Test class created by Spring already as part of the initial project.

### **Writing First Test**

The Test class present in the *src/test *package will have *@SpringBootTest* annotation which tell to start the Spring application with the class having *@SpringBootApplication* and also states that this is the Test class for out Spring Boot application.

We will enable the auto configure of *MockMVC *by using the *@EnableAutoConfigureMockMvc* annotation. So my final class will look like this

```java
@AutoConfigureMockMvc
@SpringBootTest
class ApachepoiApplicationTests {

    @Autowired
    MockMvc mockMvc;
    
    @Test
    void contextLoads() {}
```

We have auotwired the *MockMvc *class to perform any of the Rest call to different endpoints.

You can also notice the empty *contextLoads()* method which ensures that whenever you start the test run, it verifies that the Test has loaded the Spring Context properly or not. 

### **Get Request**

Lets create a test method using *MockMvc *class which will call a specific Get Endpoint and verify the status is *200 OK* and return the *MvcResult *instance. We can extract String response from *MvcResult *instance.

```java
@Test
void readDummyExcelTest() throws Exception {
    MvcResult result = mockMvc.perform(
            MockMvcRequestBuilders
                    .get("/excel/readDummy")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON))
                    .andExpect(status().isOk())
                    .andReturn();
    System.out.println(result.getResponse().getContentAsString());

    Assertions.assertNotNull(result.getResponse().getContentAsString());
    Assertions.assertEquals("Success", result.getResponse().getContentAsString());
}
```

Here the perform method of *MockMvc *class takes *RequestBuilder* which is used to construct an Get Request. In the request construct, we can set the *contentType*, what type to accept as response and verify if the status of the request is *200 OK*. At last return a *MvcResult *object.

And we are using Junit Assertions methods like *assertNotNull()*, *assertEquals()* etc. to assert the output with the expected response.

### **Post Request**

As the above get request test method, we will create another test for Post request, where we can set the content as String only.

```java
@Test
void integrationPostTest() throws Exception {
    ExcelRowEle obj = new ExcelRowEle();
    obj.setOpen(500); obj.setHigh(700);
    obj.setClose(678); obj.setLow(477); obj.setVolume(5623498);
    obj.setTypicalPrice((obj.getHigh()+obj.getLow()+obj.getClose())/3);
    obj.setVp(obj.getVolume()*obj.getTypicalPrice());
    obj.setTotalV(obj.getVolume()); obj.setTotalVP(obj.getVp());
    obj.setVwap(obj.getTotalV()/obj.getTotalVP());

    MvcResult result = mockMvc.perform(MockMvcRequestBuilders
            .post("/excel/test")
            .content(objectMapper.writeValueAsString(obj))
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andReturn();

    String response = result.getResponse().getContentAsString();

    Assertions.assertEquals(response, obj.toString());
}
```

In the above method, we are creating a Model and setting the content with our *Model(ExcelRowEle*) in the JSON format.

***NOTE****: With RequestBuilder, you can only set the content or get the response as String. Then we can use ObjectMapper class to convert in JSON format.*

You can refer to my [*github repository*](https://github.com/ankitagrahari/apachepoi/) for the full codebase. The test class is present [*here*](https://github.com/ankitagrahari/apachepoi/blob/main/src/test/java/com/dynamicallyblunttech/apachepoi/ApachepoiApplicationTests.java).

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.

### References
* [https://spring.io/guides/gs/testing-web/](https://spring.io/guides/gs/testing-web/)