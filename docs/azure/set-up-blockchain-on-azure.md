---
title: "How to set up an Ethereum Blockchain on Azure"
author: "Gaël Blanchemain"
date: "September 19, 2019"
---

Nethereum supports Microsoft Azure, the below will show you how to deploy a private Blockchain on Azure and start interacting with it:

## 1 - Create an [Azure Account](https://azure.microsoft.com/en-us/resources/videos/sign-up-for-microsoft-azure/) or [sign](https://azure.microsoft.com/en-us/account/) in if you already have one

## 2 - Create A Quorum Blockchain Member On Your Azure Dashboard
![](set-up-blockchain-on-azure1.png)
Creating a Blockchain member will spin up a network with two validator nodes and one transaction node on Azure, create a consortium and make you a member of that consortium. If you create a member in an existing consortium, Azure will add your account as a member.   

## 3 - Select A Connection Token
![](set-up-blockchain-on-azure3.png)
Select the name of your newly created consortium member, then select "transaction nodes", choose the node
you need to connect to from the list of nodes, then "sample code" and finally select the 'Nethereum' tab. You'll obtain a list of pre-filled methods you can pick from to connect to your particular Quorum instance.   

For further instructions on how to interact with an instance of Quorum on Azure, please consult Nethereum: 
