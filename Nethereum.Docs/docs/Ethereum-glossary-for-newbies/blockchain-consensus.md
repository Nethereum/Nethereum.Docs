---
title: "What is consensus in the Ethereum blockchain?"
author: "Gaël Blanchemain"
date: "July 27, 2017"
export_on_save:
  markdown: true
---

###  What is consensus in the Ethereum blockchain?

####  tl;dr
The purpose of a consensus algorithm in a public Blockchain network is to make sure that the network’s participants agree on the current state of the Blockchain without the need to trust each other or to have a central authority. In current blockchain, consensus is reached via Proof of Work, Proof of Stake or Proof of Authority.

###  Detailed explanations

####  Why do blockchains need "_Proof of_"?
You probably noticed that most blockchains rely on either _**PoW (Proof of Work), PoS (Proof of Stake), PoA (Proof of Authority)**_ and various others.
The goal of the "proofing" work is to make it costly and difficult to add false transactions/spam to a block.

Proofing processes make it hard for [miners](/docs/Ethereum-glossary-for-newbies/mining.md/) to submit a block to the blockchain but easy for all [nodes](/docs/Ethereum-glossary-for-newbies/node.md) to verify if the new block is valid.

####  Proof of Work
In the context of Ethereum, a _**Proof of Work**_  is a cryptographic puzzle that [miners](/docs/Ethereum-glossary-for-newbies/mining.md/) try to solve in order to submit a new block to the blockchain and be rewarded Ether. That puzzle is difficult (costly, time-consuming) to produce. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required before a valid proof of work is generated. Ethereum currently uses proof of work (as of 07/25/2017) but is slated to adopt Proof of Stake soon.

####  Proof of Stake
A _**Proof of Stake**_ verifies that a [miner](/docs/Ethereum-glossary-for-newbies/mining.md/) has enough Ether at stake to submit/confirm a new block. Proof of Stake rewards miners who submit/confirm a valid block and it punishes those who don't, making it insanely costly to tamper with the blockchain's transaction.


####  Proof of Authority
_**Proof-of-authority**_ chains utilise a number of secret keys (authorities) to collaborate and create the longest chain instead of the public Ethereum network's proof-of-work scheme (Ethash).