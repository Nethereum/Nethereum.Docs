---
title: 'What is an Ethereum account?'
author: 'Gaël Blanchemain'
date: 'July 28, 2017'
---  
  
## What is an Ethereum account?
  
  
#### tl;dr
  
  
Accounts are simple public/private keypairs, which you use to sign transactions.
There are two types of accounts: [externally owned accounts](#Externally-owned-accounts ) (EOAs) and [contract-accounts](#contract-accounts ). 
  
### Detailed explanation
  
  
#### Externally owned accounts: <a id="Externally-owned-accounts"></a>
  
- Have an ether balance
- Can send transactions (ether transfer or trigger contract code)
- Are controlled by private keys
- Have no associated code. They merely have a balance in Eth
#### Contract accounts (aka "contracts"): <a id="contract-accounts"></a>
  
- Have an ether balance
- Have associated code
- Their code execution is triggered by transactions or messages (calls) received from other contracts
- When executed - contracts perform operations of arbitrary complexity (Turing completeness)
- Manipulate their own persistent storage: i.e., can have its own permanent state - can call other contracts
This generic notion of account (Externally owned accounts/Contract accounts) is justified in that these entities are state objects, each of them have a state, and the state of all those accounts is the state of the Ethereum network which is updated with every block when [consensus](blockchain-consensus.md ) is reached.
  
Accounts are essential for users to interact with the Ethereum blockchain via [transactions](transaction.md ).
  
If we restrict Ethereum to only externally owned accounts and allow only transactions between them, we arrive at an “altcoin” system that is less powerful than bitcoin itself and can only be used to transfer ether.
  
Accounts represent identities of external agents (e.g., human personas, mining nodes or automated agents). Accounts use public key cryptography to sign transaction so that the EVM can securely validate the identity of a transaction sender.
  
Credits  to [ethdocs.org](http://ethdocs.org ) for the technical part of this explanation: http://ethdocs.org/en/latest/account-management.html#accounts
  