---
title: "Junit5 with Mockito Framework"
date: 2026-10-27T08:14:26+05:30
draft: false
featureImage: "images/df024c_e7626a0fdfbe45d187b1b7703bd15778.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

In this blog post we will talk about one of the testing framework which I wanted to try it on, and rather use it in my day to day coding.

> Mockito framework is the mocking framework that tastes really good.

This is from the official Mockito [*website*](https://site.mockito.org/), and I have not played with words here. :)

But as it says, it did taste good and you might extend your Junits with Mocks, because this is clean, readable and produce clean verification errors. Also it will become addictive.

Mockito framework mocks the objects by either
* Using static methods, or
* Mocks annotations.

Mockito provides
* Annotation Support,
* Exception Support,
* Order support to run test cases.

In this post, we will use annotations to mock the objects and will try to apply it in our existing project and learn a few key concepts associated to it.

## **Mocks and Stubs**

*Stubs* can be defined as an clone of the instance with same attributes and behavior injected with our sample dataset, that can be used for testing.

*Mocks* is something which creates an image of the same class, and we can create the dataset as per the test cases.

## **Need for Mocks**

When we have to write the Junits for our code
* We need to identify the dependency like: database, webservices, other classes etc. and
* How many other Junits are accessing the same tables of that database. This would again reset or change the data consistency for our test criteria.

Mockito comes with benefits of eliminating the dependency which would ease the creation of implementing our unit test cases. It would also keep the data consistency and integrity, because it will not change the data set used by other Junits test cases.

Another important aspects of using Mockito is to eliminate the external dependency on databases, or Webservices to be present for the execution of test. This will take care of the any slow IO operations also, if we use the Mockito which is part of the codebase.

## **Maven Dependency**

You can add the following maven dependency in your pom xml file.

```java
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>4.4.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>4.4.0</version>
    <scope>test</scope>
</dependency>
```

## **Example**

We will refer to our previous blog post on implementing [*Lambda and Functional progamming in Java 8*](https://www.dynamicallyblunttech.com/post/day-to-day-lambda-functional-programming-java-8), to implement different test cases. You can find the Github link [*here*](https://github.com/ankitagrahari/Learn/tree/main/src/main/java/com/java8).

### **How to Write a Stub Class and Use it**

When we talk about Stub, think this as a data structure which has some dummy data for my Junits to work on. So that, we don't have to depend on the external database or webservices to return the dataset. A *stub *class can be created of your Entity, and you can add as many method required for the Junits written.

I will use the [*User.java*](https://github.com/ankitagrahari/Learn/blob/main/src/main/java/com/java8/User.java) class from the previous post and will create a *UserStub.java* out of it. It will return dataset for its getter methods.

```java
Faker faker = new Faker();

public String getFirstName() {
    return faker.name().firstName();
}

public String getLastName(){
    return faker.name().lastName();
}

public Integer getAge(){
    return faker.number().numberBetween(1, 100);
}
```

In this example, I have used *javaFaker *third party tool, which creates random dummy dataset each time it is called. Easy and fun tool to use. You can refer the complete Stub class on my Github [*here*](app://obsidian.md/index.html).

Implementing this *UserStub *class will be like any other utility/helper class invoked when the data is required. Then the assertion will be done based on the dataset provided.

We will refer to two Junits *sortByAgeDescAndNameAsc()* and *getAverageAgeOfUsers()* here

```java
@Test
public void sortByAgeDescAndNameAsc() {
    List<User> users = userStub.getDummyUsersWithAllPrivileges();
    List<User> sortedUsers = userService.sortByAgeDescAndNameAsc(users);

    assertEquals(50, sortedUsers.get(0).getAge());
    assertEquals("dynamically", sortedUsers.get(0).getFirstName());
    assertEquals("blunt", sortedUsers.get(0).getLastName());

    assertEquals(32, sortedUsers.get(2).getAge());
    assertEquals("dynamically", sortedUsers.get(2).getFirstName());
    assertEquals("blunttech", sortedUsers.get(2).getLastName());
}

@Test
public void getAverageAgeOfUsers(){
    List<User> users = userStub.getDummyUsersWithAllPrivileges();
    assertEquals(38, userService.getAverageAgeForUsers(users));
}
```

Both the Junits, is dependent on the *Stub *class method to create the dataset, which is further used for the testing.

> Major Disadvantages Using Stub is high maintenance.

For every method added, a list of dataset that can be created for the Stub need to be handled, which increases the complexity when the application grows in size.

So, instead of using Stubs, we will be focusing on *Mock *objects now.

### **How to write Junits with Mocks**


**Creation of Mock Object**

As stated above there are two way to instantiate the Mock object.
* by directly calling the *Mockito.mock()* method
* by calling *@Mock* annotations.

When using Mock annotation, it is mandatory to call *MockitoAnnotations.openMocks()* to initialize the mock objects. *MockitoAnnotations.openMocks()* initializes fields annotated with Mockito annotations. It also
* Allows shorthand creation of objects required for testing.
* Minimizes repetitive mock creation code.
* Makes the test class more readable.
* Makes the verification error easier to read because field name is used to identify the mock.

But, there is an integration change when working with Junit 5. In Junit 4, there was *@RunWith* annotation, which will take the *MockitoJunitRunner.StringStub.class* and instantiate the mock object with its value.

Now the *@RunWith* annotation is removed in Junit 5 and therefore cannot be integrated like above. Instead, Junit 5 has more powerful *@ExtendWith* annotation, which will take the *MockitoExtension.class* that comes as part of *mockito-junit-jupiter* dependency.

```java
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>4.4.0</version>
    <scope>test</scope>
</dependency>
```

It is not mandatory to using *@ExtendWith*, instead the *MockitoAnnotation.openMocks()* can be used to instantiate the mock object.

Now, we will try simple, precise and different flavors of Junits tests created using Mockito framework. ***TDD****(Test Driven Development) *approach can be achieved easily but since I reuse already written code, we will not use ***TDD ***here.

#### **When ... Then**

Enables stubbing methods. Think of this as `*when a method is called then do this`*.
e.g. *when doSomething() is called, then return String.*

We can implement this for our *sortAgeDescNameAsc()* method

```java
when( userService.sortByAgeDescAndNameAsc(new ArrayList<>()))
    .thenReturn(users);
```

This states when *sortByAgeDescAndNameAsc()* method is called with List as an argument, then it will return *List<User>*.

#### **Iterator Style Stubbing**

There will be scenarios where the method would return multiple values and we have to assert on each value it is returning.

This can be asserted by calling *thenReturn()* method multiple times. Every time it is called, it will move on to return the next value. It will behave something like *Iterator.next()* method.

We will implement Junit for the *getUpdateUserwithAgeHigherThan()* method from out previous blog post. Here if we have multiple values of the same age, it would return me different value on each *thenReturn()* call.

```java
List<User> users = Arrays.asList(
        new User(faker.number().randomNumber(),
                "Dynamically", faker.name().lastName(),
                faker.number().numberBetween(30, 100),
                Arrays.asList(Privilege.CREATE, Privilege.UPDATE)),
        new User(faker.number().randomNumber(),
                "Blunt-tech", faker.name().lastName(),
                faker.number().numberBetween(30, 100),
                Arrays.asList(Privilege.CREATE, Privilege.UPDATE, Privilege.READ)),
        new User(faker.number().randomNumber(),
                faker.name().firstName(), faker.name().lastName(),
                faker.number().numberBetween(1, 100),
                Arrays.asList(Privilege.READ))
);

when(userService.getUpdateUserWithAgeHigherThan(anyList(), anyInt()))
        .thenReturn(Optional.ofNullable(users.get(0)))
        .thenReturn(Optional.ofNullable(users.get(1)));
```

For the given list of Users, where *age=30* is for two User objects, *When..Then* will return 0th index element first and if called again, it will return 1st index value.

When we will do the assertion like this

```java
assertEquals("Dynamically",
        userService
           .getUpdateUserWithAgeHigherThan(Collections.emptyList(), 30)
           .get()
           .getFirstName());
           
assertEquals("Blunt-tech",
        userService
            .getUpdateUserWithAgeHigherThan(new ArrayList<>(), 30)
            .get()
            .getFirstName());
```

First assert statement will return *true *because *getUpdateUserWithAgeHigherThan()* will return 0th index value.

While the second assert statement will also return *true *again, because *getUpdateUserWithAgeHigherThan()* will return the value at the 1st index.


#### **Argument Matchers**

From the above example, notice that the method *getUpdateUserWithAgeHigherThan()* is called with two arguments which is *Mockito.anyXXX()*. This allows us to pass any dummy value to the matcher functions. Like here for the first argument, it would work even if a
* *Collections.emptyList()* is called, or
* *new ArrayList<>()* is called, or
* *new LinkedList<>()* is called etc.

#### **Handling Exceptions**

Lets suppose for arguments you are passing *null *and this would throw *NullPointerException *in future. So, we can handle these scenarios using *thenThrow()*.

If for the above method *getUpdateUserWithAgeHigher()* we pass *List<User>* as *null*, which should cause exception in the code implementation. We can write our Junit like this:

```java
when(userService.getUpdateUserWithAgeHigherThan(null, 30))
        .thenThrow(RuntimeException.class);
```

This assertion will return true only if the code is throwing *RuntimeException*. Lets say for this Junit, the code is not throwing *RuntimeException*, then the assertion will fail with the message passed as the third argument to *assertThrows()*.

```java
assertThrows(
        RuntimeException.class,
        () -> {userService.getUpdateUserWithAgeHigherThan(null, 30);},
        "Users list is empty. RuntimeException expected!!");
```

#### **BDD with Mockito**

*Behavior Driver Development* style of writing tests uses *given...when...then* design as fundamental part of the test methods. The following statement is from the Java Doc of Mockito.

> The problem with current stubbing api with canonical role of ***when**** *word does not integrate nicely with ***given...when...then**** *comments. It's because stubbing belongs to ***given**** *component of the test and not to the ***when**** *component of the test. Hence [*BDDMockito*](https://javadoc.io/static/org.mockito/mockito-core/3.3.3/org/mockito/BDDMockito.html)* *class introduces an alias so that you stub method calls with [*given(Object)*](https://javadoc.io/static/org.mockito/mockito-core/3.3.3/org/mockito/BDDMockito.html#given-T-) method. Now it really nicely integrates with the ***given**** *component of a BDD style test!

*BDDMockito *is imported to work on implementing a more natural order of test creation and execution. We will implement Junit test for *getMostFrequentLastName()* using the *BDDMockito*.

```java
given(userService.getMostFrequentLastName(anyList()))
    .willReturn(Optional.of(lastName));
```

Here, we are defining the behavior which is
* if given with the *getMostFrequentLastName()*
* then return *Optional *of the *lastName* string.

The *given...when....then* will looks like this

```java
// Defined Expected Behaviour
given(userService.getMostFrequentLastName(anyList())).willReturn(Optional.of(lastName));

// When method is called
// First Invocation
userService.getMostFrequentLastName(Collections.emptyList()).get();

// Then Verify, how many times it is called.
verify(userService, times(1)).getMostFrequentLastName(anyList());
```

#### **Verify**

Mockito provides verify method which identifies that *how many times/ never/ atleast/ atmost* the actual method is invoked. These are different flavors and will go through these one by one.

Let's take the above example, where we have *getMostFrequentLastName()* and will verify the number of times it was invoked/called using *times()* which takes expected number of times as argument.

```java
// Then Verify, how many times it is called.
verify(userService, times(1)).getMostFrequentLastName(anyList());
```

Here *times(1)* is the default value and can be omitted.

We can use the *atLeastonce()* or* atMostOnce()* method also, because it would identify that the method is invoked for at least 1 time or for at most 1 time respectively.

```java
// Returns true, as method is invoked at-least once.
verify(userService, atLeastOnce()).getMostFrequentLastName(anyList());

// Return true, as method is invoked max of 1 time.
verify(userService, atMostOnce()).getMostFrequentLastName(anyList());
```

Similarly, we can use *atLeast(n)* or *atMost(n)*, which takes how many times it was expected to be invoked.

```java
// Second Invocation
userService.getMostFrequentLastName(anyList());

// Return true, as method is invoked at-least 2 times.
verify(userService, atLeast(2)).getMostFrequentLastName(anyList());
```

For this example, we have never called *getAverageAgeForUsers()*, and so it was never invoked, which can be asserted like this

```java
// Return true, as given method is never invoked.
verify(userService, never()).getAverageAgeForUsers(any());
```

#### **Void Return Type**

When working with methods which have *void *as return type, we can use the *doReturn()* method of Mockito. It would be something like

```java
doReturn("a", "b", "c").when(mockObj).doSomething()
```

This will return list of strings, when the *doSomething()* is called on the Mock object. The below statement is from the Java doc of Mockito.

> You can use *doThrow()*, *doAnswer()*, *doNothing()*, *doReturn()* and *doCallRealMethod()* in place of the corresponding call with when(), for any method. It is necessary when you
>  - stub void methods
>  - stub methods on spy objects
>  - stub the same method more than once, to change the behavior of a mock in the middle of a test.

There are other topics which include *spying *on the real objects, *mocking static, final, enums, lenient* etc.. but adding here will make this post like a mini book. This could be added as another post in future.

Once you have read about the above ways to create Junits, then it is advisable to refer to this [*JavaDoc*](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html#0.2) where everything that can be achieved using Mockito is listed with how to implement it. I would also recommend going through the [*Github *](https://github.com/ankitagrahari/Learn/tree/main/src/test/java/com/java8)example for the Mocks and try to create as many testcases in your project. It will help in knowing your code better and implementing different features with ease testing all dependent features.

Hope this will help you in your learning process. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.