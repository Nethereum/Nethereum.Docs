---
title: "What is an Ethereum account?"
author: "Gaël Blanchemain"
date: "ddate"
export_on_save:
  markdown: true
---
## What is an Ethereum account?
  
  
#### tl;dr

A transaction is a message that is sent from one account to another account (which might be the same or the special zero-account, see below). It can include binary data (its payload) and Ether.

If the target account contains code, that code is executed and the payload is provided as input data.

a transaction is a document authorizing some particular action associated with the blockchain. In a currency, the dominant transaction type is sending currency units or tokens to someone else; in other systems actions like registering domain names, making and fulfilling trade offers and entering into contracts are also valid transaction types.
  
### Detailed explanation
  

  Transactions:
Cost gas (Ether)
Change the state of the network
Aren't processed immediately
Won't expose a return value (only a transaction id).
  
### Transactions vs Messages?
  a sort of "virtual transaction" sent by EVM code from one account to another. Note that "transactions" and "messages" in Ethereum are different; a "transaction" in Ethereum parlance specifically refers to a physical digitally signed piece of data that goes in the blockchain, and every transaction triggers an associated message, but messages can also be sent by EVM code, in which case they are never represented in data anywhere.
wip
  
**Credits**  to [Karl Floersch](https://karl.tech ) for the technical part of this explanation: https://karl.tech/intro-guide-to-ethereum-testnets/