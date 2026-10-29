---
title: "Fork-Join Framework in Java"
date: 2026-10-27T08:14:21+05:30
draft: false
featureImage: "images/df024c_a0d024bca07c43a5aa61a451c20ac021.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

This post will discuss on the Fork Join framework introduced in Java 7. It utilizes the maximum available processors to compute any recursive task. So e.g. calculating the Fibonacci series or finding a number in the huge array can be done in very less time.

## How it Works

Lets understand some key points in this framework

Fork means spawning a new task.

Join means to join the pending task output.

Fork/Join uses the ***Divide and Conquer*** which divides the entire dataset into small chunks for computation or applying any specific logic. Once each task is computed independently, it will merge the output of the computation to get the final result.

It runs all the forked tasks in parallel using the available capacity of your machine on which it is running.

To run the tasks in parallel, it uses the number of processors available to JVM which is *Runtime.getRuntime().availableProcessors()* number of threads.

Each of these threads have ***double ended Queue (De-queue)***. In a de-queue you can add or remove an elements from the head or tail.

Using de-queue, it applies the ***work-stealing algorithm***, where if there are no tasks for  a thread to execute, it will steal the tasks from other threads.

This approach ensures efficient execution of a big task, utilizing the available processors of your machine.

## Classes

*ForkJoinPool *class* *is a common shared thread pool which can be accessed using *commonPool()* static method. This will invoke classes which extends *RecursiveAction *or *RecursiveTask*. These Recursive classes implements *ForkJoinTask *interface.

We can return a specific value (like *Future *in *Executor framework*) from class extending *RecursiveTask *(~*Callable*) and class extending *RecursiveAction *(~*Runnable *) will not return any values. These classes have *compute()* method, which holds the logic for your tasks.

With fork/join, there will be a way to solve any problem for certain size threshold. But if the threshold is crossed it follows this order
* Create two tasks,
* Fork the first task
* Call compute() on the second task
* Call join() on the first task.

This order is mandatory to follow. Here first the task is forked and we compute the task and then join it using the join() method. We will go through two examples to understand this better.
* Finding the frequency of duplicate element in an Array
* Finding the Fibonacci number at a given index.

## Problem I - Frequency of Duplicate Element in an Array

The problem statement is to find an element in an array and how many times it is duplicated.

Now here the array size can be anything, ranging from 1 to millions.

Here the logic will be to maintain the start and end index of the array. 

```java
private static final int THRESHOLD = 47;
int[] arr;
int start, end, toFind;
```

There will be one part where we put the logic to get the duplicate element frequency like this

```java
for (int i = start; i <= end; i++) {
    if (toFind == arr[i]) {
        count++;
    }
}
System.out.println("count:"+ count 
        + " from start:"+ start 
        +" and end:"+ end);
return count;
```

And other part will be when the size of the Array is crossing the Threshold limit. 

I have put 47 as threshold, because it is something used in the Sort method of Arrays class.

```java
CountDuplicate task1 = new CountDuplicate(arr, 0, end/2, toFind);
CountDuplicate task2 = new CountDuplicate(arr, (end/2)+1, arr.length-1, toFind);

task1.fork();
return task2.compute() + task1.join();
```

*CountDuplicate *is the class which computes the frequency of the duplicate elements in a specific index range of the given array.

And in the main method, we will initiate the *ForkJoinPool *and the invoke the *CountDuplicate *task. The invoke method will return an Object. It can return an Integer if while specifying it is given as the *RecursiveTask<Integer>*.

```java
ForkJoinPool pool = ForkJoinPool.commonPool();

int[] arr = {1, 4, 2, 1, 2, 1, 23, 1, 5, 5, 2, 4, 9, 2, 8, 3, 5, 1, 0, 6, 3, 1};
CountDuplicate task = new CountDuplicate(arr, 0, arr.length-1, 1);
Integer count = pool.invoke(task);
System.out.println(count);
```

The above print method will print the count of element 1 which is repeated 6 times in the given array.

## Problem II - Fibonacci Number at an Index

Here the problem statement is to find the Fibonacci number at a given index starting from 0. The way we calculate the Fibonacci number is to add the previous two number from the list. Now every element can be computed in subtasks.

The first part is to calculate the Fibonacci number if the number is below the Threshold level

```java
Integer computeDirectly(){
    int i=2;
    int a=0, b=1, curr;
    if(to<=1)
        return 1;

    while(i<=to){
        curr = a + b;
        a = b;
        b = curr;
        i++;
    }
    return b;
}
```

Then the other part will be to get the recursive logic working if the index is more than the Threshold level.

```java
Fibonacci task1 = new Fibonacci(to-1);
Fibonacci task2 = new Fibonacci(to-2);

task1.fork();
return task2.compute() + task1.join();
```

Here task1 calculates the Fibonacci at *n-1* index and task2 will calculate the fibonacci at *n-2* index. The final result will be the summation of both the values.

***NOTE:*** You can notice in both the example above that the fork() is called on the first task to create the subtask, then the compute() is called on the second subtask to recursively process it and then the join() on the first task again. The join() method should be called at last because it will block the next task from being processed until the result is returned. 

The *Arrays.parallelSort()* method also using this Fork/Join framework to sort the arrays. You can find the parallel sort example [*here*](https://github.com/ankitagrahari/Tryouts/blob/master/src/main/java/com/array/sort/ArraySort.java). 

You can also find the entire code base in my [*github repository*](https://github.com/ankitagrahari/Tryouts/). You can refer to the solution of problem1 [*here *](https://github.com/ankitagrahari/Tryouts/blob/aecfa1c9737eb70a4dabb48bc342a50fa915ef56/src/main/java/com/array/ForkJoinT.java#L63)and for problem 2 [*here*](https://github.com/ankitagrahari/Tryouts/blob/aecfa1c9737eb70a4dabb48bc342a50fa915ef56/src/main/java/com/array/ForkJoinT.java#L23).

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.