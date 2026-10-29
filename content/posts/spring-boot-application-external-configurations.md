---
title: "Spring Boot Application External Configurations"
date: 2026-10-27T08:14:21+05:30
draft: false
featureImage: "images/df024c_09d10c65f576482b8dcc2642c0985e30.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

Spring boot application provides a quick and elegant way to create REST API's with minimal boiler plate code and resolves any dependency that is present in the *classpath*.

In this plethora of new technologies era, it is evident that your spring boot application can have multiple configuration files which is configured, to be used by different parts of your code. 

For example the database specific configuration can go in a different location which more secure, while an environment specific configuration is kept in a different configuration file. Its more on how the design and implementation goes. 

In this blog post, we will focus on ***different ways to read configuration files*** in a spring boot application. Lets start by creating a sample spring boot application using [*Spring initializer*](https://start.spring.io/) with Spring Web and Lombok as dependencies. We will create a sample Rest controller which will read some configurable properties from the properties file. 

### **Default Configuration**

Whenever we create a spring boot application, under the */src/main/resources* directory, you can find an *application.properties* file, which is the default configuration file for your spring boot application. You would specify any number of parameters as key value pairs, which can be read by your code as per necessary. 

This is the ***default ***configuration file which spring boot automatically can finds it in the 
* *classpath root *or
* under *classpath config package*.

It can also look 
* under current directory or
* child of current directory or
* child of child of current directory

to find files of *application.properties* or the *application.yaml* type.

We can guide spring boot to look for the default configuration file in some other directory as well using *@PropertySource* annotation, which we will look in some time. 

There are different ways to pass the configurable values to your project other than the default configuration file. 

### **@Value annotation**

##### **How To**

This is more real world scenarios to extract key value pairs from the configuration file. It can be used with the parameters we want in the configuration file like this

```java
@Value("${app.config.name}")
private String appConfigName;
```

Here the *app.config.name* parameter is injected in the *appConfigName *String variable. 

Also, this brings to one important thing is @Value annotation accepts only String value which further can be casted to other datatype by Spring.

> *@Value* annotation can get environment variables or system variables or configurable variables defined in some configuration (**.properties or *.yaml or *yml*) files.

##### **Default Value**

We can give a default value with @Value annotation like this:

```java
@Value("${app.config.name:DBTConfigReader}")
private String appConfigName;
```

This is to handle scenarios where the [*app.config.name*](app.config.name) is not found in the configuration files, then it will default it to "DBTConfigReader".

##### **SpEL**

We can use *spring expression language* to refer to a list of values or map and do some manipulations on it. 

Get the entire properties file using:

```java
@Value("#{systemProperties}")
private Map<String, String> properties;
```

or can get any specific parameter:

in case of Map, it is like doing a get on the map's key:

```java
@Value("#{systemProperties['app.config.group.map']}")
private Map<String, String> appConfigGroupMap;
```

in case of List, we could use something like this:

```java
@Value("#{'${app.config}'.split(',')}")
private List<String> appConfigs;
```

even with the case where we have to get Map<List>, for entries where parameter has values separated by delimiter like comma, we can use following:

```java
@Value("#{${app.config.entries}}")
private Map<String, List<String>> entries;
```

### From Environment

Spring core framework provides another way to read configuration values using Environment interface based on the profile which is selected.

Here we are going to use the *@PropertySource* to explicitly tell Spring that when this configuration is loaded, the configuration parameters needs to be accessed from the given configuration files present in the *classpath*. We can *autowire* the Environment interface which will injected with the object during the runtime by Spring.

```java
import com.dbt.appconfreader.entity.AppConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

@Configuration
@PropertySource("classpath:env.properties")
public class EnvConfigReader {

    @Autowired
    private Environment env;

    public AppConfig appConfig(){
        AppConfig obj = new AppConfig();
        obj.setKey("system.name");
        obj.setValue(env.getProperty("system.name"));
        obj.setMessage("JavaHome:"+ env.getProperty("java.home"));
        return obj;
    }
}
```

You will notice if you run this class, that the value for *JavaHome *will be from the environment variable set and not from the configuration files.

***NOTE****: Make sure that the property key is not duplicated from the default configuration properties file, else the default will take the precedence. *

### **From Beans**

> Spring Boot provides an alternative method of working with properties that allows strongly typed beans to govern and validate the configuration of your application.

For the specific properties file like

```java
server.port=8798
app.config.profile=DEV
app.config.name=dev-DynamicallyBluntTech
app.config.type=dev-TechBlog
app.config.entry=DEV Application Configuration Reader
```

create a bean out of it, which can be injected when necessary. 

```java
import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "app.config")
@PropertySource("classpath:dev.properties")
public class DevProperties {
    
    private String name;
    private String profile;
    private String type;
    private String entry;
}
```

For nested level values, we can create public static class that can be populated with the nested level of property name. For the following sample properties file:

```java
server.port=8798
app.config.profile=DEV
app.config.name=dev-DynamicallyBluntTech
app.config.type=dev-TechBlog
app.config.entry=DEV Application Configuration Reader
app.config.classA.name=A-DBT_Nested
app.config.classA.type=A-nested
app.config.classA.value=A-IN-USE
app.config.classB.name=B-DBT_Nested
app.config.classB.type=B-nested
app.config.classB.value=B-IN-USE
```

We can observe that the nested level is there on the *app.config.classA* and *app.config.classB*

for which we can create the Bean as this:

```java
@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "app.config")
@PropertySource("classpath:dev.properties")
public class DevProperties {
    
    private String name;
    private String profile;
    private String type;
    private String entry;
    private ClassA classA;
    private ClassB classB;

    @Getter
    @Setter
    public static class ClassA{
        private String name;
        private String type;
        private String value;
    }

    @Getter
    @Setter
    public static class ClassB{
        private String name;
        private String type;
        private String value;
    }
}
```

This will get the values injected under each nested level properly.

We were mostly talking about reading property files till now, but lets see reading the *yaml *files instead if properties file.

### **From YAML configuration**

When using the *@Value* annotation, we don't have to change anything here and can get the values present as part of the configuration files. Same is the case with *Environment *interface.

The problem comes with *@PropertySource*, which cannot read *YAML *configuration files. So, in order to find something to make it work with, we can utilize the Spring *YamlPropertySourceLoader *which load the *.yml* or *.yaml* files into the *PropertySource *abstract class.

```java
@Bean
public static YamlPropertySourceLoader propertyYamlConfigInDev() {
    return new YamlPropertySourceLoader();
}
```

We also have to define the *YAML *factory which will take the **.yml* or **.yaml* files and convert to the property files to read the configuration parameters.

So, now we have the factory class, which takes the *yaml *and convert to *PropertySource *object like this

```java
public class YamlSourceFactory implements PropertySourceFactory {

    @Override
    public PropertySource<?> createPropertySource(
        String name, EncodedResource resource) {
        YamlPropertiesFactoryBean factoryBean = new YamlPropertiesFactoryBean();
        factoryBean.setResources(resource.getResource());
        Properties properties = factoryBean.getObject();
        return new PropertiesPropertySource(
            resource.getResource().getFilename(), properties);
    }
}
```

And the configuration class will look like this:

```java
@Getter
@Configuration
@PropertySource(value = "classpath:diff.yaml", factory = YamlSourceFactory.class)
public class YamlConfigReader {

    @Value("${app.config.name:DBTConfigReader}")
    private String appConfigName;
    
    @Value("${app.config.type}")
    private String appConfigType;

    @Bean
    public static YamlPropertySourceLoader propertyYamlConfigInDev() {
        return new YamlPropertySourceLoader();
    }
}
```

And this concludes all the ways to read the configuration files in Spring boot application. You can find all the code base on my [*Github *](https://github.com/ankitagrahari/AppConfReader)link.

### **References:**
* [*https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config*](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)

Hope this will help you in your learning process. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.