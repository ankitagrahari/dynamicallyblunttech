---
title: "Spring Data JPA with MongoDB"
date: 2026-10-27T08:14:17+05:30
draft: false
featureImage: "images/df024c_bc378f880a5e4dea9d61c68fdcdf418a.jpg"
tags: ['[]']
categories: ['["619c9d9d8da2c200166cb558"]']
showReadingTime: true
---

In this post we will create a simple Spring JPA project which will connect to MongoDB and create a document, where we will save records and then will try to fetch those records using JPA repository built in methods. 

In this post we will try performing all CRUD Operation on MongoDB Using JSON queries in Spring Data JPA 

## **Project Structure**

We will create Employee repository which will store the Employee models, and will create Test cases to fetch data based on JSON queries from MongoDB on my local.

### **Dependencies**

We will be using *lombok *and *spring starter mongodb* to start with.

```java
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

### **Configuration**

The application properties will have the spring data attributes which will tell the spring project about the hostname, port, username, password, database etc. We can define like this

```java
server.port=8768
spring.data.mongodb.uri= mongodb://127.0.0.1:27017/employees
spring.data.mongodb.database=employees
spring.data.mongodb.repositories.enabled=true

#spring.data.mongodb.authentication-database= # Authentication database name.
#spring.data.mongodb.database=test # Database name.
#spring.data.mongodb.field-naming-strategy= # Fully qualified name of the FieldNamingStrategy to use.
#spring.data.mongodb.grid-fs-database= # GridFS database name.
#spring.data.mongodb.host=localhost # Mongo server host.
#spring.data.mongodb.password= # Login password of the mongo server.
#spring.data.mongodb.port=27017 # Mongo server port.
#spring.data.mongodb.repositories.enabled=true # Enable Mongo repositories.
#spring.data.mongodb.uri=mongodb://localhost/test # Mongo database URI. When set, host and port are ignored.
#spring.data.mongodb.username= # Login user of the mongo server.
```

You can refer to other commented spring data monogDB parameters which can be changed during the development cycle.

### **Model**

This is the *Employee *model which will have name, address, and experience attributes.

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
@Document(collection = "employee")
public class Employee {

//    @Id
//    private String id;
    private String name;
    private String address;
    private Integer experience;
}
```

Here, we can add the document collection name (~table) using the *@Document* annotation. By default, if the *@Document* is not given, it will map it to the class name. It will also create the employee document in MongoDB if it is not present.

After the data insertion in DB, it will look like this 

Notice that the id column is commented, but while storing to the MongoDB, it will add the *_id* field. Also, since we are using lombok, we don't have to write the boiler-plate code because lombok, will automatically add the getters and setter methods. Also we have asked to add all argument and no argument constructors.

### **Repository**

The *Employee *repository will extends *MongoRepository *class where we can define the key and value's data type. It also will have all the built-in methods and include any custom queries which we want to fetch data with.

#### **Fetch Data *****byName***

The employee repository will fetch data of employees by name attributes using this field

```java
@Query("{name:'?0'}")
List<Employee> findEmployeeByName(String name);
```

We can also skip the @Query annotation.

#### **Fetch Data byName using Regex**

We can fetch data of employees by giving a substring of the name. Like using regex we can get data whose name contains the specific string.

```java
@Query("{ 'name' : { $regex: ?0 } }")
List<Employee> findEmployeeByRegexpName(String regexp);
```

#### **Fetch Data *****byExperience***

We can fetch employees whose experience is equals to a certain number, like this

```java
@Query(value = "{experience:'?0'}", fields = "{'name':1, 'address':1}")
List<Employee> findEmployeeByExperienceEquals(int exp);
```

#### **Fetch Data *****byExperience *****using custom query**

We can fetch employees whose experience is between a set of numbers, like this

```java
@Query("{'experience': { $gt: ?0, $lt: ?1 } }")
List<Employee> findEmployeesByExperienceBetween(int start, int end);
```

## **Unit Testing**

As part of unit testing our spring boot project, we can use the @SpringBootTest annotation and add the Junit @Test or @BeforeAll or @BeforeEach, @After, @AfterEach annotations to create a test class, or to run certain methods before each or after each test case run.

We will setup by creating few Employee records and insert into the MongoDB. 

```java
@BeforeEach
void setUp(){
    //Remove everything from Employee table
    employeeRepo.deleteAll();

    //Insert new Employee data
    Employee employee = new Employee("dynamically", "Amsterdam", 9);
    Employee employee1 = new Employee("blunt", "India", 5);
    Employee employee2 = new Employee("tech", "Germany", 6);
    Employee employee3 = new Employee("Subscribe", "Austin", 9);

    empList.add(employee); empList.add(employee1); empList.add(employee2); empList.add(employee3);
    employeeRepo.saveAll(empList);

    System.out.println("Employees data saved");
}
```

This method will run before every test case run, so that the new Junit will work on separate and new dataset. 

We will add other test cases to run different test cases.

```java
@Test
void fetchDataByName(){
    List<Employee> employees = employeeRepo.findEmployeeByName("tech");
    Assertions.assertEquals("tech", employees.get(0).getName());
}

@Test
void fetchDataByNamePart(){
    List<Employee> employees = employeeRepo.findEmployeeByRegexpName("c");
    Assertions.assertEquals(
            empList.stream().filter(emp -> emp.getName().contains("c")).count(),
            employees.size()
    );
}
```

The above test case will have fetch data by Name as defined above.

Similarly, we can define other test cases which will call the methods to fetch data based on experience attributes.

```java
@Test
void fetchDataByExp(){
    List<Employee> employees = employeeRepo.findEmployeeByExperienceEquals(9);
    Assertions.assertEquals(
            empList.stream().filter(emp -> emp.getExperience().equals(9)).count(),
            employees.size()
    );
}

@Test
void fetchDataByExpBetweenFiveAndTen(){
    List<Employee> employees = employeeRepo.findEmployeesByExperienceBetween(6, 10);
    Assertions.assertEquals(
            empList.stream().filter(emp -> emp.getExperience()>6 && emp.getExperience()<10).count(),
            employees.size()
    );
}
```

You might face an exception if the @Query annotation is not properly constructued.

*org.bson.BsonInvalidOperationException: readStartDocument can only be called when CurrentBSONType is DOCUMENT, not when CurrentBSONType is STRING.*

This will conclude the creation, fetching and deletion of data using Spring Data JPA and MongoDB. You can find the entire codebase in my [*Github repository*](https://github.com/ankitagrahari/MongoDBJPA).

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.