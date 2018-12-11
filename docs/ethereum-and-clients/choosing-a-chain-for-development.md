# Choosing a chain for your development environment 

When developing on Ethereum, different approaches are required depending on your development environment. Below are some tools we recommend:

## Testchains

Blockchain developing often requires to run a local Blockchain client (AKA: TestChain). This is to make sure your work remains private and that any sent transaction gets a fast response.

In order to speed up the process, Nethereum offers pre-configured devchains that can be spun  in a few minutes. Each of these chains uses PoA (Proof of Authority) as a consensus model for faster response. They all launch using provided scripts, automatically provided with accounts and passwords. 

First, clone the following repo: https://github.com/Nethereum/TestChains

The preconfigured account is ```0x12890d2cce102216644c59daE5baed380d84830c``` with private key ```0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7```.

The account key store file password is : ```password```

## Geth
___
Devchain version of Geth (Ethereum Go client) configured with PoA (Proof of Authority) for fast reponse.

### - Windows

>       > geth-clique-windows > startgeth.bat

Latest versions of geth can be downloaded [here](https://geth.ethereum.org/downloads/), simply download the geth executable and replace the old one.

### - Mac

>       > geth-clique-mac > startgeth.sh

Note: use ``` chmod +x startgeth.sh ``` and ``` chmod +x geth ``` to allow geth to execute.

Latest versions of geth can be downloaded [here](https://geth.ethereum.org/downloads/), simply download the geth executable and replace the old one.
### - Linux

>       > geth-clique-linux > startgeth.sh

Note: use ``` chmod +x startgeth.sh ``` and ``` chmod +x geth ``` to allow geth to execute.


Latest versions of geth can be downloaded [here](https://geth.ethereum.org/downloads/), simply download the geth executable and replace the old one.
## Parity
___
Devchain version of Parity (Ethereum Rust client) configured with PoA (Proof of Authority) for fast reponse.

### - Windows

>       > parity-poa-windows > launch.bat

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.

### - Mac

>       > parity-poa-mac > launch.sh

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.


Note: use ``` chmod +x launch.sh ``` and ``` chmod +x parity ``` to allow geth to execute.

### - Linux

>       > parity-poa-linux > launch.sh

Note: use ``` chmod +x launch.sh ``` and ``` chmod +x parity ``` to allow geth to execute.

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.

## Ganache
___

parity-poa-windows

CLI version of Truffle's devchain.

### Windows
npm install -g ganache-cli
>   ganache-windows    > launch.bat

### Mac
npm install -g ganache-cli
>  ganache-mac    > ./launch.sh

### Linux
npm install -g ganache-cli
>   ganache-linux    > ./launch.sh

## Quorum
___

Quorum setup in draft mode.

### Linux

>   quorum-linux    > ```./setup.sh``` ```./launch.sh```
/

## Setting up a testchain 

When working in a local environment, the tools we recommend are ``` Geth Clique ```, ``` Parity PoA ``` and ``` Ganache CLI ```

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





**Credits**  to [Karl Floersch](https://karl.tech) for the information about the different testnets: https://karl.tech/intro-guide-to-ethereum-testnets/
