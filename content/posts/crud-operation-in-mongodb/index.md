---
title: "CRUD operation in MongoDB"
date: 2026-10-27T08:14:20+05:30
draft: false
featureImage: "images/df024c_ffb0aee799ef4a768ccec9ae6e32939b.jpg"
tags: ['CRUD', 'MongoDB']
categories: ['MongoDB', 'CRUD']
showReadingTime: true
---

In this post we will create a Java application which will interact with MongoDB to perform all the CRUD operations. 

## **What is NoSQL database.**

To start with, these database are non-relational database, but that doesn't mean that the NoSQL database cannot maintain relationship. These database are different from relational database in the way the data is stored. NoSQL data model keeps the related data nested to single data structure.

It can be called as "***non SQL***" or "***not only SQL***" database.

## **What is MongoDB ?**

As stated on MongoDB official website: 

> *MongoDB is a document database with the scalability and flexibility that you want with the querying and indexing that you need*

MongoDB is a NoSQL database which stores data in ***JSON ***like documents, means that the number/type of fields can vary from document to document. ***It is a distributed database at its core, so high availability, horizontal scaling and easy to use***.


And on top of it, its free to use. So lets use it to create, update, retrieve and delete (***CRUD***) data from MongoDB using Java.

## **Basics**

### ***Database***

In MongoDB, database is collection of documents. A single MongoDB server can have multiple databases.

You can create database using below command. 

```java
> use mydb
switched to db mydb
> dbs
mydb
Collections
```

It will access the database if it exists, else it will *create the database when you store data to it*. The command "dbs" will let you know which database you are accessing.

### ***Collections***

In MongoDB, Collections can be compared to tables in relational database. Only change here is that these are non tabular. The below command can be used to create collection.

```java
db.createCollection(<collectionName>)
```

To list down all the collections in the database, use below command

```java
db.getCollectionNames()
```

### ***Documents***

In MongoDB, Documents can be compared to rows in relational database. Only change here is that these documents are JSON like records. 

```java
{ "_id" : { 
    "$oid" : "5ede054470d5755464d4f37a" 
  }, 
  "name" : "NewDoc", 
  "type" : "database", 
  "count" : 5, 
  "versions" : ["v3.2", "v3.0", "v2.6"], 
  "info" : { "x" : 203, "y" : 102 } 
}
```

## **Perform CURD operation on MongoDB**

We will create a Java project which will 

Add the mongoDB dependency, &

Connect to the database &

Access the specific databases, &

List all the databases, &

Create and Access Collections, &

Create Documents, &  

List all documents, &

Retrieve specific Docuements, &

Update specific Document, &

Delete specific Documents

### **Dependencies**

To include monogdb in your project you can use the following maven dependency in your pom.xml file.

```java
<dependency>
    <groupId>org.mongodb</groupId>
    <artifactId>mongo-java-driver</artifactId>
    <version>3.4.1</version>
</dependency>
```

### **Create MongoClient Object**

Like with any other database we will create a MongoClient object to connect to the mongoDB database. We can use MongoClient or MongoClientURI to create the client object.
* Create client for default host localhost and default port 27017:

```java
MongoClient client = new MongoClient();
```
* Create client for given host and default port 27017:

```java
MongoClient client = new MongoClient("localhost");
```
* Create client for given host and port:

```java
MongoClient client = new MongoClient("localhost", 27017);
```
* Create client using the connection string:

```java
MongoClientURI connectionString = new MongoClientURI(
        "mongodb://localhost:27017");
MongoClient mongoClient = new MongoClient(connectionString);
```

### **Accessing given Database**

Once we have created the *MongoClient* object, we can get specific database using ***getDatabase()*** method.

```java
//Access given database
MongoDatabase db = client.getDatabase("mydb");
System.out.println(db.getName());
```

### **List all Database names**

Using the *MongoClient* object created above, we can list down all the databases created using ***listDatabaseNames() ***method.

```java
//Listing all the database
MongoIterable<String> itr = client.listDatabaseNames();
for (MongoCursor<String> it = itr.iterator(); it.hasNext(); ) {
    System.out.println(it.next());
}
```

### **Create and Access Collection**

Using the *MongoClient* object, we can create a new collection and access the new collection using ***getCollection()***** **method.

```java
//Create a collection under mydb
db.createCollection("mycol");

//Access given (mycol) collection
MongoCollection<Document> collection = db.getCollection("mycol");
```

