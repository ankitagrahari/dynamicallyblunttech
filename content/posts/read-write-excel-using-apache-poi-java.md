---
title: "Read/Write Excel Using Apache POI & Java"
date: 2026-10-27T08:14:13+05:30
draft: false
featureImage: "images/df024c_01ca01aeb48a49938c332028f8b412ef.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

This post will explore Apache POI library which is used to read any excel document and can also edit the excel sheets. 

Apache POI (***Poor Obfuscation Implementation***) is open source java project to read or write Microsoft excel documents. The latest version is **5.0.1**

### **Dependencies**

To include Apache POI libraries, there are two libraries to handle different version of Excel.

If we are using MS Excel '97(-2007) file format, then you will be using HSSF(Horrible Spreadsheet Format) which is pure Java implementation of the Excel '97(-2007) file format. 

```java
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.1.0</version>
</dependency>
```

And If we are using Excel 2007 OOXML (.xlsx) file format then in order to read, write, access the sheets you will be using XSSF and need to add following dependency.

```java
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.0.0</version>
</dependency>
```

You cannot use both the libraries together as, there will be some dependency which will become ambiguous on method call. Also there is another XSSF format called SXSSF which can be used when you are working with large spreadsheet and have to use low heap space. 

> SXSSF achieves its low memory footprint by limiting access to the rows that are within a sliding window, while XSSF gives access to all rows in the document. Older rows that are no longer in the window become inaccessible, as they are written to the disk

### **Composition**

Like in any excel, here also you will work on a *Workbook*, which will contains *Sheets*. So sheets can be of either *HSSF*, or *XSSF *or *SXSSF *type. Similarly, each sheet contains *Row *and each row contains *Cell*.

### **Read Excel File**

We will read a given MS Excel file, which contains stock price dataset.
* Create Workbook from Given Excel: The Workbook used here is the XSSFWorkbook which takes an Input Stream.

```java
Workbook workbook = new XSSFWorkbook(new FileInputStream(path));
```
* Create Sheet or access the existing sheet using getSheetAt() method.

```java
XSSFSheet sheet = (XSSFSheet) workbook.getSheetAt(0);
```
* Iterate over the Row to access each cell.

```java
for(Row row: sheet){...}
```
* Access Cell value using respective methods based on the data type of the cell.

```java
cell.getDateCellValue();         //Get the Date value from Cell
cell.getNumericCellValue();      //Get the Numeric value from Cell
cell.getStringCellValue();       //Get the String value from Cell
```
* Create cell if needed by using createCell() method of Row class based on index and also can set the cell value using the setter method in Cell class. Like below I am creating a new cell at index 7 and setting the value of the call as 876755.855.

```java
row.createCell(7).setCellValue(876755.855);
```

### **Write to Excel File**

To write to an excel file, we can use write() method of the Workbook class, which will write data to the Output Stream.

```java
try(OutputStream os = new FileOutputStream(path)){
    workbook.write(os);
    os.close();
}
```

In the official documentation they have used OPCPackage to handle the lifecycle of the file, but when I used the OPCpackage to write or read the file, it threw following exception on closing the package.

```java
nested exception is org.apache.poi.openxml4j.exceptions.OpenXML4JRuntimeException: Fail to save: an error occurs while saving the package : The part /docProps/app.xml failed to be saved in the stream with marshaller org.apache.poi.openxml4j.opc.internal.marshallers.DefaultMarshaller@5750bd37. Enable logging via POILogger for more details.
```

There is no exact resolution to this, it might be because of the way OPCPackage is getting accessed and converting the data because inside the OPCPackage class, it is referring to the getParts() method where it iterates over the values and then un-marshal it. 

It could be due to something else also. If you know any details do comment down your suggestion.

### **Project**

So, we will be accessing a excel file containing Stock dataset and will try to read each stocks volume, high, low, open and close price for each day, and create new columns like 
* **Typical Price** - Average of Open, High and Close price of each day
* **VP** - product of the volume and the typical price.
* **TotalVP** - summation of all the VP which came before.
* **TotalV** - summation of the Total volume.

To calculate these specific columns we have to iterate over the cells and keep the summation of the value to a third variable.

You can find the above project in my [*github repository*](https://github.com/ankitagrahari/apachepoi). You can directly check the process and the flow present in this class [*here*](https://github.com/ankitagrahari/apachepoi/blob/main/src/main/java/com/dynamicallyblunttech/apachepoi/service/ReadExcelService.java). 

The excel file is having around 800 records of stocks price which is taking around 2332ms ~ 2sec.

### References
* [*https://poi.apache.org/components/spreadsheet/quick-guide.html#ReadWriteWorkbook*](https://poi.apache.org/components/spreadsheet/quick-guide.html#ReadWriteWorkbook)
* [*http://poi.apache.org/components/spreadsheet/examples.html#common-formulas*](http://poi.apache.org/components/spreadsheet/examples.html#common-formulas)

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://www.dynamicallyblunttech.com/#:~:text=3-,Subscribe%20Form,-Stay%20up%20to) the blog if you like it.