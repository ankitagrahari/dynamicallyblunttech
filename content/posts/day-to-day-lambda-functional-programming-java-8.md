---
title: "Day to Day Lambda & Functional Programming in Java 8"
date: 2026-10-27T08:14:12+05:30
draft: false
featureImage: "images/df024c_4c93affe98db4da7897808708a5f1a3c.jpg"
tags: ['[]']
categories: ['["6249579158f0bd10b2a57273"]']
showReadingTime: true
---

If you have seen lately, everyone has shifted to Java 8 and is more or less trying to move from lengthy code blocks to few lines/precise use of Lambda and Functional Programming introduced in Java 8. So, we will talk about all day to day operations that can be converted to use lambda or functional programming and make our code precise and simple.

This post will be a bit lengthy where we will write *Junit5* tests and the code for every scenario. It will be interesting to know, as these days, a lot of companies are focusing on candidates to know the use of lambda expressions at least.

Lets start considering we have a User object which has its attributes like *firstName*, *lastName*, *age *and a set of *Privileges*. The Privileges is an *enum*, which defines all privileges a user can have, like Read, Create, Update, Delete.

So my User and Privilege class looks like this:

**User.java**

```java
public class User {

    private Long id;
    private String firstName;
    private String lastName;
    private Integer age;
    private List<Privilege> privileges;

    public User(final Long id,
                final String firstName,
                final String lastName,
                final Integer age,
                final List<Privilege> privileges) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.privileges = Collections.unmodifiableList(privileges);
    }
    .
    .
    //getters and setters for its attributes
    .
    .
    @Override
    public String toString(){
        return this.id+"_"
            + this.firstName + "_" + this.lastName
            + "_" + this.age + "_("
            + ((this.privileges.size()==4)
                ? "All"
                : this.privileges.stream()
                        .map(String::valueOf)
                        .collect(Collectors.joining(","))
            )
            + ")";
    }
}
```

**Privilege.java**

```java
public enum Privilege {
    CREATE,
    UPDATE,
    READ,
    DELETE
}
```

The User class does not override *hashcode *and *equals *method.

Lets start with each scenario one by one.

## **Scenarios**

### **1. Sort** By Name in Ascending and Age in Descending Order

We need to sort the list of users

by first name, then

by last name, and then

by age in reverse order.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Sort Users by Name in ascending and then by Age in descending order")
void sortByAgeDescAndNameAsc() {
    final User user1 = new User(1L, "John", "Doe", 26, 
            ALL_PRIVILEGES);
    final User user2 = new User(2L, "Greg", "Smith", 30, 
            ALL_PRIVILEGES);
    final User user3 = new User(3L, "Alex", "Smith", 13, 
            ALL_PRIVILEGES);
    final User user4 = new User(4L, "Dynamic", "Blunt", 30, 
            Collections.singletonList(Privilege.READ));
    final User user5 = new User(5L, "Dynamic", "BluntTech", 30, 
            ALL_PRIVILEGES);

    final List<User> sortedUsers =
            userService.sortByAgeDescAndNameAsc(
                Arrays.asList(user1, user2, user3, user4, user5)
            );
    System.out.println(sortedUsers);
    Assertions.assertArrayEquals(
            sortedUsers.toArray(), 
            new User[]{ user4, user5, user2, user1, user3}
    );
}
```

We have 5 users, with 
* Greg and Alex user with same last name and different age
* Dynamic Blunt and Dynamic BluntTech user with same first name and age but different last name.

We are asserting and expecting the users to be in this order

```java
user4(Dynamic Blunt) --> user5(Dynamic BluntTech) --> user2(Greg) --> user1(John) --> user3(Alex)
```

#### Lets check the logic for this:

We need to use lambda expression to first sort it based on first name, then last name and then the age in reverse order. So we do what we say:

```java
@Override
public List<User> sortByAgeDescAndNameAsc(List<User> users) {
    return users.stream()
            .sorted(
                    Comparator.comparing(User::getFirstName)
                            .thenComparing(User::getLastName)
            )
            .peek(System.out::print)
            .sorted(
                    Comparator.comparingInt(User::getAge)
                            .reversed()
            )
            .peek(System.out::println)
            .collect(Collectors.toList());
}
```

On the stream of users, we are using *Comparator.comparing()* method to sort. We also have to tell on what basis it has to compare and for that we used Functional programming to get the first name (*getFirstName()*). Once we have compared on first name, then we have to compare on the last name, and for that we used *thenComparing()* method. 

> *peek()* takes Consumer as argument and we can use this to know the values from the previous lambda operation. Very useful in debugging.

Similarly, we can sort based on the age, but this time we will use *reversed()*, as we need the age to sorted in descending order.

And at last, we have the terminal operation, which will collect the sorted users in a *List*.

So the output on console will have the print statements from peek() and final list.

```java
3_Alex_Smith_13_(All)4_Dynamic_Blunt_30_(READ)5_Dynamic_BluntTech_30_(All)2_Greg_Smith_30_(All)1_John_Doe_26_(All)4_Dynamic_Blunt_30_(READ)
5_Dynamic_BluntTech_30_(All)
2_Greg_Smith_30_(All)
1_John_Doe_26_(All)
3_Alex_Smith_13_(All)
---------------------------------------------->>Above are from Peek()
[4_Dynamic_Blunt_30_(READ), 5_Dynamic_BluntTech_30_(All), 2_Greg_Smith_30_(All), 1_John_Doe_26_(All), 3_Alex_Smith_13_(All)]
```

### **2. Distinct **Privileges

We need to return all the distinct privileges which are part of the input list of User.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Return all distinct privilege in the list")
void getAllDistinctPrivileges() {
    final User createUser = new User(1L, "John", "Doe", 26,
            Collections.singletonList(Privilege.CREATE));
    final User updateUser = new User(2L, "Greg", "Smith", 30, 
            Collections.singletonList(Privilege.UPDATE));
    final User updateUser1 = new User(3L, "Greg", "Smith", 20, 
            Collections.singletonList(Privilege.UPDATE));
    final User deleteUser = new User(4L, "Alex", "Smith", 13,         
            Collections.singletonList(Privilege.DELETE));

    final List<Privilege> distinctPrivileges =
            userService.getAllDistinctPrivileges(
                    Arrays.asList(
                            createUser, 
                            updateUser, 
                            updateUser1, 
                            deleteUser
                    )
            );
            
    System.out.println(distinctPrivileges);
    
    Assertions.assertEquals(distinctPrivileges.size(), 3);
}
```

