---
title: "Smart Contracts"
author: "Gaël Blanchemain"
date: "July 27, 2017"
export_on_save:
  markdown: true
---
##  What is a smart contract?

####  tl;dr
A smart contract is a digitized version of a traditional contract. It sits on the blockchain (Ethereum in our case) and contains the business logic of a [Dapp](/docs/Ethereum-glossary-for-newbies/Dapp.md).

###  Detailed explanation

To a developer, smart contract source code is not much different from that of centralized apps. 

A few points make a difference:
* **Smart contracts are immutable**
Once programmed, the terms of the contract cannot be changed, thus reducing the risks of fraudulent manipulation.
* **Smart contracts enforce themselves** 
They don't need a third-party to be enforced, each computational step is executed by each node, making them more trustworthy, faster and cheaper than middlemen's assisted operations (lawyers, notaries, banks).
* **Smart contracts are resilient to power cuts** 
Because thousands of nodes run a copy of those contracts, they are not vulnerable to power failure and other infrastructure malfunctions.

Example of Smart Contract:
```pragma solidity 0.4.13;
contract HelloWorld { function saySomething() returns (string message) { return "Hello World!"; }}
```