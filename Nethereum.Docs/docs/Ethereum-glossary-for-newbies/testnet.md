---
title: "What is a testnet?"
author: "Gaël Blanchemain"
date: "ddate"
export_on_save:
  markdown: true
---
##  What is a testnet?

####  tl;dr
Testnets simulate the Ethereum network and [EVM](/docs/Ethereum-glossary-for-newbies/EVM.md). They allow developers to upload and interact with smart contracts without paying the cost of gas.

###  Detailed explanation

###  Why use a Testnet?
As a developer, Testnets have several benefits:
####  1. Testnets are free to use
Smart contracts must pay gas for their computations on the Ethereum network. If you rent the Ethereum network to run a contract, you have to pay. However, testnets provide free or unlimited gas. That allows developers to test contracts without having to pay real money for their execution.
####  2. Testnets are fast
The Ethereum main net takes about 20 seconds to process transactions while testnets are nearly instantaneous.
####  3. Testnets provide more feedback
Calls to lightweight testnets nodes provide good error messages.

###  What Testnets can I use?


##### 1. Test RPC
Although not a "true Testnet" since it runs locally, Test RPC is ideal to start a project, execute [transactions](/docs/Ethereum-glossary-for-newbies/transaction.md) instant response


[//]: # (CJuan> Is there anything Nethereum-specific to say about Ropsten, Rinkeby and Kovan?)

##### 1. Ropsten

##### 2. Rinkeby

##### 3. Kovan

####Where do I find Ether to use a testnet?...
The ether and tokens on test networks is generally worthless and is used for testing purposes only. It's often distributed in "faucets". Faucets are best found by using keywords such as  testnet's name (```Rinkeby, Ropsten, Kovan```) + ```faucet```. We chose not to provide URLs as they change all the time :)
You can read Nethereum-specific advice about faucets [here](https://medium.com/@juanfranblanco/netherum-faucet-and-nuget-templates-4a088f06933d)

**Credits**  to [Karl Floersch](https://karl.tech) for the technical part of this explanation: https://karl.tech/intro-guide-to-ethereum-testnets/