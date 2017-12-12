## Installation and configuration of the Ethereum client Geth

You can download ``` Geth ``` latest stable version from [Github](https://github.com/ethereum/go-ethereum/releases)

## Installation

 ### Windows

On Windows, ``` Geth ``` installation is as simple as extracting geth.exe from your chosen OS.
The download page provides an installer as well as a zip file. 

The installer puts geth into your PATH automatically. The zip file contains the command .exe files and can be used without installing.

- Download zip file
- Extract geth.exe from zip
- Open a command prompt
- Excute geth.exe

### Mac

[Brew](https://brew.sh/) is recommended to install ``` Geth ``` on Mac OS:
```
$ brew update
$ brew upgrade
$ brew tap ethereum/ethereum
$ brew install ethereum
```

### Linux

On Linux, installing ``` Geth ``` can be done using ``` apt ```.

```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository -y ppa:ethereum/ethereum
$ sudo apt-get update
$ sudo apt-get install ethereum
```

### RPC / IPC options

There are several command line options to run geth [which can be found in their documentation](https://github.com/ethereum/go-ethereum/wiki/Command-Line-Options).

But most importantly, RPC or IPC need to be enabled.

HTTP JSON-RPC can be started with the ``` --rpc ``` flag

```
$ geth --rpc
```
The default port ( ```8545 ```) can be change as well as the listing address (``` localhost ```).

```
$ geth --rpc --rpcaddr <ip> --rpcport <portnumber>
```
If accessing the RPC from a browser, ``` CORS ``` will need to be enabled with the appropriate domain set. Otherwise, JavaScript calls are limited by the same-origin policy and requests will fail:

```
$ geth --rpc --rpccorsdomain "http://localhost:3000"
```
The JSON RPC can also be started from the geth console using the ```admin.startRPC(addr, port) ``` command.

### Setting up your own testnet

There is already a preconfigured tesnet in Nethereum, which [can be downloaded from github](https://github.com/Nethereum/Nethereum/tree/master/testchain/clique)

The preconfigured testnet will start producing blocks inmediately so there is no need to start this manually, for more information check the Proof of Authority section below.

The chain keystore in the "devChain" folder contains the keys for the preconfigured account, which is also present in the genesis file "genesis_dev.json".

* Account : ``` 0x12890d2cce102216644c59daE5baed380d84830c ```
* Password: ``` password ```
* Private Key: ``` 0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7 ```

### Proof of Authority

The consensus mechanism used in this testchain is Proof of Authority (PoA).

PoA consensus is reached by referring to a list of validators (referred to as authorities when they are linked to physical entities).

It does not depend on nodes solving arbitrarily difficult mathematical problems, but instead uses a set of "authorities" - nodes that are explicitly allowed to create new blocks and secure the blockchain. The chain has to be signed off by the majority of authorities, in which case it becomes a part of the permanent record. This makes it easier to maintain a private chain and keep the block issuers accountable.

For consortium setting there are no disadvantages of PoA network as compared to PoW. It is more secure (since an attacker with unwanted connection or hacked authority can not overwhelm a network potentially reverting all transactions), less computationally intensive (mining with difficulty which provides security requires lots of computation), more performant (Aura consensus provides lower transaction acceptance latency) and more predictable (blocks are issued at steady time intervals). PoA deployments are used by the enterprise and by the public (e.g. popular Kovan test network).

The current testchain it has been configured to produce blocks immediately, it has only one node with one validator account which it is unlocked when launching geth. ```--unlock 0x12890d2cce102216644c59daE5baed380d84830c --password "pass.txt"```

To start the chain you can use batch files or shell scripts, both of them will reset all the data when launched.

#### Batch file

```
RD /S /Q %~dp0\devChain\geth\chainData
RD /S /Q %~dp0\devChain\geth\dapp
RD /S /Q %~dp0\devChain\geth\nodes
del %~dp0\devchain\geth\nodekey

geth  --datadir=devChain init genesis_clique.json
geth --nodiscover --rpc --datadir=devChain  --rpccorsdomain "*" --mine --rpcapi "eth,web3,personal,net,miner,admin,debug" --unlock 0x12890d2cce102216644c59daE5baed380d84830c --password "pass.txt" --verbosity 0 console

```
[Source code](https://github.com/Nethereum/Nethereum/edit/master/testchain/clique/startgeth.bat)

#### Shell script

Ensure to make your script executable: ` chmod +x startgeth.sh `
You can start the script from the directory where it sits: ` ./startgeth.sh `
```
rm -rf devChain/chainData
rm -rf devChain/dapp
rm -rf devChain/nodes
rm -rf devchain/nodekey

geth  --datadir=devChain init genesis_clique.json
geth --nodiscover --rpc --datadir=devChain  --rpccorsdomain "*" --mine --rpcapi "eth,web3,personal,net,miner,admin,debug" --unlock 0x12890d2cce102216644c59daE5baed380d84830c --password "pass.txt" --verbosity 0 console

```
[Source code](https://github.com/Nethereum/Nethereum/edit/master/testchain/clique/startgeth.sh)


### Other info
If you need more information on how to setup your chain you can use this blog post
[http://juan.blanco.ws/setup-your-own-tesnet-ethereum/](http://juan.blanco.ws/setup-your-own-tesnet-ethereum/)

Proof of Authority in [Parity](https://github.com/paritytech/parity/wiki/Proof-of-Authority-Chains) and [Geth](https://github.com/ethereum/EIPs/issues/225)