We have 4 users, which are having Create, Update and Delete as the distinct privileges and the output size will be the assertion criteria.

#### Lets look into the logic of how to get the *List<List<>>* to *List<>* using* flatMap()*.

```java
@Override
public List<Privilege> getAllDistinctPrivileges(List<User> users) {
    return users.stream()
            .map(user -> user.getPrivileges())
            .peek(System.out::print)
            .flatMap(List::stream)
            .distinct()
            .peek(System.out::println)
            .toList();
}
```

See, how precise and easy to understand this code looks. We are first getting the list of privileges for each user and then converting that List to Stream of Privilege. Doing a distinct() and converting to list will be our output. 

> More intuitive it will be, if you are using some editor, and properly separating it to new line after every lambda operation. I am using IntelliJ, and this is how it looks

You can refer the yellow marked ones, where the editor is displaying the return type of that operation. Like, 

*user.stream()* returns a *Stream<user> *

then applying *map()* on it, returns a *Stream<List<Privileges>>*

then applying *flatMap()* on it, will give me a *Stream<Privileges>*.

So, the output of this method will be:

```java
[CREATE]CREATE
[UPDATE]UPDATE
[UPDATE][DELETE]DELETE
---------------------------------------------->>Above are from peek()
[CREATE, UPDATE, DELETE]
```

### **3. Filter** User with Update Privilege and Age>29

