---
title: "III - Named Entity Recognition - Apache OpenNLP"
date: 2026-10-27T08:14:29+05:30
draft: false
tags: ['Apache', 'OpenNLP']
categories: ['Apache', 'NLP']
showReadingTime: true
---

In this series of learning Natural Language Processing with ***Apache OpenNLP*** library in Java, we will discuss on ***NamedEntityRecognition***, which can identify names, places, locations etc. in any given string.

In ***Apache OpenNLP*** library, ***NamedEntityRecognition*** uses predefined trained models which is used to recognize names or date or places or location etc. in the given string. These models are:
* *en-nerdate.bn,*
* *en-ner-location.bin*
* *en-ner-organization.bin*
* *en-ner-person.bin*
* *en-ner-time.bin*

Like in previous posts on [*SentenceDetector*](https://dynamicallyblunttech.blogspot.com/2020/07/find-sentences-using-apache-open-nlp.html)[*** ***](https://dynamicallyblunttech.blogspot.com/2020/07/find-sentences-using-apache-open-nlp.html)and [*Tokenization*](https://dynamicallyblunttech.blogspot.com/2020/07/tokenization-using-apache-opennlp.html), here also we have to identify the models which we want to use, load the model, and use the find method of the ***NameFinderME ***class to find the specific name, location or place as per the models used.

Lets start with loading the person model:

```java
InputStream is = new FileInputStream("src\\main\\resources\\models\\en-ner-person.bin");
TokenNameFinderModel model = new TokenNameFinderModel(is);
```

The model is loaded in ***TokenNameFinderModel ***class.

Use this model object to create ***NameFinderME ***object. The find method of this class will take an array of string as input which will return an array of Span object. This array will have all the matching names, places or location etc as per the models used. 

```java
NameFinderME finder = new NameFinderME(model);
String[] words = text.split(" ");

Span[] spans = finder.find(words);
```

Use the ***Span's getStart()*** and ***getEnd()*** methods to get the indexes of the matching words.

So for an input like this:

```java
NamedEntityRecognition ner = new NamedEntityRecognition();
String sentence = "Indian Names could either Abhay or Ankit and other options are Charles and Michael";
ner.nameFinder(sentence);
```

This will be the output:

```java
[11..12) person---Charles
[13..14) person---Michael
```

If you want to find the places, location or time, then use the respective models.

## Limitation of these Models:

The models for names *en-ner-person.bin  *will work on a small subset of the name, as I tried with Indian names as input, but it only recognizes the western names. This also is limited to some names.

For the entire codebase, you can visit my [***Github repository***](https://github.com/ankitagrahari/chatbot/tree/master/src/main/java/com/agrahari/ner). 

References
* [https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html](https://opennlp.apache.org/docs/1.9.2/manual/opennlp.html)
* [https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html](https://opennlp.apache.org/docs/1.9.2/apidocs/opennlp-tools/index.html)
* [https://www.tutorialspoint.com/opennlp/index.htm](https://www.tutorialspoint.com/opennlp/index.htm)
* [http://opennlp.sourceforge.net/models-1.5/](http://opennlp.sourceforge.net/models-1.5/)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.