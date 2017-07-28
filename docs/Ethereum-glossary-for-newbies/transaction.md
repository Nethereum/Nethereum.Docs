---
title: "What is an Ethereum transaction?"
author: "Gaël Blanchemain"
date: "July 28, 2017"
export_on_save:
  markdown: true
---
## What is an Ethereum transaction?
  
#### tl;dr

A transaction is a message that is sent from one [account](/docs/Ethereum-glossary-for-newbies/account.md) to another account (which might be the same or the special zero-account). It can include binary data (its payload) and Ether.

If the target account contains code, that code is executed and the payload is provided as input data.
  
### Detailed explanation
A transaction is a document authorizing some particular action associated with the blockchain. In a currency, the dominant transaction type is sending currency units or tokens to someone else; in other systems actions like registering domain names, making and fulfilling trade offers and entering into contracts are also valid transaction types.

### What are the characteristics of an Ethereum transaction?
  Transactions:
1. Cost gas (Ether)
2. Change the state of the network
3. Aren't processed immediately
4. Won't expose a return value (only a transaction id).
  
### Transactions vs Messages?
  In Ethereum transactions and [Messages](/docs/Ethereum-glossary-for-newbies/message.md) are different; a "transaction" in Ethereum parlance specifically refers to a physical digitally signed piece of data that goes in the blockchain, and every transaction triggers an associated message, but messages can also be sent by EVM code, in which case they are never represented in data anywhere.
