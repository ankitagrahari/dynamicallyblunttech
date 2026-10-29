---
title: "Set Swappiness in Linux"
date: 2026-10-27T08:14:18+05:30
draft: false
featureImage: "images/df024c_2f3925c35c5d43feb72a4dd9d4883a0c.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

In this post we will look into how to change the swappiness value in Linux.

**Swappiness** is the kernel parameter that defines how much your Linux kernel will use to copy RAM contents to swap. A low swap value means kernel will try to avoid swapping as much as possible, while a higher value will tend to use more data for swapping.

### Approach 1:

#### Steps

1. Login as root.

2. To get the current swappiness value:

```java
cat /proc/sys/vm/swappiness
```

3. To edit, open ***/etc/sysctl.conf*** file and set the desired value for ***vm.swappiness***

4. You can also set it like:

```java
sudo sysctl vm.swappiness =5 (can be between 0 to 100)
```

5. After this it requires a restart to set the values.

There is one more option without ***restarting*** your machine:

### Approach 2:

```java
swapoff -a
sudo sysctl vm.swappiness =5
swapon -a
```

This will set the swappiness on Linux machine without any restart.