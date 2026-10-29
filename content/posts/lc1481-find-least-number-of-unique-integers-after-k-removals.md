---
title: "#LC1481 - Find Least Number of Unique Integers After K Removals"
date: 2026-10-27T08:14:24+05:30
draft: false
featureImage: "images/df024c_7fec00e1471f4d6b9bcd0ba25d39f852.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post, we will look into one of the [*Leetcode problem #1481*](https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/), where we have to find the least number of unique integers after removing k elements.

### **Problem Statement:**

Given an array of integers ***arr*** and an integer ***k***. Find the *least number of unique integers* after removing exactly k elements.
So, the problem statements says to remove k elements from the given array in such a way that we get the least number of unique integers. Lets say we have following array:  

```java
arr[] = {5, 5, 4};    k=1;
```

In this case, we can remove only one element from the array. If we remove 5, we will get 4 remaining or if we remove 4, we will get two counts of 5 remaining. In either case, the count of unique integers is 1.

Lets take another example, which is not given in the Leetcode #1481 problem statement:

```java
arr[] = {2, 1, 1, 3, 3, 3};    k=3;
```

In the above example, we have to remove 3 elements from the array.


Now, if we remove one count of each 2, 1, 3 we will get one counts of 1 and two counts of 3 remaining.
Lets say, if we remove all three counts of 3, we will get one counts of 1 and two counts of 1 remaining.
Lets say, if we remove all two counts of 1 and one counts of 2, we will get all three counts of 3 remaining. 

So, in any scenario, the output will be 2, and so is the answer.

### **Logic/Algorithm**

First and the foremost thing to do is to have the occurrence count of each elements in the array. 

After this, we have to remove the elements with the least occurrence count and gradually decrease the value of  k.

In order to get the elements with the least count, we will prepare a map and sort it based on the values, which is the occurrence count.

### **Code Snippet **

Let look into the code:


##### **Get the occurrence count of each elements present in the array**

```java
Map<Integer, Integer> countMap = new HashMap<>();
for(int i: arr){
    countMap.put(i, countMap.getOrDefault(i, 0)+1);
}
```

##### **Sort the map based on the occurrence count**

```java
Comparator<Map.Entry<Integer, Integer>> sortByCount = Comparator.comparing(Map.Entry::getValue);
Map<Integer, Integer> linkedCountMap = countMap.entrySet()
        .stream()
        .sorted(sortByCount)
        .collect(Collectors.toMap(
                Map.Entry::getKey,
                Map.Entry::getValue,
                (e1, e2) -> e1,
                LinkedHashMap::new)
        );
```

The above code is using a ***Comparator*** to sort the ***Map ***based on its values. We will construct a ***LinkedHashMap ***which will contain the sorted ***Map ***based on value, which is the occurrence count.


##### **Iterate and remove the items from the Sorted map based on the value of  ****k****. **

If the occurrence count of the elements is more than k, then we will deduct the occurrence count value by k

```java
Iterator<Map.Entry<Integer, Integer>> itr = linkedCountMap
            .entrySet()
            .iterator();
Map.Entry<Integer, Integer> nextEle;
while(itr.hasNext() && k>0){
    nextEle = itr.next();
    if(nextEle.getValue()>k){
        linkedCountMap.put(nextEle.getKey(), nextEle.getValue()-k);
        break;
    }
    k = k - nextEle.getValue();
    itr.remove();
}
```

Return the size of the ***LinkedHashMap***.

```java
return linkedCountMap.size();
```

The entire code base can be found on [*Github repository*](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/leetcode/FindLeastNumOfUniqueInts.java). Also, this code took ***81ms*** and it consumed ***55.7mb*** of memory to run all test cases on Leetcode.

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.