---
title: "What are public and private keys"
author: "Gaël Blanchemain"
date: "August 7, 2017"
export_on_save:
  markdown: true
---
##  What are public and private keys?

####  tl;dr
On Ethereum, public and private are used:
1. to **Sign data** (certifying its origin).
2. to **Encrypt data**
3. to **Decrypt data**

Public and private keys.

###  Detailed explanation
Cryptographic keys are the backbone of security in Ethereum, they garantee the origin of data and restrict their access to  designated owners/users.

Each Ethereum account has a **private key** and a **public key**.

1. **Private key**
Private keys are generated cryptographically with tools like _openssl_. The following command:
``` openssl ecparam -name secp256k1 -genkey -noout ```

Generates a key of the format:
``` 
MHQCAQEEIHg9y3qNQ4kGLNr2aGH4bCah+WHL44Ta2qix0pwSK59IoAcGBSuBBAAK
oUQDQgAEqXS+UM4Dyu06ksUWmcgl/0g5EkGNxolCxIz4DYqbLuED5iqu2XI4YCb6
9vx9xXaiswCbfhcaez6RbD0dDRHKWQ==
```
Private keys shouldn't be shared with anyone, they are the equivalent of the physical key protecting a lock.

2. **Public key**
Public keys are generated using a private key, they are shared with users who need to verify the origin of a file.

#### How do Private/Public Keys work?

always come in pairs and offer its owner various capabilities. Those capabilities are based on cryptographic mathematics. As their name suggest, the public key is meant to be distributed to whoever is relevant, while the private key is to be jealously guarded, akin to having your house address public, but keeping the key to your house private.