### **Create Documents**

We have to create Document object to store each record and will use the collection created above to insert these documents to specific collection.

```java
Document document = new Document("name", "NewDoc")
        .append("type", "database")
        .append("count", 1)
        .append("versions", Arrays.asList("v3.2", "v3.0", "v2.6"))
        .append("info", new Document("x", 203).append("y",102));
collection.insertOne(document);
System.out.println("After adding one document to the collection, total count of documents is "+collection.count());
```

After adding the document to the collection, we can get the count of documents present in the collections using ***collections.count()*** method. 

We can insert either one document or list of documents to a collection.

```java
MongoCollection<Document> collection = db.getCollection("mycol");
List<Document> documents = new ArrayList<>();
Document document1 = new Document("name", "SecDoc")
        .append("type", "middleware")
        .append("count", 2)
        .append("versions", Arrays.asList("v1.2", "v1.0"));
Document document2 = new Document("name", "ThirdDoc")
        .append("type", "database")
        .append("count", 3)
        .append("versions", Arrays.asList("11g", "12c", "18c", "19c"));

documents.add(document1); 
documents.add(document2);
collection.insertMany(documents);
```

Now if you execute the ***collections.count()*** method, you will get count as 2.

### **List all Documents**

Like listing all the databases, you can list down all the documents using the ***find()*** method which provides the iterator on the *MongoCursor* and even print it in *JSON *format using ***toJSON()*** method.

```java
public static void listAllDocuments(MongoCollection<Document> collection){
    System.out.println("Listing all documents in the collection in JSON format");
    MongoCursor<Document> cursor = collection.find().iterator();
    while(cursor.hasNext()){
        System.out.println(cursor.next().toJson());
    }
}
```

We can also use the ***collection.find().first()*** method to get the first document/record from the collection.

### **Retrieving Documents**

In order to fetch some documents on desired constraints, we can use the ***find()*** method with the *Filters *class which contains all the utilities that can be used in the finding the documents. This is analogous to the where clause in relational database.

We have to statically import *Filters *class

```java
import static com.mongodb.client.model.Filters.and;
import static com.mongodb.client.model.Filters.eq;
```

And the same can be used in the find() method to apply the where clause.

```java
MongoDatabase db = client.getDatabase("mydb");
MongoCollection<Document> collection = db.getCollection("mycol");
Document docTypeMiddleware = collection.find(
                eq("type","middleware")
             ).first();
System.out.println("Document where type=middleware: ");
System.out.println(docTypeMiddleware.toJson());

Document docTypeDBCount1 = collection.find(
                and(eq("type", "database"), 
                    eq("count", 1)
                )
             ).first();
System.out.println("Document where type=database and count=1");
System.out.println(docTypeDBCount1.toJson());
```

### **Update Documents**

We can update the documents created using ***updateMany()*** or ***updateOne()*** methods. It returns *UpdateResult *class with which we can get the count of records updated.

```java
MongoDatabase db = client.getDatabase("mydb");
MongoCollection<Document> collection = db.getCollection("mycol");
UpdateResult updateResult = collection.updateMany(
        eq("type","database"), 
        new Document("$set", new Document("count", 5))
    );
System.out.println(updateResult.getModifiedCount());
this.listAllDocuments(collection);
```

The last line will call the above method which will list all the documents in that collection.

### **Delete Documents**

We can also delete documents which is comparable to deleting rows from tables in relational database. It return *DeleteResult**** ***class, using which we can get the number of records deleted.

```java
MongoDatabase db = client.getDatabase("mydb");
MongoCollection<Document> collection = db.getCollection("mycol");
DeleteResult deleteResult = collection.deleteOne(
        eq("type", "middleware")
     );
System.out.println(deleteResult.getDeletedCount());
```

This concludes the creating, retrieving, updating and deleting a document (all CRUD operation) in MongoDB. These are some basic operation to start using a NoSQL database. It has a lot of other thing, but this should be a good starting point to use it your projects for basic operations.


You can find the entire code base in this [*Github *](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/rest/RestAPI.java)*repository*.

### Reference
* [https://docs.mongodb.com/manual/introduction/](https://docs.mongodb.com/manual/introduction/)
* [https://mongodb.github.io/mongo-java-driver/3.4/driver/getting-started/quick-start/](https://mongodb.github.io/mongo-java-driver/3.4/driver/getting-started/quick-start/)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.