We will be filtering the list of user with Update Privilege and Age greater than given input(29).

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Return User with higher age than X of Update Privilege")
void getUpdateUserWithAgeHigherThan() {
    final User updateUser = new User(1L, "John", "Doe", 26,
            Collections.singletonList(Privilege.UPDATE));
    final User updateUser1 = new User(2L, "Greg", "Smith", 30, 
            Collections.singletonList(Privilege.UPDATE));
    final User deleteUser = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    Optional<User> user = userService.getUpdateUserWithAgeHigherThan(
            Arrays.asList(updateUser1, updateUser, deleteUser),
            29
    );
    
    System.out.println(user.get());
    Assertions.assertEquals(user.get(), updateUser1);
}
```

I have 3 Users, of which 2 are having Update Privilege, and only one is having Age greater than 29. So my assertion criteria will be on that User.

#### Lets check the logic for this:

```java
@Override
public Optional<User> getUpdateUserWithAgeHigherThan(List<User> users, int age) {
    return users.stream()
            .filter(user -> 
                    user.getAge() > age 
                    && user.getPrivileges().contains(Privilege.UPDATE)
             )
            .peek(System.out::println)
            .findFirst();         //Can use both findFirst() or findAny()
}
```

If you notice, we are returning an *Option<User>* because, there might be a scenario where the given filter constraints never gets fulfilled, and in this scenario will return *Optional.empty*.

> Terminal operation like *findFirst()*, *findAny(), average() etc* return *Optional *object, which uses *isPresent()* to return false, if the return value is null, else true.

Output of this test is this

```java
2_Greg_Smith_30_(UPDATE)
---------------------------------------------->>Above are from peek()
2_Greg_Smith_30_(UPDATE)
```

### **4. Group** Users By Count of Privileges

We have to find the users who have either one Privilege, or two or three or all 4 Privilege.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Count of Users for each Privilege")
void groupByCountOfPrivileges() {
    final int ONE_PRIVILEGE = 1;
    final int TWO_PRIVILEGES = 2;
    final int FOUR_PRIVILEGES = 4;

    final User userWith2Privileges = new User(1L, "John", "Doe", 26,
             Arrays.asList(Privilege.UPDATE, Privilege.CREATE));
    final User userWith4Privileges = new User(2L, "Greg", "Smith", 30, 
            ALL_PRIVILEGES);
    final User userWith4Privileges1 = new User(2L, "Anton", "Smith", 34, 
            ALL_PRIVILEGES);
    final User userWith1Privileges1 = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));
    final User userWith1Privileges2 = new User(3L, "Neo", "Smith", 13, 
            Collections.singletonList(Privilege.UPDATE));

    Map<Integer, List<User>> privilegesCountUsersMap = userService
            .groupByCountOfPrivileges(
                    Arrays.asList(
                            userWith1Privileges1, 
                            userWith1Privileges2, 
                            userWith2Privileges, 
                            userWith4Privileges, 
                            userWith4Privileges1
                   )
    );
    
    System.out.println(privilegesCountUsersMap);

    Assertions.assertArrayEquals(
            new int[]{2, 1, 2},
            new int[]{
                    privilegesCountUsersMap.get(ONE_PRIVILEGE).size(),
                    privilegesCountUsersMap.get(TWO_PRIVILEGES).size(),
                    privilegesCountUsersMap.get(FOUR_PRIVILEGES).size()
            }
    );
}
```

So, we have 5 Users, which has either 1 or 2 or 3 Privileges. The method will be returning a Map of Count of Privileges and List of Users. My assertion criteria will be to look each element of map, and assert on the size of User list for each privilege.

#### Lets check the logic of this:

```java
@Override
public Map<Integer, List<User>> groupByCountOfPrivileges(List<User> users) {
    return users.stream()
            .collect(
                    Collectors.groupingBy(
                            user -> user.getPrivileges().size()
                    )
            );
}
```

We only have to group by the list of users based on the size of the Privileges each user has. And so we used *Collectors.groupingBy()* on the Privilege list size.

Output of the test is:

```java
{1=[3_Alex_Smith_13_(DELETE), 3_Neo_Smith_13_(UPDATE)], 
2=[1_John_Doe_26_(UPDATE,CREATE)], 
4=[2_Greg_Smith_30_(All), 2_Anton_Smith_34_(All)]}
```

### **5. Count** of Privileges for each User

