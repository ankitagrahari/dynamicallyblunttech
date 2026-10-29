---
title: "#LC105 - Binary Tree from In-Order and Pre-Order Traversal"
date: 2026-10-27T08:14:25+05:30
draft: false
featureImage: "images/df024c_cefb7e67b8714df19b270eaf4eb5ec0e.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will create a binary tree from the given in-order and pre-order traversal. You can find the details on the question here [***leetcode #105***](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/).

So, in a binary tree, we can do depth first traversal in three ways: 
* ***In-order traversal  (left -> root -> right) ***
* ***Pre-order traversal  (root -> left -> right) ***
* ***Post-order traversal  (left -> right -> root) ***

Refer [***Binary Tree - Traversal***](https://www.dynamicallyblunttech.com/post/binary-tree-traversal) to understand on how to traverse using the above three ways.

### **Problem Statement**

The problem states to construct the binary tree with the given pre-order traversal and in-order traversal. 

Input:

```java
pre-order    : [4, 2, 1, 3, 7, 6, 9]
in-order      : [1, 2, 3, 4, 6, 7, 9]
```

**Output:**

```java
4
   /   \
  2     7
 / \   / \
1   3 6   9
```

### **Algorithm/Logic**

Using the pre-order traversal, we can deduce that the first node in the pre-order array will be the root of the binary tree, we are going to construct. 

Further, now we will look in the in-order traversal for the root and whatever comes on the left side of the root in the in-order traversal will be the nodes present on the left side of the root node and whatever comes on the right side of the root in the in-order traversal will be on the right side of the root node.

From the first node in the pre-order traversal, we know that 4 is the root node of our binary tree. We will find the root node in in-order and divide the left nodes and right nodes.

```java
4
   /   \
1,2,3  6,7,9
```

Now, for the second round of recursion, we will take the left node list and perform the same approach as applied to find the first level of the binary tree. 

From the left node list (1, 2, 3), the root node will be 2 which is the next node after 4 in the pre-order traversal. Now, in the in-order traversal, nodes to the left of the new root node 2 is 1 and to the right of root node 2 is 3. So, we have the left nodes set for our binary tree. 

```java
4
   /   \
  2   6,7,9
 / \  
1   3
```

Using the same approach, we can construct the rights nodes of our binary tree and can construct the entire binary tree. 

```java
4
   /   \
  2     7
 / \   / \
1   3 6   9
```

### **Code-snippet**

We will add the lombok dependency to avoid any boilerplate code. If you are just writing the program without using maven or gradle, then you can skip adding this dependency and instead just add the constructor, getter and setter methods.

```java
<dependencies>
	<dependency>
		<groupId>org.projectlombok</groupId>
		<artifactId>lombok</artifactId>
		<version>1.18.22</version>
		<scope>provided</scope>
	</dependency>
</dependencies>
```

For any TreeNode, we will have the left node, right node and the value of the node.

```java
@Data
public class TreeNode {
    private TreeNode left;
    private TreeNode right;
    private int intValue;
}
```

The ***@Data*** annotation will add the required constructors, getters and setters method for all these attributes.

With this, we will need a utility to find the root node in the in-order traversal in the given index range.

```java
private int getNodeIndexInIn(int node, int[] inOrder, int start, int end){
    int index = 0;
    for(int i=start; i<=end; i++){
        if(node==inOrder[i]){
            index = i;
            return index;
        }
    }
    return index;
}
```

Now we will use recursion to create my left sub tree and then my right sub tree. To keep track on the node which will be our root for sub-trees, we will keep a global index variable.

***NOTE: ****Always be extra careful for the exit criteria when you write programs using recursion. These exit points are the key in stopping the recursion. Else you will get ****StackOverflow**** error.*

There will be two exit criteria defined for our recursion: 

first:

```java
//1st Exit Criteria: Return null, when the indexes are crossing each other, means no value can be found in the array
    if(inStart > inEnd){
        return null;
    }
```

Second:

```java
//Second exit criteria: When the node is a leaf node, means no left or right node exists, then return the node
    if (inStart == inEnd) {
        return rootNode;
    }
```

To construct our left and right subtree it will call the recursively with proper start and end index with the correct root index for our subtrees.

```java
//Find the rootIndex in Inorder array
int rootIndexInInorder = getNodeIndexInIn(root, in, inStart, inEnd);

rootNode.setLeft(constructBTree("left", inStart, rootIndexInInorder - 1, in, pre));
rootNode.setRight(constructBTree("right", rootIndexInInorder + 1, inEnd, in, pre));
```

So finally the entire code of recursion now will look like this:

```java
//This will be used for get the root index in preOrder
private static int preRootIndex = 0;

public TreeNode constructBTree(String side, int inStart, int inEnd, int[] in, int[] pre){
    //1st Exit Criteria: Return null, when the indexes are crossing each other, means no value can be found in the array
    if(inStart > inEnd){
        return null;
    }
    int root = pre[preRootIndex++];
    TreeNode rootNode = new TreeNode(root);
    
    //Second exit criteria: When the node is a leaf node, means no left or right node exists, then return the node
    if (inStart == inEnd) {
        return rootNode;
    }
    //Find the rootIndex in Inorder array
    int rootIndexInInorder = getNodeIndexInIn(root, in, inStart, inEnd);

    rootNode.setLeft(constructBTree("left", inStart, rootIndexInInorder - 1, in, pre));
    rootNode.setRight(constructBTree("right", rootIndexInInorder + 1, inEnd, in, pre));

    return rootNode;
}
```

The code for the above program can be found here [***Github Link***](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/tree/binary/ConstructBtreeFromInPreOrder.java)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.