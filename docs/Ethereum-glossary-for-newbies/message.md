---
title: "What is an Ethereum message?"
author: "Gaël Blanchemain"
date: "July 28, 2017"
export_on_save:
  markdown: true
---
## What is an Ethereum message?


[//]: # (CJuan> I can't really tell if there's a difference between message calls and messages)

#### tl;dr
Contracts can call other contracts or send Ether to non-contract accounts by the means of _message calls_. Message calls are similar to transactions, in that they have a source, a target, data payload, Ether, gas and return data. In fact, every transaction consists of a top-level message call which in turn can create further message calls.