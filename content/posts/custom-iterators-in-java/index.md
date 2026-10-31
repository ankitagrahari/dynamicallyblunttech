---
title: "Custom Iterators in Java"
date: 2026-10-27T08:14:30+05:30
draft: false
tags: ['Iterators', 'Java']
categories: ['Interview', 'Java']
showReadingTime: true
---

This is a bit embarrassing to start with, but lets say I got this question and was quite dumb stuck on how to write a custom iterator. Seems simple at that point, but couldn't exactly curate the process of developing a custom iterator which would return the second element instead of the next element.

So this post will be about ***Embarrassment***.

Lets start with Iterators.

### **Iterator **

Iterators are something, using which we iterate over a given collection of elements given in Java. So, lets says the list of Strings objects can be iterated over by *list.iterator()*.  

Now we know what an *iterator *is, we should be aware of what *Iterable *interface is. 

### **Iterable Interface**

This was introduced in Java 1.5. It makes custom data structure works with the enhanced for-each loop. It has only one method *iterator() *to be implemented. 

So, we know a bit on Iterable and more on *Iterator*. These scenarios or questions are more common when you start creating a custom data structure, and think about how to make this easily iterate-able.  

We will just do the same and without any ***embarrassment***.

### **Create Our Own Data Structure**

In this part, we will create a new data structure which is called *CustomList*. It works like List class, but the iterator implemented in *CustomList *will return me *second element* on every call.  

This *CustomList *will implement *Iterable of Type T*, which will allows us to implement the iterator that goes with this custom data structure. It will work on a List, and utilize the List methods to return the first and last element. And implementation for *add()* method to insert new element to the list.

```java
class CustomList<T> implements Iterable<T> {

    List<T> list;
    CustomList(List<T> list) {
        this.list = list;
    }

    public void add(T s) {
        list.add(s);
    }

    public T getFirst() {
        return list.get(0);
    }

    public T getLast() {
        return list.get(list.size() - 1);
    }

    public Iterator<T> iterator() {
        return new SecondIterator();
    }

    //Inner Class
    class SecondIterator<T> implements Iterator<T> {
    .
    .
    .
    .
    }

}
```

As you noticed, the *iterator()* method is returning a custom iterator called *SecondIterator*. 

Now here, we have to implement the *SecondIterator*, such that it returns the second element. And this *SecondIterator *will be the inner class of my *CustomList *data structure. 

So the next piece of code is for *SecondIterator *which implements the *Iterator *Interface, thus making sure that the custom iterator should have *next() *and *hasNext()* methods implemented.

```java
class SecondIterator<T> implements Iterator<T> {

    private int current = 0;
    private int size = list.size();

    //Return true if the second element exists
    @Override
    public boolean hasNext() {
        return size - current > 1;
    }

    //Return Second element from the list
    @Override
    public T next() {

        if(!hasNext())
            throw new NoSuchElementException();
        T t = (T) list.get(current);
        current+=2;
        return t;
    }
}
```

Here, we need to work on the index, in order to be specific about where the current pointer is. 

So lets say, I am at the 4th index of my custom data structure, and now if I call *next()*, it should always give me the 6th index element (because we are implementing *SecondIterator *and not a normal Iterator). And that's why, we will have a variable to refer the correct element, when we call *next()* on it. 

Also this makes my job easier for *hasNext()*, because it doesn't have to check if it is at 2nd index, or 4th index or 6th index etc....At any moment, I will check the difference of the actual size of the list and the current index, which should be greater than 1, in that case the *hasNext()* should always be true, because it will always have the at-least 2 elements pending. 

Similarly, my *next()* method will return *NoSuchElementException()*, if there are no elements present. Else, it will get the value at that current index from the list and increment the current index pointer by 2, to always get the second element from the current index. 

Here, I can create Nth-Iterator also, which will be give me elements on the Nth index from the current index, by just incrementing the value by N (Also, the same changes need to go to the *hasNext()* method.)

Now, after all these explanations on this tricky question, which I couldn't do when asked, lets try our new Custom Iterator and find out if it is working or not. 

### **Main**

Here is the Main class which will create a List of Strings, and pass it to the custom data structure. And then iterate using the for-each on the *CustomList *to see if we are getting the second element always from the current index or not. 

See, here the Iterable interface will come to work. 

```java
public class Main{
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("a"); //1st Element
        list.add("b"); 
        list.add("c"); //Second from 1st Element
        list.add("d"); 
        list.add("e"); //Second from 3rd Element
        list.add("f"); 
        list.add("g"); //Second from 5th Element
        list.add("h"); 

        CustomList<String> customList = new CustomList(list);
        for(String s: customList){
            System.out.println(s);
        }
    }
}
```

Now, when we executed the enhanced *for-each* loop, it didn't threw any error and was able to print the second element as was implemented in the custom iterator.

This is such a good question to learn how the iteration over the collection works. Also, I would recommend to try it out yourself, somewhere we all will get stuck, but then that's how you will find how good this question is. Also, it will help in avoiding the ***embarrassment*** phase and a curious night over a blog post. 

Hope this post will bring a smile and lots of learning. You can refer to my [*Github Repository*](https://github.com/ankitagrahari/Tryouts/tree/master/src/main/java/com/custom/iterator) for the full code base of this example. 

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.