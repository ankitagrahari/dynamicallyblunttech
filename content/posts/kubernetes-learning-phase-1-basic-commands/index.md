---
title: "KUBERNETES LEARNING PHASE 1 - BASIC COMMANDS"
date: 2026-10-27T08:14:15+05:30
draft: false
featureImage: "images/df024c_61094322f36648a4a0f160386f593577.jpg"
tags: ['[]']
categories: ['[]']
showReadingTime: true
---

This post will only includes scenario based Kubernetes problem and the commands/debugging steps. It will be updated whenever I learn something new.

**For Installation of Kubernetes refer here**: [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)

### Case 1: Get all pods in a namespace

```java
kubectl get pods -n <namespace_name>
```

### Case 2: Get all namespaces

```java
kubectl get namespaces 
OR
kubectl get ns
```

### Case 3: Create pods with a name and image in a particular namespace

```java
kubectl run <pod_name> --image=<image_name> -n <namespace>
```

*e.g.*

```java
kubectl run redis --image=redis -n my-namespace
```

### Case 4: Get all pods in all the namespaces

```java
kubectl get pods --all-namespaces
```

### Case 5: Get all replicasets

```java
kubectl get replicaset
```

### Case 6: Create pods using yaml file

```java
kubectl apply -f abc.yml -n namespace
```

*   abc.yaml *or* abc.yml* file:

```java
apiVersion: v1
kind: Pod
metadata: 
  name: new-pod
  label:
    type: linux
spec:
  containers:
    -name: redis
     image: redis
```

### Case 7: Create deployment using yaml file

```java
kubectl apply -f deployment.yml
```

deployment.yml file is having

```java
apiVersion: apps/v1
kind: Deployment
metadata:
  name: new-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      name: abc-pod
  template:
    metadata:
      labels:
        name: abc-pod
    spec:
      containers:
      - name: abc-container
        image: nginx
        command:
        - sh
        - "-c"
        - echo Hello Kubernetes! && sleep 3600
```

Here important points are: 
* apiVersion should follow the way apps/v1 or apps/v
* kind is case sensitive
* matchlabels.name should be same as metadata.labels.name
* You can specify the replica number and that many pods will be created.
* When this deployment will be created, a replica set, 3 pods, one deployment will be created.

### Case 8: Get all details of the pod

```java
kubectl describe pod <pod_name> -n <namespace>
```

### Case 9: Get all pods, replicaset, deployment and services present

```java
kubectl get all
```

### Case 10: Editing an existing replicaset

```java
kubectl edit replicaset <replicaset_name>
```

There will be an another post soon dealing with more kubernetes day to day used commands.