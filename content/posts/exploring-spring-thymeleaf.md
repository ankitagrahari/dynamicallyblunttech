---
title: "Exploring Spring Thymeleaf"
date: 2026-10-27T08:14:23+05:30
draft: false
featureImage: "images/df024c_bed0012116914ff9bc094cf4412257f7.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

In this post we will be creating a registration form which will include textbox, dropdown with multi-select option, file pickers and then bind it with backend REST services which can be further stored in some database or can be used for any other purpose.

## **Thymeleaf**

As stated in official [*Thymeleaf website*](https://www.thymeleaf.org/),

> **Thymeleaf** is a modern server-side Java template engine for both web and standalone environments.

Spring can be integrated with Thymeleaf to process or parse HTML, CSS, JS, XML, code. It becomes very simple to create an UI for your application in very little time. Thymeleaf can be used for modern day HTML5 web development as well.

Based on the requirement of dependencies, if you want to start a project with Spring and Thymeleaf, thymeleaf can be selected as dependency with others to give the basic template to start with from [https://start.spring.io/](https://start.spring.io/). 

## **Registration Form**

The form would look something like this:

The elements are random textboxes to store either name, version, descriptions, return type or platform type etc.

We will be checking following:

The description section which is storing a nested class, where the default, detailed, audit, remediate description variables are part of nested class,

The Supported platform is a list of variables displayed as drop down where user can select multiple values.

Similarly Scripts, Evaluate and Remediate Arguments will be a dynamic table where user can add or remove row.

Adding multiple file chooser support in the same form.

## **Create Spring Project from Spring Initializer**

### **Dependencies**

We will using lombok to have clean code without any of the boilerplate code and thymeleaf support.

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>
```

### **Create Java Object for Registration Form **

The POJO will have the elements that we want as part of the form like the ones displayed in the form. This POJO class will be binded with the form and the elements or attributes of the POJO can be referenced in the HTML form by their name, either by ****{}*** or ***${}.***

The registration form will look like this:

```java
@Data
public class Controls {
    private String name;
    private String version;
    private String guid;
    private Description description;
    private String returnType;
    private String platformType;
    private SupportedPlatforms[] platformSupported;
    private String[] imports;
    private List<Script> scripts;
    private MultipartFile ePyFile;
    private MultipartFile rPyFile;
    private List<EArgument> eArguments;
    private List<RArgument> rArguments
}
```

You will notice that using lombok eliminates developer to write all the getter, setter and the constructors. The annotation ***@Data*** takes care of these elements in the POJO.

### **Create Form**

We will start by creating a form which will be calling the REST API to save controls.

Lets say the URL to save the registration form is /saveControls, then code to add the form will look like this:

```java
<form action="#" th:action="@{/saveControls}" th:object="${controls}" method="post" enctype="multipart/form-data" >
```

Here the ***action ***attribute will letting us know that the REST API can be called from this URL, which will be mapped to some method is some controller.

Similarly, ***object*** attribute of form is mapped to the Form object in java. In our case it is the POJO which we created above *Controls.java.*

The form will use the ***post method*** and pass this form as the payload and since the form is having files to be attached to the payload we will be using multipart/form-data as our ***encode type***.

### **Create Textbox with Label**

Lets take an example of the name field, 

```java
<div class="form-group" th:align="left">
    <label style="font-weight: bolder" for="name">Name:</label>
    <input type="text" class="form-control" id="name" th:field="*{name}" required>
    <p class="alert alert-danger" th:if="${#fields.hasErrors('name')}" th:errors="*{name}">
</div>
```

The input label can be added using <label> html tag and the textbox can be added using input tag where type is defined as text. In the input tag, notice that the field tag is added which has name variable used. This name variable is mapped to the POJO Controls.java attribute name.

Similarly, we can add other textbox and its label.

### **Using Nested Class to display field variable**

There is a very high chance you will encounter this scenario where the Parent class is using child class which might be using another child class. Like in this example where Controls is using Description class which is mapped in the form using attribute defined in the Parent and accessing the attributes in the child by calling dot on the child attribute like this

```java
<label style="font-weight: bold" for="description.defaultDescription">Default Description:</label>
<input type="text" class="form-control" id="defaultDescription" th:field="*{description.defaultDescription}">
```

If you check the field attribute, it is calling the attribute defined in the parent class ***description ***and accessing the child attributes by calling ***description.defaullDescription***.

### **Create Drop Down **

The drop down requires a list of records which can be viewed in the drop down. The list can be dynamic or can be static which remains same. Like the ***Choose Platform Type*** variable, the number of records remains same and will be updated if RHEL introduce a new version or Windows comes up with a new version of it.

```java
<div class="form-group" th:align="left">
    <label style="font-weight: bolder" for="platformSupported">Choose Supported Platform</label>
    <select class="custom-select " th:field="*{platformSupported}" id="platformSupported" multiple required>
        <option value="">Nothing selected</option>
        <option th:each="platformSupported : ${T(com.dynamicallyblunt.tech.thymeleafform.beans.SupportedPlatforms).values()}"
                th:value="${platformSupported}"
                th:text="${platformSupported}">platformSupported
        </option>
    </select>
</div>
```

The select and option tag is used for the drop down. In this example we have used an ENUM to store the list of platforms. Also notice the multiple keyword used, which will allow the user to select multiple values. For storing multiple values, we are using an array of SupportedPlatforms POJO. 

The enum can be defined like this for different platforms:

```java
public enum SupportedPlatforms {
    Unix,
    RHEL5,
    RHEL6,
    RHEL7,
    Centos6,
    Centos7,
    Centos8,
    Windows,
    Win2008,
    Win2k2008,
    Win2012,
    Win2k2012
}
```

### **Create File Picker**

The HTML tag to choose file is same as text, which is input tag. The input tag will use the type as file. In our example we are using bootstrap 4 which will make the button looks fancier. You can refer to the bootstrap v4 examples [here](https://getbootstrap.com/docs/4.0/components/forms/). 

It will look like this 

```java
<div class="custom-file">
    <label style="font-weight: bold" for="chooseFile" class="custom-file-label">Choose Code file</label>
    <input type="file" name="file" th:field="*{epyFile}" class="custom-file-input">
</div>
```

### **Create Dynamic Table**

In this case, we will be creating a table in which once the user clicks on Add Row, we will be adding a new row for user to type in new records. Also we will provide one remove button which will delete that entry when it is clicked by user.

On click of the ***AddRow***, we will submit the form with the parameter add row, which will call a different method in the controller. The purpose of this method will be to add a new object to the Control's Arguments attribute.

The html code will be like 

```java
<div class="form-group">
    <label style="font-weight: bolder" for="eArguments">EArguments</label>
    <button class="btn btn-info" th:nowrap="true" th:align="right" type="submit" name="addEArgs" id="addEArgs">Add EArguments</button>
</div>
<div th:if="*{eArguments}">
        <table cellpadding="5px 15px;">
            <thead>
            <tr>
                <th>Index</th>
                <th>Type</th>
                <th>Default Label</th>
                <th>Default Description</th>
                <th>Default Value</th>
                <th></th>
            </tr>
            </thead>
            <tbody>
            <tr th:each="eval, stat: *{eArguments}">
                <td th:text="${stat.count}">1</td>
                <td><input type="text" class="form-control" th:field="*{eArguments[__${stat.index}__].type}"></td>
                <td><input type="text" class="form-control" th:field="*{eArguments[__${stat.index}__].defaultLabel}"></td>
                <td><input type="text" class="form-control" th:field="*{eArguments[__${stat.index}__].defaultDescription}"></td>
                <td><input type="text" class="form-control" th:field="*{eArguments[__${stat.index}__].defaultValue}"></td>
                <td><button class="btn btn-info" type="submit" name="removeEArgs" id="removeEArgs" th:value="${stat.index}">Remove</button></td>
            </tr>
            </tbody>
        </table>
    </div>
</div>
```

Here in the html tag, we are iterating over the list of eArguments objects and also keeping the index of every element in the list. It will help us in the remove section. 

In the above section you can see the elements are iterated like *{eArguments[__${stat.index}__].type} where the *__${}__* is used instead of directly using *${}*. This is because in thymeleaf, the template will pre process the variable *__${}__*, so that the outer variable will get the index instead of getting the variable. So something like first the *__${}__* is calculated and the value is kept into the outer variable, which will look like this *{eArguments[0}__].type} 

We will create a new method in the controller which will get triggered when the Add Row is triggered and it will add a new empty row for user to key in their inputs.

```java
@PostMapping(value = "/saveControls", params = {"addEArgs"})
public String addEArgument(Controls controls, BindingResult bindingResult){
    if(null!=controls){
        if(null==controls.getEArguments()){
            List<EArgument> evArgList = new ArrayList<>();
            evArgList.add(new EArgument());
            controls.setEArguments(evArgList);
        } else {
            controls.getEArguments().add(new EArgument());
        }
    }
    return "registration";
}
```

Similarly for remove method, it will call the same API but with removeEArgs parameters like this:

```java
@PostMapping(value = "/saveControls", params = {"removeEArgs"})
public String removeEArgument(Controls controls, BindingResult bindingResult, HttpServletRequest request){
    controls.getEArguments().remove(Integer.parseInt(request.getParameter("removeEArgs")));
    return "registration";
}
```

We are getting the index by calling the ***request.getParameter(String s)*** method. Since the entire eArgs is a list, on removal it will remove that index element from the list using ***remove()*** method

Using the same approach we can add any number of dynamic table where user can add and edit the rows or remove rows from the list.

We will conclude now on the thymeleaf, but from here, we can create any form and do the binding with the POJO for any number of elements. You can find the complete codebase of this tutorials in this [Github ](https://github.com/ankitagrahari/thymeleafForm)reporsitory..

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.

### References

[https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.pdf](https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.pdf)