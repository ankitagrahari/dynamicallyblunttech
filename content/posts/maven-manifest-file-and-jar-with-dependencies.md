---
title: "Maven - Manifest file and Jar with Dependencies"
date: 2026-10-27T08:14:12+05:30
draft: false
featureImage: "images/df024c_bddbb63a21c24fd8a343882d412e38f9.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post, we will build a simple maven project which will create two jar files, which can be executed using below command 

```java
java -jar sample.jar <arguments space separated>
```

In maven, there is plugin called *maven-assembly-plugin, *which will assemble the dependencies and package it into a jar file, provided packaging as jar is given in the maven pom.xml file.


So, first and foremost thing is to have packaging given as jar like this 

```java
<groupId>com</groupId>
<artifactId>mavenManifestJarDep</artifactId>
<version>1.0-SNAPSHOT</version>
<packaging>jar</packaging>
```

Now in the build section, add the maven-assembly-plugin like this

```java
<plugin>
  <artifactId>maven-assembly-plugin</artifactId>
  <executions>
    <execution>
      <phase>package</phase>
      <goals>
        <goal>single</goal>
      </goals>
    </execution>
  </executions>
  <configuration>
    <archive>
      <manifest>
        <addClasspath>true</addClasspath>
        <classpathPrefix>lib/</classpathPrefix>
        <mainClass>com.Main</mainClass>
      </manifest>
    </archive>
    <descriptorRefs>
      <descriptorRef>jar-with-dependencies</descriptorRef>
    </descriptorRefs>
  </configuration>
</plugin>
```

This will create a manifest file in your jar file with the Main class given as *com.Main* and will create a new jar file with jar-with-dependencies as suffix. This new jar will have more size as compared to the normal jar file, because if your project happens to have any dependencies, it will be included into this jar file.

Now you can run the

```java
java -jar mavenManifestJarDep-1.0-SNAPSHOT.jar <arguments space separated>
```

You can refer this on [Github Link](https://github.com/ankitagrahari/mavenManifestJarDep) for the sample pom.xml file and the target directory for the jar files and their sizes.
* mavenMainfestJarDep-1.0-SNAPSHOT.jar, &
* mavenMainfestJarDep-1.0-SNAPSHOT-jar-with-dependencies.jar

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.