We have to return the count of Privileges each user possess. This scenario is very similar to the above one, where we have to find the count of User for each Privilege.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Count of Privileges per User")
void countOfPrivilegesPerUser() {
    final User user1With2Privileges = new User(1L, "John", "Doe", 26,
             Arrays.asList(Privilege.UPDATE, Privilege.CREATE));
    final User user2With4Privileges = new User(2L, "Greg", "Smith", 30, 
            ALL_PRIVILEGES);
    final User user3With4Privileges = new User(2L, "Anton", "Smith", 34, 
            ALL_PRIVILEGES);
    final User user4With1Privilege = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));
    final User user5With1Privilege = new User(3L, "Neo", "Smith", 13, 
            Collections.singletonList(Privilege.UPDATE));

    Map<User, Integer> privilegesCountPerUserMap = userService
            .countOfPrivilegesPerUser(
                    Arrays.asList(
                            user4With1Privilege, 
                            user5With1Privilege, 
                            user1With2Privileges, 
                            user2With4Privileges, 
                            user3With4Privileges
                    )
    );

    System.out.println(privilegesCountPerUserMap);
    
    Assertions.assertArrayEquals(
            new int[]{2, 4, 4, 1, 1},
            new int[]{
                    privilegesCountPerUserMap.get(user1With2Privileges),
                    privilegesCountPerUserMap.get(user2With4Privileges),
                    privilegesCountPerUserMap.get(user3With4Privileges),
                    privilegesCountPerUserMap.get(user4With1Privilege),
                    privilegesCountPerUserMap.get(user5With1Privilege)
            }
    );
}
```

We have 5 users, which will have different privileges, and we have to assert on the Map returned by the method, which holds the count of Privilege each User has. Map is of User and the count of Privileges.

#### Lets check the logic to get this:

```java
@Override
public Map<User, Integer> countOfPrivilegesPerUser(List<User> users) {
    return users.stream()
            .collect(
                    Collectors.groupingBy(
                            user -> user,
                            Collectors.summingInt(
                                   value -> value.getPrivileges().size()
                            )
                    )
            );
}
```

We have the same logic applied as previous one, but this time, we are using *Collectors.summingInt()* method to define on what basis the *Collectors.groupingBy()* will group the users. 

Output of this test is:

```java
{
 3_Alex_Smith_13_(DELETE)=1, 
 2_Greg_Smith_30_(All)=4, 
 1_John_Doe_26_(UPDATE,CREATE)=2, 
 2_Anton_Smith_34_(All)=4, 
 3_Neo_Smith_13_(UPDATE)=1
}
```

### **6. Average** Age of Users

We have to return the average age of all the users. The return type should be *double*.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Return average age of Users")
void getAverageAgeForUsers() {
    final User createUser = new User(1L, "John", "Doe", 26,
            Collections.singletonList(Privilege.CREATE));
    final User updateUser = new User(2L, "Greg", "Smith", 30, 
            Collections.singletonList(Privilege.UPDATE));
    final User updateUser1 = new User(3L, "Greg", "Smith", 20, 
            Collections.singletonList(Privilege.UPDATE));
    final User deleteUser = new User(4L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    double averageAge = userService.getAverageAgeForUsers(
            Arrays.asList(createUser, updateUser, updateUser1, deleteUser)
    );

    System.out.println(averageAge);
    Assertions.assertEquals(averageAge, 22.25);
}
```

We have 4 Users, whose age is given and we need to assert on the average age of the users.

#### Lets check the logic of this:

```java
@Override
public double getAverageAgeForUsers(List<User> users) {
    return users.stream()
            .mapToDouble(User::getAge)
            .average()
            .getAsDouble();
}
```

We have mapped the User stream to its attributes *Age *and called the terminal operation average(), which will return an *Optional *object. To get the values from *Optional *object, we can use the *get()* method. Here, to get the double value, we have used *getAsDouble()*.

Output of the test is:

```java
22.25
```

### **7. Most Frequent** Last Name of Users

