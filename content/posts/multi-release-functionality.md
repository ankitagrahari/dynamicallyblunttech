---
title: "Multi Release Functionality"
date: 2026-10-27T08:14:25+05:30
draft: false
featureImage: "images/df024c_efbee9350c91464e93e38fafbaca86fb.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will explore one of the best feature provided by Java 9, its importance in present day development and how it will be a key in maintaining multiple version of code.

When Java 9 released in July, 2017, it was not a Long term Support(LTS), though it was having multiple features which would help Java in long run. Some of it which is now playing a big role are 
* Multi-Release Jar functionality,
* Introduction of reactive streams,
* Private methods in Interface,
* Deprecations of JavaFX, which is finally removed in Java 11 and maintained as a different project out of JDK umbrella,
* Modularity, which is on same concept as Microservices.

Since this release was not a Long Term Support (LTS), Oracle came up with another release Java 10 and soon a LTS version Java 11.

At the time of writing this post, Oracle is advertising Java 19 (non-LTS) which is released in 2022. GA is in September, 2022. 

### **Importance**

Now lets say we have our project written in Java 7, which was upgraded to Java 8 and then to the next LTS version which is Java 11. To perform these upgrades, developers took a long time as it is not just JDK upgrade, but all dependencies need to be made compatible. If some dependencies are not working, then look for their latest release or other alternatives which again involves other code changes. So upgrading to the latest is not an easy task and that's why the estimation is also big.

Since the bytecode version varies with each release, developers have to maintain the functionality and if there is a big release jump, like upgrading directly from Java 8 to Java 17 (LTS), it will bring a lot of changes which also brings load of maintaining the dependencies changes as well.

To help with this issue, Java 9 introduced multi-release functionality, which helps in maintaining Java code of different versions. This way the files changed as part of upgrade process, can be kept in another directory which will be picked by complier based on the version of Java it is running. 

Lets go through an example using maven as build tool to create a project which is originally written in Java 8 and then was upgraded to Java 11 (multi-release).

### **Example**

This will be a very simple example where we are maintaining two codebase for the files that need change and will have the respective methods present, such that if this class is run by an incompatible version of Java, it would throw errors. 

The project structure will be like this:

Lets create our Main class, where we will create an instance of Worker class. Assuming this worker class is the code that will be changed in the upgrade process, we will maintain another directory for Java 11 Worker class file.

#### **Main Class**

```java
public static void main(String[] args) {

    Worker worker = new Worker();
    if(!worker.isNameBlank())
        System.out.println(worker.getName()+"---"+worker.getVersion());
    else
        System.out.println("Name is Blank");

}
```

#### **Java 8 Worker class**

This class is written with Functional Interface annotation specific to Java 8. Also some print statements which will identify it is coming from Worker.java complied and executed with Java 8.

```java
@FunctionalInterface
interface FunctionOne{
    int addTwoNum(int a, int b);
}

public class Worker {

    private int version = 8;
    private String name = "Worker8";

    public boolean isNameBlank(){
        FunctionOne total = (a, b) -> a+b;
        System.out.println("Sum of 10, 20 is ="+ total.addTwoNum(10, 20));
        return this.name == null || this.name.trim().isEmpty();
    }

    public String getName(){
        return this.name;
    }

    public int getVersion(){
        return this.version;
    }
}
```

#### **Java 11 Worker Class**

Notice that in this class, we have used isBlank() and stripLeading() methods introduced in Java 11.

```java
public class Worker {

    private int version = 11;
    private String name = "Worker11";

    public boolean isNameBlank(){
        return this.name.isBlank();
    }

    public String getName(){
        return this.name.stripLeading();
    }

    public int getVersion(){
        return this.version;
    }
}
```

##### **POM.xml**

Since I am using Maven as the build tool, I will add the configurations which tells the complier while compiling/building which Java class to pick.

**1. Set the Source and Target Complier version**

```java
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
</properties>
```

**2. Add the maven-complier plugin**, which will have two executions ways, one for Java 8 and another for Java11.

**3. Add execution for Java 8**

```java
<execution>
    <id>java8</id>
    <goals><goal>compile</goal></goals>
    <configuration>
        <source>1.8</source>
        <target>1.8</target>
    </configuration>
</execution>
```

**4. Add execution for Java 11 **

Notice here that we are specifically telling complier that the source class is present in which directory for Java 11, and also letting it know that Multi-Release output is set to True.

```java
<execution>
    <id>java11</id>
    <goals><goal>compile</goal></goals>
    <configuration>
        <release>11</release>
        <compileSourceRoots>${project.basedir}/src/main/java11</compileSourceRoots>
        <multiReleaseOutput>true</multiReleaseOutput>
    </configuration>
</execution>
```

**5. Adding Maven-Jar Plugin** to create a manifest file which will have the Main class to start the execution.

Once the pom.xml is properly set, do a *maven clean install* to build the project. This will create a target directory which will have the final jar file.

Now when executing using Java 8, it will give following output:

While executing using Java 11, it will give the following output

If you open the Jar file, you will find the following structure:

Notice that the version specific code is present under the ***META-INF/versions*** directory.

You can refer to my [*Github Repository*](https://github.com/ankitagrahari/MultiRelease) for the full code base and unzipped jar file as well.

Hope this helps others also. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.