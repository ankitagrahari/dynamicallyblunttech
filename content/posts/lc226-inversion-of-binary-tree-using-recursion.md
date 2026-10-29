---
title: "#LC226 - Inversion Of Binary Tree Using Recursion"
date: 2026-10-27T08:14:12+05:30
draft: false
featureImage: "images/df024c_3f94199d5ca648618530ebd3bd3ed089.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

Following the last post on the[* binary tree traversals*](https://www.dynamicallyblunttech.com/post/binary-tree-traversal), in this post we will try to invert a given binary tree.

Binary tree is a data structure in which a node can have maximum two child nodes and minimum zero nodes. Each node contains the value of the node, the left node reference and right node reference.

```java
4
   /   \
  2     7
 / \   / \
1   3 6   9
```

In the above binary tree, root node has a value of 4 and 2 is the left node of the root and 7 is right node of the root. ***An inverted node will look like this, where the left node is swapped with the right node.***

```java
4
   /   \
  7     2
 / \   / \
9   6 3   1
```

#### **Create the Node**

Node can be used to construct a Binary Tree. We will be using the lombok library to avoid the boilerplate code. Using @Data annotation, we can avoid writing the constructors, setters and getters method.

```java
@Data
class TreeNode{
    private TreeNode left;
    private TreeNode right;
    private String value;  
}
```

#### **Prepare a binary tree**

```java
public TreeNode prepareBTree(){
    TreeNode leaf1 = new TreeNode("1");
    TreeNode leaf2 = new TreeNode("3");
    TreeNode leaf3 = new TreeNode("6");
    TreeNode leaf4 = new TreeNode("9");

    TreeNode nodeRight = new TreeNode(leaf3, leaf4, "7");
    TreeNode nodeLeft = new TreeNode(leaf1, leaf2, "2");

    TreeNode root = new TreeNode(nodeLeft, nodeRight, "4");
    return root;
}
```

#### **Invert Binary Tree (Algorithm/Logic)**

To invert the binary tree, we will use recursion and use the same logic we use for swapping two values. Using a third Node, we will swap the left and right nodes with each other.

In the below method, we are recursively going to each sub-binary tree and swapping the left node and right node with each other. Here the exit criteria will be leaf node. Leaf nodes don't have any left or right node. So, if a ***node.left*** is null or ***node.right*** is null, then the program will return the null.

```java
public TreeNode invertBTree(TreeNode node){
    if(null==node){
        return null;
    }
    if(null==node.getLeft() && null==node.getRight()){
        return node;
    }
    TreeNode temp = node.getLeft();
    node.setLeft(node.getRight());
    node.setRight(temp);

    invertBTree(node.getLeft());
    invertBTree(node.getRight());
    return node;
}
```

You can find the whole code here. [*Github Link*](https://github.com/ankitagrahari/Tryouts/tree/master/src/main/java/com/tree/binary)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.