We have to find the Last name from the list of User, which has occurred most number of times in the list.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Return most frequent occurring last name from the list")
void getMostFrequentLastName() {
    final User createUser = new User(1L, "John", "Doe", 26, 
            Collections.singletonList(Privilege.CREATE));
    final User updateUser = new User(2L, "Greg", "Smith", 30,         
            Collections.singletonList(Privilege.UPDATE));
    final User updateUser1 = new User(3L, "Greg", "Smith", 20, 
            Collections.singletonList(Privilege.UPDATE));
    final User deleteUser = new User(4L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    String lastName = userService.getMostFrequentLastName(
            Arrays.asList(createUser, updateUser, updateUser1, deleteUser)
    ).get();

    System.out.println(lastName);
    Assertions.assertEquals(lastName, "Smith");
}
```

We have 4 Users, among which Smith is the last name for 3 Users. So our assertions criteria will also be the same.

#### Let check the logic for this:

A normal operation would be something like, getting the map of last name and the count of it. But we can do this in one line. 

```java
@Override
public Optional<String> getMostFrequentLastName(List<User> users) {
    Map<String, Long> map =
            users.stream()
                    .collect(Collectors.groupingBy(
                            User::getLastName,
                            Collectors.counting()
                    ));
    return Optional.of(
            map.entrySet()
                    .stream()
                    .max((e1, e2) -> e1.getValue()<e2.getValue()?-1:1)
                    .get()
                    .getKey()
    );
}
```

In the map, we have grouped the Users by Last Name and captured the count of the last name found in the list. Then from the Map, we have found the *max()* by passing the comparator logic  to get the highest count value first. Since max() is also a terminal operation, it will return Optional<Map> object. 

You can see the return type of each operation here:

Output is:

```java
Smith
```

**8. Filter** by Multiple Predicates

We are given with multiple filter constraints, and we have to apply all the filters in the same user Stream.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Filter Users by first name length > 3 and privileges > 2")
void filterBy() {
    final User user1 = new User(1L, "John", "Doe", 26, 
            Collections.singletonList(Privilege.UPDATE));
    final User user2 = new User(2L, "Greg", "Jonson", 30, 
            Arrays.asList(
                    Privilege.UPDATE, 
                    Privilege.CREATE, 
                    Privilege.DELETE
           ));
    final User user3 = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    Predicate<User> firstNameLongerThan3 = user -> 
            user.getFirstName().length()>3;
    Predicate<User> privilegeGreaterThan2 = user -> 
            user.getPrivileges().size()>2;

    List<User> users = userService.filterBy(
            Arrays.asList(user1, user2, user3),
            firstNameLongerThan3,
            privilegeGreaterThan2
    );

    System.out.println(users);
    Assertions.assertEquals(users.size(), 1);
}
```

We have 3 Users, on which we two Predicates/Filters applied, and our assertion criteria will also be same.

> *Predicate *is a *boolean *valued one argument functional Interface, which has *test()* as the functional method.

#### Lets check the logic to get this:

```java
@Override
public List<User> filterBy(List<User> users, 
        Predicate<User>... predicates) {
    Predicate<User> allPredicates = Arrays.stream(predicates)
                    .reduce(w->true, Predicate::and);

    return users.stream()
            .filter(allPredicates)
            .collect(Collectors.toList());
}
```

In order to club all the predicates together, we will create a new Predicate, which will take the input list of all predicate and reduce it with an AND operation. We can also use OR operation as well. 

The *w--> true* is the initial value, so now when we club together all predicates it would be something like this.

```java
true AND Predicate1_Output AND Predicate2_Output AND....
```

Output for this scenario is:

```java
[2_Greg_Jonson_30_(UPDATE,CREATE,DELETE)]
```

We can have one more scenario where there are no predicates or filters applies. When we don't have any filter, it will return the same list as output.

#### Lets check the Junit for Empty Filters:

```java
@Test
@DisplayName("Return same list if found no filterBy conditions(predicates)")
void emptyFilter() {
    final User user1 = new User(1L, "John", "Doe", 26, 
            Collections.singletonList(Privilege.UPDATE));
    final User user2 = new User(2L, "Greg", "Jonson", 30, 
            Arrays.asList(
                    Privilege.UPDATE, 
                    Privilege.CREATE, 
                    Privilege.DELETE
            ));
    final User user3 = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    List<User> users = userService.filterBy(
            Arrays.asList(user1, user2, user3)
    );

    System.out.println(users);
    Assertions.assertEquals(users.size(), 3);
}
```

In this we don't have any filters applied, which will return the same input list as output.

Output is:

```java
[
 1_John_Doe_26_(UPDATE), 
 2_Greg_Jonson_30_(UPDATE,CREATE,DELETE), 
 3_Alex_Smith_13_(DELETE)
]
```

### **9. Map** given Function with Delimiter

We are given with a function which we need to apply for the list of User and join it based on the delimiter provided.

#### Lets the check the Junit for this scenario:

```java
@Test
@DisplayName("Convert Users by applying Function and delimited by |")
void convertTo() {
    final User user1 = new User(1L, "John", "Doe", 26, 
            Collections.emptyList());
    final User user2 = new User(2L, "Greg", "Jonson", 30, 
            Collections.emptyList());
    final User user3 = new User(3L, "Alex", "Smith", 13, 
            Collections.emptyList());

    Function<User, String> function = User::getLastName;

    String convertedStr = userService.convertTo(
            Arrays.asList(user1, user2, user3),
            "|",
            function
    );

    System.out.println(convertedStr);
    Assertions.assertEquals(convertedStr, "Doe|Jonson|Smith");
}
```

We have 3 Users, and a Function, where we have to map the User stream to each User's last name. Then return the String joined by pipe delimiter. And this String will be out assertion criteria as well.

> Function is a functional Interface which takes one argument and produces the result. It has *apply()* as the functional method.

Like the previous one, where we have to apply Predicates, here will be mapping the Function given. 

#### Lets check the logic for this:

```java
@Override
public String convertTo(List<User> users, String delimiter, 
        Function<User, String> mapFun) {
    return users.stream()
            .map(mapFun)
            .peek(System.out::println)
            .collect(Collectors.joining(delimiter));
}
```

Here, we are using *map()* to pass the Function, and the while collecting we are using *Collectors.joining()* method to convert it to String with delimiter.

Output is:

```java
Doe
Jonson
Smith
---------------------------------------------->>Above are from peek()
Doe|Jonson|Smith
```

### **10. Group** by Privileges

We have to group the Users on the Privileges, such that it returns Map<Privilege, List<User>>. This is a bit tricky. 

#### Lets the check the Junit for this scenario:

```java
@Test
void groupByPrivileges() {
    User user1 = new User(1L, "John", "Doe", 26,
             Collections.singletonList(Privilege.UPDATE));
    User user2 = new User(2L, "Greg", "Jonson", 30, 
            Arrays.asList(
                    Privilege.UPDATE, 
                    Privilege.CREATE, 
                    Privilege.DELETE
            ));
    User user3 = new User(3L, "Alex", "Smith", 13, 
            Collections.singletonList(Privilege.DELETE));

    Map<Privilege, List<User>> privilegesMap = userService
            .groupByPrivileges(
                    new ArrayList<>(Arrays.asList(user1, user2, user3)
            )
    );

    Assertions.assertArrayEquals(
            new int[]{0, 1, 2, 2},
            new int[]{
                    privilegesMap.containsKey(Privilege.READ) ? privilegesMap.get(Privilege.READ).size() : 0,
                    privilegesMap.containsKey(Privilege.CREATE) ? privilegesMap.get(Privilege.CREATE).size() : 0,
                    privilegesMap.containsKey(Privilege.UPDATE) ? privilegesMap.get(Privilege.UPDATE).size() : 0,
                    privilegesMap.containsKey(Privilege.DELETE) ? privilegesMap.get(Privilege.DELETE).size() : 0
            }
    );
}
```

Here, we have 3 Users, which has different Privilege, and we are asserting on Map elements to return the correct size of the users for each Privilege.

> *Arrays.asList()* always returns a fixed sized list. If you try to change the size by adding or removing, it will throw *UnsupportedOperationException*.

To get a variable sized list from Arrays.asList(), have

```java
new ArrayList<>(Arrays.asList())
```

#### Lets check the logic for this:

This logic is from [*Stackoverflow*](https://stackoverflow.com/a/55145947)* post*. 

```java
@Override
    public Map<Privilege, List<User>> groupByPrivileges(List<User> users) {
//        Map<Privilege, List<User>> map = new HashMap<>();
//        for(User user: users){
//            for(Privilege p: user.getPrivileges()){
//                if(map.containsKey(p)) {
//                    List<User> tmp = map.get(p);
//                    tmp.add(user);
//                    map.put(p, tmp);
//                } else {
//                    map.put(p, new ArrayList<>(Arrays.asList(user)));
//                }
//            }
//        }
//        return map;

        return users.stream()
                .flatMap(
                    user -> user.getPrivileges().stream()
                        .map(privilege -> 
                        new AbstractMap.SimpleEntry<>(privilege, user))
                )
                .peek(System.out::println)
                .collect(
                        Collectors.groupingBy(
                                Map.Entry::getKey,
                                Collectors.mapping(
                                        Map.Entry::getValue,
                                        Collectors.toList()
                                )
                        )
                );
    }
```

If you notice the commented piece of code, it is the old way of how you would approach the same problem. But with lambdas, and functional programming, we are using the *flatMap()* to convert the List<List<Privilege>> to create a *AbstractMap.SimpleEntry()* of Privilege object and User object.

> *AbstractMap* provides skeletal implementation of the *Map *Interface, to minimize the effort required to implement this interface. To return an *Unmodifiable *map, don't implement the *entrySet() *method. On add or remove, throw *UnsupportedOperationException*. Do vice-versa to implement *Modifiable *Map.

After creating a map of Privilege and list of user, we have to group by the map's key which is Privilege class based on map's value's size count.

Its a bit difficult to think this implementation way, which makes it tricky comparing the ask is only to group by Privilege.

### References
* [*https://github.com/vbrenister/java8-practice*](https://github.com/vbrenister/java8-practice) - I have used the problem set from this Github profile. Do check it out.
* [*https://stackoverflow.com/a/55145947*](https://stackoverflow.com/a/55145947) - this is for the 10th scenario.

This will conclude the list of different scenarios which should help us in learning these implementation ways using lambdas and functional programming. Its always good to try before appearing for an interview, as these have some common ways which are frequently asked in interviews.

There will be other ways to do these problem set. Please do comment out if you find any. 

Hope this will help you in your learning process. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.