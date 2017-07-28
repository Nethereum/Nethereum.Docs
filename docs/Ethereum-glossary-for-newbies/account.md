---
title: "What is an Ethereum account?"
author: "Gaël Blanchemain"
date: "July 28, 2017"
export_on_save:
  markdown: true
---
## What is an Ethereum account?

  
#### tl;dr

Accounts are simple public/private keypairs, which you use to sign transactions.
There are two types of accounts: **externally owned accounts** (EOAs) and **contract accounts**. 
1. Externally owned accounts merely have balance in Eth.
2. Contract accounts have both balance and contract storage.
  
### Detailed explanation
This generic notion of account (Externally owned accounts/Contract accounts) is justified in that these entities are state objects, each of them have a state, and the state of all those accounts is the state of the Ethereum network which is updated with every block and which the network reaches consensus about. 

Accounts are essential for users to interact with the Ethereum blockchain via [transactions](/docs/Ethereum-glossary-for-newbies/transaction.md).

If we restrict Ethereum to only externally owned accounts and allow only transactions between them, we arrive at an “altcoin” system that is less powerful than bitcoin itself and can only be used to transfer ether.

Accounts represent identities of external agents (e.g., human personas, mining nodes or automated agents). Accounts use public key cryptography to sign transaction so that the EVM can securely validate the identity of a transaction sender.

Credits  to [ethdocs.org](http://ethdocs.org) for the technical part of this explanation: http://ethdocs.org/en/latest/account-management.html#accounts