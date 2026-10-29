---
title: "#LC438 - Find All Anagrams - Sliding Window Algorithm"
date: 2026-10-27T08:14:22+05:30
draft: false
featureImage: "images/df024c_1b140b6fe8e547ed8dbece7d21265fc0.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this topic we will cover the [*leetcode #438*](https://leetcode.com/problems/find-all-anagrams-in-a-string/) Find all anagram programming question.

### Problem Statement:

Given two strings s and p, return *an array of all the start indices of p's anagrams in *s. You may return the answer in **any order**.

### Input

***String from***   -- this is the main string from which we have to find all the anagrams.

***String find***    -- this is the string for which we have to find if its anagrams are present in the *from* string.

### Algorithm/Logic

We will be using ***Sliding Window Algorithm***. 
The logic here is to prepare an int array of 26 length (called ***hash***), which contains the 0 as the initial value. It will increment value at those indexes, for which the character at the specific index in the ***find***** **string is present.

```java
public int[] prepareHash(String str){
    int[] charCount = new int[26];
    for(char c : str.toCharArray()){
        charCount[c - 'a']++;
    }
    return charCount;
}
```

The ***find ***string length defines the length of the window. We will keep the ***left ***and ***right ***variable to keep the windows start and end indexes.

```java
int[] findHash = prepareHash(find);
int left=0, right=find.length();
```

Now, for the characters present in the window, we will find the hash again and compare this int array with the hash we computed from the ***find***** **string. If both the arrays are equal, then we will add the ***left ***value in the ***result ***list. If both the arrays are not equal, we will slide the window one step ahead, means we will increment the ***left ***and ***right ***variable values. 

```java
while(right <= from.length()){
    String temp = from.substring(left, right);
    int[] tempCharCount = prepareHash(temp);
    if(Arrays.equals(findHash, tempCharCount)){
        result.add(left);
    }
    left++;
    right++;
}
```

Sliding the window, we will get all the possible anagrams present in the input ***from*** string. The below code will list all the indexes where we can find the anagrams.

```java
System.out.println(result.stream().map(Object::toString).collect(Collectors.joining(",")));
```

You can find the entire code base here. [*Github Link*](https://github.com/ankitagrahari/StringManipulation/blob/master/src/com/Anagram.java)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.