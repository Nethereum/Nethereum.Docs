# Using Testchains

In order to simplify Blockchain development, Nethereum provides with [Testchains](https://github.com/Nethereum/TestChains). A Testchain is a selection of ready-to-use Ethereum clients configured for development (as they have a very fast response time).

Nethereum **TestChains** offers the following Ethereum clients:

We recommend using [Testchains](https://github.com/Nethereum/TestChains) to quickly get started with Ethereum clients such as **Geth**, **Parity** or **Quorum** or **Ganache**.

## Pre-Requisites

Linux, Mac or Windows. 


## Install

Clone into [https://github.com/Nethereum/TestChains](https://github.com/Nethereum/TestChains).

## Starting TestChains

TestChains provides with **Geth**, **Parity**,  **Quorum** and **Ganache**.

They are preconfigured with some Ether and a default account. The default account address is ```0x12890d2cce102216644c59daE5baed380d84830c``` with private key ```0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7```.

The account key store file password is : ```password```

## Geth
___
Devchain version of **Geth** (Ethereum Go client) configured with PoA (Proof of Authority) for fast reponse.

You can start each version of **Geth** by using the **startgeth** script (see below) 
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
You can start each version of parity by using the **launch** script (see below) 

### - Windows

>       > parity-poa-windows > launch.bat

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.

### - Mac

>       > parity-poa-mac > launch.sh

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.

Note: use ``` chmod +x launch.sh ``` and ``` chmod +x parity ``` to allow script to execute.

### - Linux

>       > parity-poa-linux > launch.sh

Note: use ``` chmod +x launch.sh ``` and ``` chmod +x parity ``` to allow geth to execute.

Latest versions of Parity can be downloaded [here](https://github.com/paritytech/parity-ethereum/releases/latest), simply download the Parity executable and replace the old one.

## Ganache
___

Formerly known as TestRPC, Ganache is the gui version of Truffle's devchain.
You can start each version of Ganache by using the **launch** script (see below) 
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

Only available on Linux, **Quorum Network Manager** spins a small network of Quorum nodes.

You can install the Network with **setup.sh** and use **launch.sh** to start nodes. 
### Linux

>   quorum-linux    > ```./setup.sh``` ```./launch.sh```
