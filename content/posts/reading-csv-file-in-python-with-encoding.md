---
title: "Reading CSV file in Python with Encoding"
date: 2026-10-27T08:14:12+05:30
draft: false
featureImage: "images/df024c_21f3d9b138934d98ad850671807a4922.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

This post will be to resolve a particular error I encountered while reading the csv files for one of my task. This csv file can contain *non-English* characters like Chinese or Japanese and hence we need to use the correct encoding format to read the file.

Lets say the csv file contains following:

```java
"Title","Id"
"2018-适用于 Windows Server 2016 的 05 累积更新，适合基于 x64 的系统 (KB4103723)","e6c7b5bd04ec"
"2021-适用于 Windows Server 2016 的 09 服务堆栈更新，适合基于 x64 的系统 (KB5005698)","840e7e93b835"
"Windows 恶意软件删除工具 x64 - v5.96 (KB890830)","cffc4d7bc390"
```

As you can see it contains windows update KB name in Chinese characters.

In order to read the content of this file, there were a lot of option given which claimed to resolve the issue. One such approach was like this:

```java
with open('kb.csv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=",")
    for line in reader:
        print(": ".join(line))
```

Here we are trying to open the csv file with the encoding set as utf-8. But this would result in following error

```java
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

I tried other approaches where they were using *read_csv()* method of *Pandas *library, but it was without any luck.

Another approaches were to change the encoding format with *cp1252* or *ISO-8591-1*. But this also couldn't solve the issue. 

#### **Solution**

At last what worked for me was changing the encoding format to UTF-16 and decoding the result. The code looks like this

```java
with open('get.csv', 'rb') as f:
    content = f.read()
    content = content.decode('utf-16')
```

Here the content once read, was decoded to utf-16 which was missing in all other approaches. As the file was read in utf-8 encoded way, we were not decoding it to get the correct output in other approaches. 

Hope this helps others also. Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.