---
title: "#LC983 - Find The Minimum Cost For Tickets (DP)"
date: 2026-10-27T08:14:25+05:30
draft: false
featureImage: "images/df024c_6b79f295bdba4e2fa607a62e2b69a927.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will go through the [*Leetcode #983*](https://leetcode.com/problems/minimum-cost-for-tickets/) to find the minimum cost for Tickets, which could be one of the starting practice programs in ***Dynamic Programming***. This is a really interesting problem and I took help from [*Nideesh Terapalli*](https://www.youtube.com/watch?v=HyN5hdD1JU4) youtube video.

### **Problem Statement**

In a country popular for train travel, you have planned some train travelling one year in advance.  The days of the year that you will travel is given as an array days.  Each day is an integer from 1 to 365.

Train tickets are sold in 3 different ways:
* a 1-day pass is sold for costs[0] dollars;
* a 7-day pass is sold for costs[1] dollars;
* a 30-day pass is sold for costs[2] dollars.

The passes allow that many days of consecutive travel. For example, if we get a 7-day pass on day 2, then we can travel for 7 days: day 2, 3, 4, 5, 6, 7, and 8.

Return the minimum number of dollars you need to travel every day in the given list of days. 

### **Logic/ Algorithm:**

As the problem states, that we need to find the travel cost of a planned year, where I know the days of travel. Now to minimize the cost of the travel, I have to take the pass in such a way that the total cost is minimum.

We will divide the problem in three parts:

I know the days I am travelling,

I know that for the day I am going to travel there are three option, either I will pay for a day, or for a week, or for a month. 

From the problem, we can find the last day I traveled, by getting the last element of the array ***days***. 

Now we can deduce from the above, cost of travel for the days I don't travel will be whatever is the cost of the last day. Whether 
* If the last day falls under single day pass, then I will be paying costs[0], or
* If the last day falls under seven day pass, then I will be paying costs[1], or
* If the last day falls under thirty days pass, then I will be paying costs[2].

Now, lets dig into the code.

### **Code**

To find the last day of my travel prepare two arrays 
* cost of each day, and
* all the travel days.

```java
int lastDayForTravel = days[days.length-1];
boolean[] travelDays = new boolean[lastDayForTravel+1];
int[] costOfEachDay = new int[lastDayForTravel+1];
```

Prepare the travelDays array which is a boolean array where days I traveled is marked ***True***.

```java
for(int day: days){
    travelDays[day] = true;
}
```

Iterate over our resulting array *costOfEachDay, *to set the cost of travel for each day

```java
for(int i=1; i<costOfEachDay.length; i++){
    if(!travelDays[i]){
        costOfEachDay[i] = costOfEachDay[i-1];
        continue;
    } else {
        int boughtSingleDay = costOfEachDay[i-1] + cost[0];
        int boughtSevenDays = costOfEachDay[Math.max(i-7, 0)] + cost[1];
        int boughtThirtyDays = costOfEachDay[Math.max(i-30, 0)] + cost[2];
        int temp = Math.min(boughtSingleDay, boughtSevenDays);
        costOfEachDay[i] = Math.min(temp, boughtThirtyDays);
    }
}
```

Return the final answer which will be the last element of the array *costOfEachDay*

```java
return costOfEachDay[lastDayForTravel];
```

You can find the entire code base here on my [*github repository*](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/leetcode/sol/MinCostTicket.java). This is a good starting point for Dynamic Programming. More post coming-in on DP 😎

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.