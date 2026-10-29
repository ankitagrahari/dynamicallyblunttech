---
title: "II - Tokenization using Apache OpenNLP"
date: 2026-10-27T08:14:14+05:30
draft: false
featureImage: "images/df024c_92241e7958db4302be98777f82fd896f.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will create tokens of the given string using **Apache OpenNLP** library.

This post is a continuation of the previous post [**Find Sentences using Apache Open NLP**](https://www.dynamicallyblunttech.com/post/i-sentence-segmentation-using-apache-opennlp)**. **Refer to this post first for the setting up your project with Apache OpenNLP library. In the previous post we used ***SentenceDetecterME***, ***SentenceModel***, and ***Span ***class of the openNLP library.

Apache OpenNLP library provides the ***SimpleTokenizer***, ***WhitespaceTokenizer ***and ***TokenizerME ***which will use the normal process to tokenize by splitting the string either on whitespace or using some already trained models. These classes doesn't expose their constructors, so we have to use ***INSTANCE ***to get the instance of these classes.

## **SimpleTokenizer**

This will use split the sentences into each word or any exclamation, dot, comma etc used. It provides two methods to tokenize a given string. We will try both the methods.
* First step is to get the instance of the SimpleTokenizer

```java
//Get the Simple Tokenizer Instance
SimpleTokenizer tokenizer = SimpleTokenizer.INSTANCE;
```
* Use this object to get the tokenize() method which will take the string as input.

```java
//Call the tokenize method
String[] tokens = tokenizer.tokenize(text);
```
* Print the tokens and the output will be

```java
//Print the tokens
System.out.println(Arrays.toString(tokens));

Hi              .               How
are             you             ?
Hope            everything      is
going           well            .
Welcome         to              ChatBot
Lesson1         .               We
will            try             to
understand      Open            Apache
NLP             for             sentence
detection
```
* There is another ***tokenizePos***() method which will print the position of the tokens. Its return type is an array of ***Span*** object.

```java
Span[] spans = tokenizer.tokenizePos(text);
for(Span s: spans){
    System.out.println(s);
}
```

	The output of the above statement will be like this:

```java
[0..2)
[2..3)
[4..7)
[8..11)
[12..15)
[15..16)
```

## **Whitespace Tokenizer**

This tokenizer will split the sentence based on white space. It also has two methods to returns tokens as string array and another ***tokenizePos()*** method which return an array of ***Span*** objects.

Here is the code to get the ***WhiteSpaceTokenizer ***instance and printing the tokens and their position.

```java
//Get the Simple Tokenizer Instance
WhitespaceTokenizer tokenizer = WhitespaceTokenizer.INSTANCE;

//Call the tokenize method, this will split based on spaces
String[] tokens = tokenizer.tokenize(text);

//Print the tokens
for(String s: tokens){
    System.out.println(s);
}

Span[] spans = tokenizer.tokenizePos(text);
for(Span s: spans){
    System.out.println(s);
}
```

The output will be like this:

```java
Hi.            How               are
you?           Hope              everything
is             going             well.
Welcome        to                ChatBot
Lesson1.       We                will
try            to                understand
Open           Apache            NLP
for            sentence          detection

[0..3)           [4..7)              [8..11)
[12..16)         [17..21)            [22..32)
[33..35)         [36..41)            [42..47)
[48..55)         [56..58)            [59..66)
[67..75)         [76..78)            [79..83)
[84..87)         [88..90)            [91..101)
[102..106)       [107..113)          [114..117)
[118..121)       [122..130)          [131..140)
```

The implementation is similar to the ***SimpleTokenizer***.

## **TokenizerME**

This class will create tokens based on the trained model it is using. It loads a particular model to TokenizerModel and then loads it to this class. 
* Load the trained model into ***TokenizerModel*** object. I have used an existing model which comes with ***Apache OpenNLP*** library.

```java
//Load the token models
InputStream is = new FileInputStream("src\\main\\resources\\models\\en-token.bin");
TokenizerModel model = new TokenizerModel(is);
```
* This class has three methods ***tokenize()***, ***tokenizePos()*** and ***getTokenProbablities()*** methods. It can used like this:

```java
//Print the tokens
for(String tokens: tokenizerME.tokenize(text)){
    System.out.println(tokens);
}

//Get the position of the tokens
Span[] spans = tokenizerME.tokenizePos(text);
for(Span span: spans){
    System.out.println(span);
}

//Get the token probabilities
double[] prob = tokenizerME.getTokenProbabilities();
for(double s: prob){
    System.out.println(s);
}
```

The output of the above code will be like this:

```java
Hi              .               How 
are             you             ?
Hope            everything      is
going           well            .
Welcome         to              ChatBot
Lesson1         .               We
will            try             to
understand      Open            Apache 
NLP             for             sentence
detection

[0..2)      [2..3)      [4..7)
[8..11)     [12..15)    [15..16)
[17..21)    [22..32)    [33..35)
[36..41)    [42..46)    [46..47)
[48..55)    [56..58)    [59..66)
[67..74)    [74..75)    [76..78)
[79..83)    [84..87)    [88..90)
[91..101)   [102..106)  [107..113)
[114..117)  [118..121)  [122..130)
[131..140)
You can find the code here in the Github repository.
```

### References
* [https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html](https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html)
* [https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html](https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html)
* [https://www.tutorialspoint.com/opennlp/index.htm](https://www.tutorialspoint.com/opennlp/index.htm)
* [http://opennlp.sourceforge.net/models-1.5/](http://opennlp.sourceforge.net/models-1.5/)

This concludes the tokenization using ***Open ApacheNLP*** library in Java. This will be another step in using natural language processing. 

Also, please comment down with your feedback or any suggestions.