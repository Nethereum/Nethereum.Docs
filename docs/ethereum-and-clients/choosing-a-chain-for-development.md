# Setting up a client for development 

Blockchain development often requires to rely on a "fake" Blockchain environment which allows to test code against blockchain, but without the constraints of a real mainnet. These environments are called Testnets or Devchains. 
Working with a devchain enables you to work faster (devchains use a fast consensus model) and not to pay gas for each transaction (devchains run on "monopoly gas" which doesn't cost anything), in the case of a local Devchain, they also keep your work private.

Depending on your use-case, you might rely on a public Testnet (like Rinkeby or Gorli) or a local devchain. The main differences between them are:

- Testnets are not private and require to be online while local devchains are private and can be used offline. 
While it seems obvious to use a local devchain in every cases, Testnets actually come handy to test assumptions in a "semi-real" environment.

The below lists the main Ethereum clients and how to set them up as devchains. 


## Setting up a testchain 

All the main Ethereum clients can be configured as Testchains. 
When working in a local environment, the tools we recommend are ``` Geth Clique ```, ``` Parity PoA ``` and ``` Ganache CLI ```

Below are the most used Ethereum clients:
### Geth Clique

Using Geth Clique allows you to test your integration with smart contracts directly in Geth with a fast Proof of Authority consensus.

[Geth Clique Manual](geth.md)

### Parity

Using Parity in combination with PoA consensus mechanism yields the same benefits as with Geth.

[Parity Clique Manual](parity.md)

### Ganache-CLI

``` Ganache CLI ``` (formerly ``` Test RPC ```) is a very common and well-documented chain emulator.

Ganache inherits Truffle suite's benefits: mainly simplifying Smart Contracts testing, debugging and updating. Ganache has a quasi-immediate response time and great feedback cycle.
It's great to deploy contracts and interact with them instantly at no GAS cost.

[Ganache official repo](https://github.com/trufflesuite/ganache-cli)

## Cloud private testnet

Azure BaaS (Blockchain as a Service) allows you to deploy a testnet with several nodes and have a team work on the development.

[Azure BaaS Documentation](https://azure.microsoft.com/en-us/solutions/blockchain/) 

## Public testnets

Public testnets function in the same way main nets work, with two differences:
* They are free: transactions are paid with a worthless crypto-currency
* They are often more responsive than main nets 

The main public testchains are:

#### 1. Rinkeby

Cross-client testnet using PoA consensus mechanism.

[Rinkeby Official Site](https://www.rinkeby.io)

#### 2. Kovan

Cross-client testnet (working with both Parity and Geth) using PoA consensus mechanism and a particular focus on spam-resilience.  

[Kovan Official Site](https://kovan-testnet.github.io/website/)

#### 3. Ropsten

Less popular since hacked early 2017, however, Ropsten is still in service.

[Ropsten Github Repo](https://github.com/ethereum/ropsten)

Note: public testnets can be accessed via public nodes such as [INFURA](https://www.infura.io) 

## Debug mode

Debug modes are available whether you are using chain emulators or full-on Ethereum clients. 

### 1 - Geth

- Using option ``` debug ```

### 2 - Parity

- The use of Json RPC's [Trace Module](https://github.com/paritytech/parity/wiki/JSONRPC-trace-module) allows to trace transactions.

### 3 - Ganache/Testnet RPC

- Use the ``` --debug ``` option will Output VM opcodes for debugging

## Ether Faucets

The ether and tokens used in test networks is for testing purposes only (it can accurately be compared to Monopoly bills). It's mostly distributed by online "faucets". 

Here's a list of testnet Ether sources:

| Testnet Name | Faucet|
|----------------------|-------|
|Rinkeby| https://www.rinkeby.io/#faucet|
|Ropsten|https://blog.b9lab.com/when-we-first-built-our-faucet-we-deployed-it-on-the-morden-testnet-70bfbf4e317e|
| Kovan | Kovan requires you to request KETH from another person|

For more specific advice about faucets please check [this article.](https://medium.com/@juanfranblanco/netherum-faucet-and-nuget-templates-4a088f06933d)

## Testchains

At Nethereum, we developed a tool to simplify and accelerate Ethereum Blockchain development. It's called Testchains, installs in minutes and allows you to code fast with your Ethereum client of choice. Testchains can be downloaded at https://github.com/Nethereum/TestChains 



**Credits**  to [Karl Floersch](https://karl.tech) for the information about the different testnets: https://karl.tech/intro-guide-to-ethereum-testnets/
