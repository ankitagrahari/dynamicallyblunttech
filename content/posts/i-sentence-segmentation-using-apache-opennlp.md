---
title: "I - Sentence Segmentation Using Apache  OpenNLP"
date: 2026-10-27T08:14:26+05:30
draft: false
featureImage: "images/df024c_828f36bcaae74db99e5f086c33fff6f9.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post, we will discuss on how to find sentences in a block of text, which can be a paragraph or an entire book. We will be using ***Apache OpenNLP*** library with Java. 

Objective here is to learn ***Apache OpenNLP*** library and effectively use it in processing any text. We will start with Sentence Segmentation and will post more on the usage of its services in further posts.

### **Apache Open NLP**

Apache OpenNLP is an open source library, which is used to process ***Natural Language Text***. It provides services such as sentence segmentation, tokenization, part of speech tagging, named entity extraction, chunking, parsing etc. Its a powerful library which comes with its own set of models, which I will be using in our examples. You can find the set of models from here [http://opennlp.sourceforge.net/models-1.5/](http://opennlp.sourceforge.net/models-1.5/)

For this post, we will setup our project and will start with Sentence Segmentation.

### **Maven Dependencies**

For using the Apache Open NLP library, we can either download the latest zip files from [https://opennlp.apache.org/download.html](https://opennlp.apache.org/download.html). If you are downloading the zip files, once extracted, you have to set it in your classpath, else use maven dependencies in your project. 

Add below maven dependencies in your project 

```java
<dependencies>
    <dependency>
        <groupId>org.apache.opennlp</groupId>
        <artifactId>opennlp-tools</artifactId>
        <version>1.9.2</version>
    </dependency>
    <dependency>
        <groupId>org.apache.opennlp</groupId>
        <artifactId>opennlp-uima</artifactId>
        <version>1.9.2</version>
    </dependency>
</dependencies>
```

### **Sentence Segmentation**

The objective here is to find all the sentences in a given block of text, it could be paragraph or an entire book. 

We will use one of the existing models **en-sent.bin***, * to detect the sentences in the block of text. We will load the binary file in the ***InputStream ***and pass this stream object to ***SentenceModel ***class which belongs to ***opennlp.tools.sentdetect*** package. The model we used is converted to ***SentenceModel*** object.

```java
//Load the sentence detection model
InputStream is = new FileInputStream("src\\main\\resources\\models\\en-sent.bin");
SentenceModel modelObj = new SentenceModel(is);
```

Now, load this model object to the ***SentenceDetectorME*** class which is also from same package. This class holds the methods which helps in finding the end of sentence character in a string. It splits the raw text to sentences.

### ***sentDetect()***

This method will detect all the sentences from the given text.

```java
//Break raw text into sentences
SentenceDetectorME detectorME = new SentenceDetectorME(modelObj);
String[] detectedSen = detectorME.sentDetect(rawText);
System.out.println("All sentences detected are:");
System.out.println(Arrays.toString(detectedSen));
```

Once all the sentences are detected, we are printing it using the Arrays.toString() method. The output of the above print will be something like this

```java
All sentences detected are:
    [Hi. How are you?, 
    Hope everything is going well., 
    Welcome to OpenNLP Lesson1., 
    We will try to understand Open Apache NLP for sentence detection]
```

### ***sentPosDetect()***

The ***SentenceDetectorME ***also provide ***sentPosDetect()*** method to get the position of the detected sentence. It return ***Span*** class which keep the start and end of the detected sentences. ***Span ***class had ***getStart()*** and ***getEnd()*** methods.

```java
//Find position of all sentences
Span[] spans = detectorME.sentPosDetect(rawText);
System.out.println("Positions of all detected sentences:");
for(Span span: spans){
    System.out.println(span);
}
```

The above part of code produce the following output:

```java
Positions of all detected sentences:
    [0..16)
    [17..47)
    [48..75)
    [76..140)
```

### ***getSentenceProbabilities()***

It also have ***getSentenceProbabilities()*** method which gives the probabilities of each sentence for the most recent call to ***sentDetect()***. If not applicable, then an empty array is returned.

```java
//Getting the probabilities of the last sendDetect method call for the sentences
double[] probabilities = detectorME.getSentenceProbabilities();
System.out.println(Arrays.toString(probabilities));
```

The above code will produce the following output:

```java
[0.9240246995179983, 0.8808767380536497, 0.9899713160931164, 1.0]
```

This is a very simple exercise to start with ***Apache Open NLP*** library. You can find the above code example in my [Github repository](https://github.com/ankitagrahari/chatbot/tree/master/src/main/java/com/agrahari/sentenceDetection). As of now, we are using the existing models which comes with Apache Open NLP only.

For the next step in learning to Natural Language Processing, .i.e. to tokenize any given string using ***Apache OpenNLP*** library is discussed in this post [Tokenization Using Apache OpenNLP](https://www.dynamicallyblunttech.com/post/ii-tokenization-using-apache-opennlp).

### References
* [https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html](https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html)
* [https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html](https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html)
* [https://www.tutorialspoint.com/opennlp/index.htm](https://www.tutorialspoint.com/opennlp/index.htm)
* [http://opennlp.sourceforge.net/models-1.5/](http://opennlp.sourceforge.net/models-1.5/)

Do let me know your thoughts if anything specific should be included and also do provide your comments/feedback down below.