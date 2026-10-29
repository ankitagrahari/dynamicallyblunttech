---
title: "#LC746 - Minimum Cost Of Climbing Stairs"
date: 2026-10-27T08:14:21+05:30
draft: false
featureImage: "images/df024c_4243b8a6b27d4c41aba7bc481af7db15.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will look into the the [*leetcode #746*](https://leetcode.com/problems/min-cost-climbing-stairs/) problem to find the minimum cost of climbing stairs. This is also a good example to start your journey to learn dynamic programming.

### **Problem Statement**

You are given an integer array cost where ***cost[i]*** is the cost of ***ith*** step on a staircase. Once you pay the cost, you can either climb one or two steps. You can either start from the step with index 0, or the step with index 1. 


Return the minimum cost to reach the top of the floor. 

**Example 1:**
  *Input:* cost = [10,15,20]
  *Output:* 15
  *Explanation: You will start at index 1.*
*  - Pay 15 and climb two steps to reach the top.*
*  The total cost is 15.*

**Example 2:**
  *Input:* cost = [1,100,1,1,1,100,1,1,100,1]
  *Output:* 6
  *Explanation: You will start at index 0.*
*  - Pay 1 and climb two steps to reach index 2.*
*  - Pay 1 and climb two steps to reach index 4.*
*  - Pay 1 and climb two steps to reach index 6.*
*  - Pay 1 and climb one step to reach index 7.*
*  - Pay 1 and climb two steps to reach index 9.*
*  - Pay 1 and climb one step to reach the top.*
*  The total cost is 6. *

**Constraints:**
  *2 <= cost.length <= 1000*
*  0 <= cost[i] <= 999*

### **Algorithm/Logic**

In this DP problem we will solve the subset of the problem, store the result and then solve next subset of the problem and combine all the result to get the final output. Here we should always start from the end of the given array. 

In order to calculate the minimum, we have to pick the minimum of the two steps at any given time and add the value at the given index. Once the minimum to get to that step is calculated, it will store it in the current step variable and then move backwards on that index. 

Once we have iterated all the indexes, then we only have to get the minimum of the two steps variable we have used before.


The code will look something like this:

```java
int steps = cost.length;
int step1 = 0, step2 = 0;
for(int i=steps-1; i>=0; i--){
    int curStep = cost[i] + Math.min(step1, step2);
    step1 = step2;
    step2 = curStep;
}
return Math.min(step1, step2);
```

The above solution takes 1ms and 40mb to execute.

You can find the complete code here on my [*github repository*](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/leetcode/dp/MinCostClimbingStairs746.java). Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.