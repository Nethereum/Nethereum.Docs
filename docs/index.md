# What is Nethereum ?

Nethereum is the .Net integration library for Ethereum, simplifying the access and smart contract interaction with Ethereum nodes both public or permissioned like Geth, [Parity](https://www.parity.io/) or [Quorum](https://www.jpmorgan.com/global/Quorum).

Nethereum is developed targeting netstandard 1.1, net451 and also as a portable library, hence it is compatible with all the operating systems (Windows, Linux, MacOS, Android and OSX) and has been tested on cloud, mobile, desktop, Xbox, hololens and windows IoT.

Upcoming releases will include functionalities such as [DevP2P](https://github.com/ethereum/devp2p), [Plasma](https://plasma.io/plasma.pdf) and Micro-Payments.

## Features

* JSON RPC / IPC Ethereum core methods.
* Geth management API (admin, personal, debugging, miner).
* [Parity](https://www.parity.io/) management API.
* [Quorum](https://www.jpmorgan.com/global/Quorum) integration.
* Simplified smart contract interaction for deployment, function calling, transaction and event filtering and decoding of topics.
* [Unity 3d](https://unity3d.com/) Unity integration.
* ABI to .Net type encoding and decoding, including attribute based for complex object deserialization.
* Hd Wallet
* Transaction, RLP and message signing, verification and recovery of accounts.
* Libraries for standard contracts Token, [ENS](https://ens.domains/) and [Uport](https://www.uport.me/)
* Integrated TestRPC testing to simplify TDD and BDD (Specflow) development.
* Key storage using Web3 storage standard, compatible with Geth and Parity.
* Simplified account life cycle for both managed by third party client (personal) or stand alone (signed transactions).
* Low level Interception of RPC calls.
* Code generation of smart contracts services.

## Quick installation

Nethereum provides two types of packages. Standalone packages targeting Netstandard 1.1, net451 and where possible net351 to support Unity3d. There is also a Nethereum.Portable library which combines all the packages into a single portable library. As netstandard evolves and is more widely supported, the portable library might be eventually deprecated.

To install the latest version:

#### Windows users

To install the main packages you can either:

```
PM > Install-Package Nethereum.Web3
```
or 
```
PM > Install-Package Nethereum.Portable
```

#### Mac/Linux users

```
dotnet add package Nethereum.Web3 
``` 
or 
```
dotnet add package Nethereum.Portable
```

## Main Libraries

|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------|
| Nethereum.Portable    | [![NuGet version](https://badge.fury.io/nu/nethereum.portable.svg)](https://badge.fury.io/nu/nethereum.portable)| Portable class library combining all the different libraries in one package |
| [Nethereum.Web3](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Web3)    | [![NuGet version](https://badge.fury.io/nu/nethereum.web3.svg)](https://badge.fury.io/nu/nethereum.web3)| Ethereum Web3 Class Library simplifying the interaction via RPC. Includes contract interaction, deployment, transaction, encoding / decoding and event filters |
| [Nethereum.Unity](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Unity) |  | Unity3d integration, libraries can be found in the Nethereum [releases](https://github.com/Nethereum/Nethereum/releases) |
| [Nethereum.Geth](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Geth)    | [![NuGet version](https://badge.fury.io/nu/nethereum.geth.svg)](https://badge.fury.io/nu/nethereum.geth)| Nethereum.Geth is the extended Web3 library for Geth. This includes the non-generic RPC API client methods to interact with the Go Ethereum Client (Geth) like Admin, Debug, Miner|
| [Nethereum.Quorum](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Quorum)| [![NuGet version](https://badge.fury.io/nu/nethereum.quorum.svg)](https://badge.fury.io/nu/nethereum.quorum)| Extension to interact with Quorum, the permissioned implementation of Ethereum supporting data privacy created by JP Morgan|
| [Nethereum.Parity](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Parity)| [![NuGet version](https://badge.fury.io/nu/nethereum.parity.svg)](https://badge.fury.io/nu/nethereum.parity)| Nethereum.Parity is the extended Web3 library for Parity. Including the non-generic RPC API client methods to interact with Parity. (WIP)|

## Core Libraries

|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------|
| [Nethereum.ABI](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.ABI) | [![NuGet version](https://badge.fury.io/nu/nethereum.abi.svg)](https://badge.fury.io/nu/nethereum.abi)| Encoding and decoding of ABI Types, functions, events of Ethereum contracts |
| [Nethereum.EVM](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.EVM) | |Ethereum Virtual Machine API|
| [Nethereum.Hex](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Hex) | [![NuGet version](https://badge.fury.io/nu/nethereum.hex.svg)](https://badge.fury.io/nu/nethereum.hex)| HexTypes for encoding and decoding String, BigInteger and different Hex helper functions|
| [Nethereum.RPC](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.RPC)   | [![NuGet version](https://badge.fury.io/nu/nethereum.rpc.svg)](https://badge.fury.io/nu/nethereum.rpc) | Core RPC Class Library to interact via RCP with an Ethereum client |
| [Nethereum.JsonRpc.Client](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.Client)   | [![NuGet version](https://badge.fury.io/nu/nethereum.jsonrpc.client.svg)](https://badge.fury.io/nu/nethereum.jsonrpc.client) | Nethereum JsonRpc.Client core library to use in conjunction with either the JsonRpc.RpcClient, the JsonRpc.IpcClient or other custom Rpc provider |
| [Nethereum.JsonRpc.RpcClient](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.RpcClient)   | [![NuGet version](https://badge.fury.io/nu/nethereum.jsonrpc.rpcclient.svg)](https://badge.fury.io/nu/nethereum.jsonrpc.rpcclient) | JsonRpc Rpc Client provider using Edjcase.JsonRpc.Client |
| [Nethereum JsonRpc IpcClient](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.IpcClient)| [![NuGet version](https://badge.fury.io/nu/nethereum.jsonRpc.ipcclient.svg)](https://badge.fury.io/nu/nethereum.jsonRpc.ipcclient) |JsonRpc IpcClient provider for Windows, Linux and Unix|
| [Nethereum.RLP](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.RLP)  | [![NuGet version](https://badge.fury.io/nu/nethereum.rlp.svg)](https://badge.fury.io/nu/nethereum.rlp) | RLP encoding and decoding |
| [Nethereum.KeyStore](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.KeyStore)  | [![NuGet version](https://badge.fury.io/nu/nethereum.keystore.svg)](https://badge.fury.io/nu/nethereum.keystore) | Keystore generation, encryption and decryption for Ethereum key files using the Web3 Secret Storage definition, https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition |
| [Nethereum.Signer](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Signer)  | [![NuGet version](https://badge.fury.io/nu/nethereum.signer.svg)](https://badge.fury.io/nu/nethereum.signer) | Nethereum signer library to sign and verify messages, RLP and transactions using an Ethereum account private key |
| [Nethereum.Contracts](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Contracts)  | [![NuGet version](https://badge.fury.io/nu/nethereum.contracts.svg)](https://badge.fury.io/nu/nethereum.contracts) | Core library to interact via RPC with Smart contracts in Ethereum |
| [Nethereum.IntegrationTesting](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.IntegrationTesting)  |   | Integration testing module |
| [Nethereum.HDWallet](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.HDWallet)  | [![NuGet version](https://badge.fury.io/nu/nethereum.HDWallet.svg)](https://badge.fury.io/nu/nethereum.HDWallet) | Generates an HD tree of Ethereum compatible addresses from a randomly generated seed phrase (using BIP32 and BIP39) |

Note: IPC is supported for Windows, Unix and Linux but is only available using Nethereum.Web3 not Nethereum.Portable
 
## Smart contract API Libraries

|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------
| [Nethereum.StandardTokenEIP20](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.StandardTokenEIP20)| [![NuGet version](https://badge.fury.io/nu/nethereum.standardtokeneip20.svg)](https://badge.fury.io/nu/nethereum.nethereum.standardtokeneip20)| Nethereum.StandardTokenEIP20 Ethereum Service to interact with ERC20 compliant contracts |
| [Nethereum.Uport](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Uport)| [![NuGet version](https://badge.fury.io/nu/nethereum.uport.svg)](https://badge.fury.io/nu/nethereum.uport)| Uport registry library |
| [Nethereum.ENS](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.ENS)| [![NuGet version](https://badge.fury.io/nu/nethereum.ens.svg)](https://badge.fury.io/nu/nethereum.ens)| Ethereum Name service library (original ENS) WIP to upgrade to latest ENS |

## Utilities

|  Project Source |  Description |
| ------------- |--------------------------|
| [Nethereum.Generator.Console](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Generator.Console) |  |
| [Nethereum.Console](https://github.com/Nethereum/Nethereum.Console) | A collection of command line utilities to interact with Ethereum and account management |

## Training modules

|  Project Source |  Description |
| ------------- |--------------------------|
|[Nethereum.Workbooks](https://github.com/Nethereum/Nethereum.Workbooks) | Xamarin Workbook tutorials including executable code | 
|[Nethereum.Tutorials](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Tutorials) | Tutorials to run on VS Studio |

## Code templates

|  Source |  Description |
| ------------- |------------|
[Keystore generator](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.KeyStore.Console.Sample)| Keystore file generator|
[Faucet](https://github.com/Nethereum/Nethereum.Faucet)| Web application template for an Ether faucet |
[Nethereum Flappy](https://github.com/Nethereum/Nethereum.Flappy)| The source code files for the Unity3d game integrating with Ethereum |
[Nethereum Game Sample](https://github.com/Nethereum/nethereum.game.sample)| Sample game demonstrating how to integrate Nethereum with [UrhoSharp's SamplyGame](https://github.com/xamarin/urho-samples/tree/master/SamplyGame) to build a cross-platform game interacting with Ethereum |
[Nethereum UI wallet sample](https://github.com/Nethereum/nethereum.UI.wallet.sample)| Cross platform wallet example using Nethereum, Xamarin.Forms and MvvmCross, targeting: Android, iOS, Windows Mobile, Desktop (windows 10 uwp), IoT with the Raspberry PI and Xbox. |

## Smart contract api Libraries
|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------|
| [Nethereum.StandardTokenEIP20](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.StandardTokenEIP20)| [![NuGet version](https://badge.fury.io/nu/nethereum.standardtokeneip20.svg)](https://badge.fury.io/nu/nethereum.nethereum.standardtokeneip20)| ``` Nethereum.StandardTokenEIP20 ``` Ethereum Service to interact with ERC20 compliant contracts |
| [Nethereum.Uport](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Uport)| [![NuGet version](https://badge.fury.io/nu/nethereum.uport.svg)](https://badge.fury.io/nu/nethereum.uport)| Uport registry library |
| [Nethereum.ENS](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.ENS)| [![NuGet version](https://badge.fury.io/nu/nethereum.ens.svg)](https://badge.fury.io/nu/nethereum.ens)| Ethereum Name service library (original ENS) WIP to upgrade to latest ENS |



