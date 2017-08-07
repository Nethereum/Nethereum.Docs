---
title: "What is an hash function?"
author: "Gaël Blanchemain"
date: "August 7, 2017"
export_on_save:
  markdown: true
---
##  What is a hash function?

####  tl;dr
Cryptographic hash function take an input and convert it into an output. 

```mermaid
graph LR
ABCDEF-->|Hash Function|f6674e62795f798fe2b01b08580c3fdc
```

###  Detailed explanation
Ethereum addresses are generated using a contract's [public key](/docs/Ethereum-glossary-for-newbies/public-private-key.md), they represent the location of an Ethereum contract.