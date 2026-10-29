---
title: "Exploring Government's Cowin APIs"
date: 2026-10-27T08:14:14+05:30
draft: false
featureImage: "images/df024c_0fee975913424b4eb20fba84efaa6260.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will be looking into the CoWIN APIs which GoI has published during the covid period where the third party app can utilize the APIs to create there own app.

We used only few API from the public list and created a ***Spring boot application*** which will get me the list of all the available slots for either the old or young people based on their age on a given date and list of pin codes. 

You can refer to the government API from here: [https://apisetu.gov.in/public/api/cowin#/](https://apisetu.gov.in/public/api/cowin#/)

Also, you can find the Github link for all these services and the application at the end of this post.

## Services

We have three services which will be listed here with its descriptions:

### 1. Get all available slots on a given date for given pincode area

**Service Name**: ***getAvailabilityByPinAndDate***

**Input**: Pincode, Date

**Output**: Sessions object

**Description**: Get all the available slots on a given date for a given pincode.

**Endpoint**: cowin/pin=pincode1/date=date1

    e.g.: http://localhost:8083/cowin/pin=221001/date=07-05-2021

**Sample Output**:

### 2. Get all available slots for Young people on a given date and for given list of pincodes

**Service Name**: ***getAvailabilityByPinAndDateForYoung***
**Input**: List of Pincodes, Date
**Output**: Sessions object
**Description**: Get the available slots for Young (age between 18 to 45) on a given date for a list of given pincodes.
**Endpoint**: cowin/young/pins=pincode1,pincode2,pincode3/date=date1

    e.g.: http://localhost:8083/cowin/young/pins=431801,431802,431803/date=07-05-2021
**Sample Output**:

### 3. Get all available slots for Old people on a given date and for given list of pincodes

**Service Name**: ***getAvailabilityByPinAndDateForOld***
**Input**: List of Pincodes, Date
**Output**: Sessions object
**Description**: Get the available slots for Old(age 45+) on a given date for a list of given pincodes.
**Endpoint**: cowin/old/pins=pincode1,pincode2,pincode3/date=date1
    e.g.: http://localhost:8083/cowin/old/pins=221001,221002,221003,221004,221005/date=07-05-2021
**Sample Output**:

Github Link: [*https://github.com/ankitagrahari/CowinCo*](https://github.com/ankitagrahari/CowinCo)


You can find the Model classes for models which are made public by government. I will try other services as well and will update the same Github repository.

If you find the post helpful, do give a thumbs up and also share your feedback and topics that I should  covered. 


If you are looking for some COVID19 resources, follow this post [COVID19-Resources](https://dynamicallyblunttech.blogspot.com/2021/04/covid19-resourceswebsites.html) for all the websites/application or twitter search format