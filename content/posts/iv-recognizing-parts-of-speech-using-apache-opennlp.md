---
title: "IV - Recognizing Parts Of Speech Using Apache OpenNLP"
date: 2026-10-27T08:14:14+05:30
draft: false
featureImage: "images/df024c_828f36bcaae74db99e5f086c33fff6f9.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will discuss on recognizing parts of speech in a given sentence using ***Apache OpenNLP*** library. This is part of the series on *learning Natural Language Processing* using Apache OpenNLP  library.

Like other models where we detect sentence, or find names, or tokenize any give string, in this post also we will be using one of the trained models which is provided by Apache Open NLP library only. 

You can find the other post discussing on detecting sentence, using named entity recognition to find names or tokenize a given string here in these posts [*Finding Sentences*](https://dynamicallyblunttech.blogspot.com/2020/07/find-sentences-using-apache-open-nlp.html), [*Finding Names using NamedEntityRecognition*](https://dynamicallyblunttech.blogspot.com/2020/07/find-names-location-or-time-in-given.html) and [*Tokenization *](https://dynamicallyblunttech.blogspot.com/2020/07/tokenization-using-apache-opennlp.html)*of the Strings.*

We will be using ***en-pos-maxent.bin*** models which detects the parts of speech and tag it based on the short names. In the below table, you can find the parts of speech and its short form name. Be sure to use the above model, else system will tag it with some other keywords.


| **Parts of Speech** | **Meaning of parts of speech** |
| --- | --- |
| *NN*​ | *Noun, singular or mass* |
| ​*DT* | *Determiner* |
| *VB* | *Verb, base form* |
| *VBD* | *Verb, past tense* |
| *VBZ* | *Verb, third person singular present* |
| *IN* | *Preposition or subordinating conjunction* |
| *NNP* | *Proper noun, singular* |
| *TO* | *to* |
| *JJ* | *Adjective* |


As we did while using the other models, here also we will perform the same steps, where we 

Load the models,

Tokenize the given strings

Tag the tokens with the relevant Parts of Speech short name.

Lets go through the code for each steps:

### **Load the Model**


We will use the ***FileInputStream ***to load the relevant models. The model is loaded to create a ***POSModel ***object.

```java
public POSModel loadModel(){
    try {
        InputStream is = new FileInputStream("src\\main\\resources\\models\\en-pos-maxent.bin");
        POSModel model = new POSModel(is);

        return model;
    } catch (FileNotFoundException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }
    return null;
}
```

### **Tokenize Given String**

Using the POSModel object created above, we have to create POSTaggerME object and then tokenize the given string.

```java
POSModel model = loadModel();
POSTaggerME posObj = new POSTaggerME(model);
WhitespaceTokenizer whitespaceTokenizer = WhitespaceTokenizer.INSTANCE;
String[] tokens = whitespaceTokenizer.tokenize(sentence);
```

### **Tagging Tokens**

Now the above tokens will be tagged and POSSample object will be created. These POSSample will contain the tokens tagged with the short name of the parts of speech. For an input like this

```java
String input = "Welcome to DynamicallyBluntTech, for our class of natural language processing.";
```

We will get an output like this, where each word will tagged with the parts of speech short name.(Given in the above table)

```java
Welcome_UH
to_TO
DynamicallyBluntTech,_NNP
for_IN 
our_PRP$ 
class_NN 
of_IN 
natural_JJ 
language_NN 
processing._NN
```

We can also monitor the performance using ***PerformanceMonitor ***class.

```java
public void performanceMonitor(POSSample sample){
    PerformanceMonitor monitor = new PerformanceMonitor(System.err, "uploaded");
    monitor.start();
    monitor.incrementCounter();
    monitor.stopAndPrintFinalResult();
}
```

This will output the below performance metrics:

```java
Average: 0.0 uploaded/s
Total: 1 uploaded
Runtime: 0.0s
```

You can find the entire code for this post as well for others, in my [Github Repository](https://github.com/ankitagrahari/chatbot/blob/master/src/main/java/com/agrahari/pos/RecognizePOS.java) link.

This concludes the series on ***Apache OpenNLP*** library. Also, it provides a command line interface to launch it directly from command prompt/terminal and run the specific commands, but we will be conclude our discussion on OpenNLP library now. 

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.