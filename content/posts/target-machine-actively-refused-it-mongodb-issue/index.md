---
title: "Target Machine Actively Refused it - MongoDB Issue"
date: 2026-10-27T08:14:30+05:30
draft: false
tags: ['MongoDB']
categories: ['MongoDB']
showReadingTime: true
---

In this post we will discuss one of the issue encountered after installing MongoDB on my windows machine. This from the [***previous post***](posts/crud-operation-in-mongodb) where we performed all the CRUD operation on MonogDB in Java.

For installation of MongoDB, follow the official guide.

### **Issue**

While opening the mongo.exe by double clicking on it, the console opens and then it vanishes. So, I tired again, still the console just showed for a second or two and then vanished again in thin air. Even tried using the mongoDB compass editor to check the connection, but that also didn't connect.

### **Reason**

So this issue can happen if the underline *data directory is corrupted* or the mongoDB needs some *repairing*. 

Check for data directory you have started MongoDB with, or you can create another data directory. Mostly if you are using a different data directory, that should solve the issue, but if there is something to be repaired on the MongoDB, then this will again occur, when you again open it.

### **Resolution**

As stated above, try opening with a different data directory like this

```java
mongod --dbpath C:/data/db
```

If the data/db directory is not present, you can create it under C: directory. You can also use any other directory and mention the path here.

If creating the db path also didn't solve the problem, then you have to repair the installed MongoDB.

Go to the installed bin directory and run following command:

```java
mongod --repair
```

Let this run, it shouldn't take much time. When the repairing is done, it will not close the console and *you also shouldn't close it*. 

Now, double click on the mongo.exe and the console will not vanish and you can key in your commands. 

This helped me resolving the above issue. Let me know in the comments below if you followed another resolution technique. Also if you like my work you can subscribe and appreciate my work from the Subscribe section.