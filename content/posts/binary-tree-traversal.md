---
title: "Binary Tree Traversal"
date: 2026-10-27T08:14:30+05:30
draft: false
featureImage: "images/df024c_d8c9f57927994358989b02cabcca63dc.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will look into the different ways to traverse a Binary Tree.

In a binary tree, you can traverse in two different ways:
* Breadth first traversal
* Depth first traversal
* In-order
* Pre-order
* Post-order

Lets start with an example. Given the following binary tree:

```java
4
   /   \
  2     7
 / \   / \
1   3 6   9
```

When we traverse a binary tree, we can go either breadth first or depth first. 

### **Breadth First**

Now when we say breadth first, it start from the root node and traverse all the nodes at that level. Once all the nodes is traversed, we go to next level and so on.

In our case, the breadth first will be like this

```java
4 --> 2 --> 7 --> 1 --> 3 --> 6 --> 9
```

### **Depth First**

In the depth first, we traverse from root to the leaf node. There are three types of depth first traversal:


#### **In-order Traversal**

In this traversal, we follow the order: *Left > Root > Right. *We print the left node then the root and then the right node. So, in our case the In-order traversal will be 

```java
1 --> 2 --> 3 --> 4 --> 6 --> 7 --> 9
```

#### **Pre-order Traversal**

In this traversal, we follow the order: ***Root >**** Left  > Right. *We print the left node then the root and then the right node. So, in our case the In-order traversal will be 

```java
4 --> 2 --> 1 --> 3 --> 7 --> 6 --> 9
```

#### **Post-order Traversal**

In this traversal, we follow the order: *Left > Right >Root . *We print the left node then the root and then the right node. So, in our case the In-order traversal will be 

```java
1 --> 3 --> 2 --> 6 --> 9 --> 7 --> 4
```

These are some of the ways to traverse a binary tree. You can find the code base here. [*Github Link*](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/tree/binary/BTreeTraversal.java)
Also, refer here to know [how to inverse a binary tree](https://dynamicallyblunttech.blogspot.com/2020/06/inversion-of-binary-tree-in-java-using.html).

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.