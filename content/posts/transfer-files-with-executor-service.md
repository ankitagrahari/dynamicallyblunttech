---
title: "Transfer Files with Executor Service "
date: 2026-10-27T08:14:29+05:30
draft: false
featureImage: "images/df024c_ee69317a2af845d9b542883d88c3179a.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will move all files from one directory to another using Java's Executor Service and will also discuss on how we can enhance the entire process.

To move files from one directory to another:
* List all files in the source directory
* Create a main class which will call the threads to process all the files in given directory.

So lets start developing our main class which will hold the skeleton of the program to call executor thread which will in turn transfer all files from one directory to another.

### **Main **
* Checks if the source and target directory exists
* Get the stream of Path using *Files.walk()* on the source directory.
* For each file in the Stream of paths, it puts an entry into the *ConcurrentHashMap *declared globally.
* Calls the method which will in-turn call the thread using Executor Service.

```java
private static final Integer THREADS = 10;
public static ConcurrentHashMap<String, Integer> filesMap = new ConcurrentHashMap<>();

public static void main(String[] args) {
    File workDir = new File("src\\main\\resources\\source");
    if(workDir.exists() && workDir.isDirectory()) {
        try {
            Stream<Path> paths = Files.walk(Paths.get("src\\main\\resources\\source"), 1);
            paths.forEach(path -> {
                if(!path.toFile().getName().equalsIgnoreCase("source"))
                    filesMap.put(path.toFile().getName(), 0);
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        File collectDir = new File("src\\main\\resources\\target");
        if (collectDir.exists() && collectDir.isDirectory()) {
            MainClass.moveUsingMultiThread();
        }
    }
}
```

### **Executor Method**
* Set a fixed thread pool using *newFixedThreadPool()* method of the *Executors* class.
* It creates five *ProcessFiles* threads and executes it using *ExecutorService* object.
* It calls *shutdown()* of *ExecutorService *once all the thread execution is done. It will wait using the while loop, until all the threads are completed and then print the message "Finished all threads".

```java
public static void moveUsingMultiThread(){
    System.out.println("Running MultiThreaded Application to Move files         
          from source to target");
    ExecutorService executorService = Executors.newFixedThreadPool(
          THREADS);

    for(int i=0; i<5; i++) {
        Runnable worker = new ProcessFiles();
        executorService.execute(worker);
    }
    executorService.shutdown();

    while (!executorService.isTerminated()) {
        // Wait until all threads are finished
    }
    System.out.println("Finished all threads");
}
```

### **Executor Thread**

This is my Runnable thread which 
* Iterate over the *ConcurrentHashMap*,
* Move the files from source to target using *Files.move()*, and
* Remove the entry from *ConcurrentHashMap*.

```java
if(null!= MainClass.filesMap && MainClass.filesMap.size()>0){
    for (Map.Entry<String, Integer> entry :MainClass.filesMap.entrySet()){
        synchronized (this) {
            System.out.println(Thread.currentThread().getName()
                  +"---" + entry.getKey()
                  +"---" + MainClass.filesMap.get(entry.getKey()));
            try {
                //Multiple checks for multi threads
                if (null != MainClass.filesMap 
                    && null!=MainClass.filesMap.get(entry.getKey()) 
                    && MainClass.filesMap.get(entry.getKey()) == 0) {                        
                    Files.move(
                        Paths.get(
                            "src\\main\\resources\\source" 
                            + File.separator + entry.getKey()
                        ),
                        Paths.get(
                            "src\\main\\resources\\target" 
                            + File.separator + entry.getKey()
                        )
                    );
                    MainClass.filesMap.remove(entry.getKey());
                }
            } catch (NoSuchFileException nsfe) {
                if (!new File("src\\main\\resources\\target" +
                    File.separator + entry.getKey()).exists()) {
                    nsfe.printStackTrace();
                }
            } catch (NullPointerException npe){
                //There might be a case when some threads will 
                // try to access get on fileMap,
                // which will be empty at that time. 
                // Hence, on NPE if the map is not empty, then
                // throw error, else skip
                if(null!=MainClass.filesMap
                        && MainClass.filesMap.size()>0){
                    System.out.println("FileName:"+entry.getKey()
                        +" Value:"+entry.getValue());
                    npe.printStackTrace();
                }
            }
```

The *NoSuchFileException *mentioned above is handled in the catch block.


This will move all the files from source to target directory using 5 *ProcessFiles *threads and a *thread pool size* of 10 threads.

While trying this out, we came to a interesting aspect, where the entire list of files can be divided into multiple list (equal to the number of threads) and then passing the sub-list to each thread. By using this logic, you can avoid all the collision because each thread will work on different set of files.

##### **Limitations**
* While using the above logic, there are chances that one thread is accessing one file while other thread has already moved it. So, we will get *NoSuchFileException*.
* While moving the files, there could be a case where one thread accessed one file from the directory, but another thread moved the same file in the target directory. In these cases, we can encounter *NullPointerException*.

##### **Resolutions**
* For *NoSuchFileException*, we can check if the same file exists in the target directory, and if not then throw the error.
* For *NullPointerException*, we will keep a Map (in this case a *ConcurrentHashMap*) to keep the records of the files existing in the directory. And as the threads move the files to target directory, we will remove the entry from the Map.

### **Fixing the Limitations**

So in order to fix the limitations, the *ProcessFiles *runnable thread need to work on a limited number of files. And when I say limited number of files, each thread will work on a segment of the list of files collected from the source directory.

This is where the List partition comes into picture. As part of Main class, now we will partition the file list into multiple list (in our case, 3 sub-list will be created from the main list of files). 

The *ProcessFiles *is now changed to accept a list of file as input parameter and we are using *submit()* of the *ExcecutorService *which can return a *Future* object.

```java
List<List<File>> partitionedLists = partitionListOfFiles(fileList, 3);
for(List<File> files : partitionedLists) {
    Runnable worker = new ProcessFilesUsingListPartition(files);
    executorService.submit(worker);
}
```

The partition of list is done using the *subList *method of the List interface:

```java
private static List<List<File>> partitionListOfFiles(List<File> files, final int breakInto) {
    List<List<File>> fileParts = new ArrayList<>();
    final int totalFiles = files.size();
    for (int i = 0; i < files.size(); i += breakInto) {
        fileParts.add(
                new ArrayList<>(files.subList(
                    i, 
                    Math.min(totalFiles, i + breakInto))
                )
        );
    }
    return fileParts;
}
```

Here, lets say you have 10 files and you are partitioning the list into 2 parts, then *breakInto *parameter will be 5. 


This will actually speed up the task of moving the files from one directory to another. You can vary the size of sub-list of files, based on the number of files you have. So that the program will use same amount of threads as the number of partitioned list of files.

You can find the whole code base here in my Github repo [*ExecutorServiceExample*](https://github.com/ankitagrahari/Tryouts/tree/master/src/main/java/com/threads/moveFiles)*.*

Please do suggest more content topics of your choice and share your feedback. Also [*subscribe and appreciate*](https://razorpay.com/payment-button/pl_IKvqCobZrv20Av/view/?utm_source=payment_button&utm_medium=button&utm_campaign=payment_button) the blog if you like it.