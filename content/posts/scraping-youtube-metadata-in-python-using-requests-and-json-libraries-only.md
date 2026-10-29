---
title: "Scraping Youtube Videos - Using Python's Requests & JSON Libraries"
date: 2026-10-27T08:14:17+05:30
draft: false
featureImage: "images/df024c_9caecd0715d949b39ff82979a6ff9c4a.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will look into ***Scraping any Youtube video*** metadata to get the views, likes, dislikes, published date etc. information using ***Python***. We will not be using any third party libraries which parse the HTML like Beautiful Soup.

### **Problem Statement:**

To fetch Youtube video metadata like its View count, Likes/Dislikes count, Published Date, Title of the video etc. without using any 3rd party libraries which parses HTML or Javascript. To add to that, we will not be using the ***Youtube API*** to fetch data.


### **Approach**

There are multiple ways to fetch the data from youtube, or any other website. In order to parse the website, *Beautiful Soup* library can be used. But we will use even simpler way to get out required data-set. 

We will be using python ***requests*** library to get the page source of the youtube video link and ***json ***library to parse the text to Json object.

There is a pattern to any Youtube video page source. When you open the page source, search for '***ytInitialData***' in the page source, and you will find that in the script tag, this variable is assigned with a Json. Only problem is that, we cannot use it as it is, and needs some manipulation. So basically, we will be manipulating strings in Python to get the data we want.

To get the exact Json, I need to find the start and end Index of this Json from the page source. Lets try it out for any Youtube video you are watching. 

**F**or getting the page source of any website, you can right click on the website and click on the *View Page Source *option

**S**earch for ***ytInitialData*** in the tab where the page source is open. Actual string will be like this:

### Code

Lets code it in Python step by step:

You need to import ***json ***and ***requests ***libraries as the prerequisite step.

```java
import json
import requests
```

**F**rom the given video link, get the page source using request library and save the text format to some variable

```java
def import_video_data(URL):
    print('Fetching Video page source using URL ' + URL)
    # window["ytInitialData"] =
    page_source = requests.get(URL)
    page_source = page_source.text
```

**E**xtract the json data from the page source of the given video link.

```java
start_index = page_source.find('ytInitialData')
    tmp = page_source[ start_index+17:]
    end_index = tmp.find('}};')
    tmp = tmp[:end_index] + '}}'
    return tmp
```

**N**ow, parse the string returned as ***Json ***object using ***Json*** library. Here we are using ***loads()*** method to convert the ***Json*** string into a dictionary.

```java
def parse_json(json_data):
    json_dict = json.loads(json_data)
    return json_dict
```

The Json we fetched in the last step will look something like this:

**F**rom the Json, we can now extract any information we want. 

The basic manual way to get the title, video Id, View Count, Likes, Dislikes, their short form and its published date are displayed here:

***For Video Id***:

```java
video_id = yt_json['currentVideoEndpoint']['watchEndpoint']['videoId']
print('VideoId:' + video_id)
```

***For Title***:

```java
title = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['title']['runs'][0]['text']
print('Title:'+ title)
```

***For View count and its short form***:

```java
views = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']

short_views = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['viewCount']['videoViewCountRenderer']['shortViewCount']['simpleText']

print('Views:' + views + ' in short:'+ short_views)
```

***For Likes and its short form***:

```java
likes = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']

likes_inshort = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['simpleText']

print('Likes:'+ likes+' in short:'+ likes_inshort)
```

***For Dislikes and its short form***:

```java
dislikes = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']

dislikes_inshort = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['defaultText']['simpleText']

print('Dis-Likes:'+ dislikes+' in short:'+ dislikes_inshort)
```

***For Published Date***:

```java
published_date = yt_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['dateText']['simpleText']

print('Published Date:'+ published_date)
```

The output of the above code will be look like this:

#### **Fetching Video stats (as per date 3rd August, 2020)**

**URL: **[*https://www.youtube.com/watch?v=JRtgXN-bwGE*](https://www.youtube.com/watch?v=JRtgXN-bwGE)
**VideoId: ***JRtgXN-bwGE*
**Title: ***Honest Review | Raat Akeli Hai, Shakuntala Devi & Lootcase | MensXP*
**Views: ***282,420 views in short:282K views*
**Likes: ***21,343 likes ****in short****: 21K*
**Dis-Likes: ***413 dislikes ****in short****:413*
**Published Date: ***1 Aug 2020*

Using the above technique, you will have the Json and can extract any data which is required. You can find this entire code on my [*Github Repository*](https://github.com/ankitagrahari/pyprojects/blob/master/com/agrahari/YTScraping.py).

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.