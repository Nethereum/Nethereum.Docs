---
title: "How to set up an Ethereum Blockchain on Azure"
author: "Gaël Blanchemain"
date: "October 30, 2017"
---

### Nethereum supports Microsoft Azure, which puts Azure infrastructure at the service of your Nethereum project, the below will show you how to deploy a private Blockchain on Azure:

## 1 - Create an [Azure account](https://azure.microsoft.com/en-us/resources/videos/sign-up-for-microsoft-azure/) or [sign](https://azure.microsoft.com/en-us/account/) in if you already have one

## 2 - Create a new resource on your Azure dashboard
![](1.png)

## 3 - In the resource search bar, enter ``` ethereum consortium blockchain ``` Select the ethereum consortium template, then click ‘Create’.
![](2.png)

## 4 - Click create to confirm deployment model
![](3.png)

## 5 - Enter the specifications of your blockchain, then click OK

### - Number of Consortium Members

The number of mining members in the network. Subnet will be formed for each mining member. (2 to 12 members)

### - Number of mining nodes per member

The number of mining nodes deployed per member.Total mining nodes = Members * Nodes Per Member. (1 to 15 nodes/member)

### - Mining node storage performance

Storage type for transaction db. (Standard or Premium)

### - Number of transaction nodes

The number of transaction nodes to be created. (1 to 5)

### - Transaction node storage performance

Storage type for transaction db. (Standard or Premium)

### - Transaction node storage replication

### - The storage replication policy. (LRS, GRS, RAGRS)

### - Transaction node virtual machine size
Size of transactional nodes VMs. (Standard A, Standard D, Standard D-v2,Standard F series, Standard DS, and Standard FS) 
![](4.png)

## 6 - Submit a network id, some passwords, then click OK.
The network id should be ideally between 4 and 9 digits number.
![](6.png)

## 7 - Review your blockchain's specs, then click OK.
![](7.png)

## 8 - Agree (or not) to the Terms of use, give Azure servers a few minutes to deploy your chain, you're done!
![](8.png)