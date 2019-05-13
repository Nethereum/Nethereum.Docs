# Nuget Packages

Nethereum provides two types of packages. Standalone packages targeting Netstandard 1.1, net451, Netstandard 2.0, Netcoreapp 2.1 and where possible net351 to support Unity3d. There is also a Nethereum.Portable library which combines all the packages into a single portable library for backwards support. As netstandard evolves and is more widely supported, the portable library might be eventually deprecated.

All the releases can be found in Nuget.

!!! Note
    **Continuous Integration Builds** - If you want to take advantage of a new feature as soon as they are merged into the code base, or if there are critical bugs you need fixed, we invite you to try the packages on our continuous integration feed. Simply add `https://www.myget.org/F/nethereum/api/v3/index.json` as a package source to either Visual Studio or Visual Studio for Mac.

To add a nuget to your project you can:

#### Windows users

To install the main packages you can either:

```
PM > Install-Package Nethereum.Web3
```
or 
```
PM > Install-Package Nethereum.Portable
```

#### Windows/Mac/Linux users

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
| Nethereum.Portable    | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.portable.svg)](https://www.nuget.org/packages/nethereum.portable)| Portable class library combining all the different libraries in one package |
| [Nethereum.Web3](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Web3)    | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.web3.svg)](https://www.nuget.org/packages/nethereum.web3)| Ethereum Web3 Class Library simplifying the interaction via RPC. Includes contract interaction, deployment, transaction, encoding / decoding and event filters |
| [Nethereum.Unity](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Unity) |  | Unity3d integration, libraries can be found in the Nethereum [releases](https://github.com/Nethereum/Nethereum/releases) |
| [Nethereum.Geth](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Geth)    | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.geth.svg)](https://www.nuget.org/packages/nethereum.geth)| Nethereum.Geth is the extended Web3 library for Geth. This includes the non-generic RPC API client methods to interact with the Go Ethereum Client (Geth) like Admin, Debug, Miner|
| [Nethereum.Quorum](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Quorum)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.quorum.svg)](https://www.nuget.org/packages/nethereum.quorum)| Extension to interact with Quorum, the permissioned implementation of Ethereum supporting data privacy created by JP Morgan|
| [Nethereum.Parity](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Parity)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.parity.svg)](https://www.nuget.org/packages/nethereum.parity)| Nethereum.Parity is the extended Web3 library for Parity. Including the non-generic RPC API client methods to interact with Parity. (WIP)|

## Core Libraries

|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------|
| [Nethereum.ABI](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.ABI) | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.abi.svg)](https://www.nuget.org/packages/nethereum.abi)| Encoding and decoding of ABI Types, functions, events of Ethereum contracts |
| [Nethereum.EVM](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.EVM) | |Ethereum Virtual Machine API|
| [Nethereum.Hex](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Hex) | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.hex.svg)](https://www.nuget.org/packages/nethereum.hex)| HexTypes for encoding and decoding String, BigInteger and different Hex helper functions|
| [Nethereum.RPC](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.RPC)   | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.rpc.svg)](https://www.nuget.org/packages/nethereum.rpc) | Core RPC Class Library to interact via RCP with an Ethereum client |
| [Nethereum.JsonRpc.Client](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.Client)   | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.jsonrpc.client.svg)](https://www.nuget.org/packages/nethereum.jsonrpc.client) | Nethereum JsonRpc.Client core library to use in conjunction with either the JsonRpc.RpcClient, the JsonRpc.IpcClient or other custom Rpc provider |
| [Nethereum.JsonRpc.RpcClient](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.RpcClient)   | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.jsonrpc.rpcclient.svg)](https://www.nuget.org/packages/nethereum.jsonrpc.rpcclient) | JsonRpc Rpc Client provider using Edjcase.JsonRpc.Client |
| [Nethereum JsonRpc IpcClient](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.IpcClient)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.jsonRpc.ipcclient.svg)](https://www.nuget.org/packages/nethereum.jsonRpc.ipcclient) |JsonRpc IpcClient provider for Windows, Linux and Unix|
| [Nethereum.RLP](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.RLP)  | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.rlp.svg)](https://www.nuget.org/packages/nethereum.rlp) | RLP encoding and decoding |
| [Nethereum.KeyStore](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.KeyStore)  | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.keystore.svg)](https://www.nuget.org/packages/nethereum.keystore) | Keystore generation, encryption and decryption for Ethereum key files using the Web3 Secret Storage definition, https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition |
| [Nethereum.Signer](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Signer)  | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.signer.svg)](https://www.nuget.org/packages/nethereum.signer) | Nethereum signer library to sign and verify messages, RLP and transactions using an Ethereum account private key |
| [Nethereum.Contracts](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Contracts)  | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.contracts.svg)](https://www.nuget.org/packages/nethereum.contracts) | Core library to interact via RPC with Smart contracts in Ethereum |
| [Nethereum.IntegrationTesting](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.IntegrationTesting)  |   | Integration testing module |
| [Nethereum.HDWallet](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.HDWallet)  | [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.HDWallet.svg)](https://www.nuget.org/packages/nethereum.HDWallet) | Generates an HD tree of Ethereum compatible addresses from a randomly generated seed phrase (using BIP32 and BIP39) |

Note: IPC is supported for Windows, Unix and Linux but is only available using Nethereum.Web3 not Nethereum.Portable
 
## Smart contract API Libraries

|  Project Source | Nuget_Package |  Description |
| ------------- |--------------------------|-----------
| [Nethereum.StandardTokenEIP20](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.StandardTokenEIP20)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.standardtokeneip20.svg)](https://www.nuget.org/packages/nethereum.nethereum.standardtokeneip20)| Nethereum.StandardTokenEIP20 Ethereum Service to interact with ERC20 compliant contracts |
| [Nethereum.Uport](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Uport)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.uport.svg)](https://www.nuget.org/packages/nethereum.uport)| Uport registry library |
| [Nethereum.ENS](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.ENS)| [![NuGet version](https://img.shields.io/nuget/vpre/nethereum.ens.svg)](https://www.nuget.org/packages/nethereum.ens)| Ethereum Name service library (original ENS) WIP to upgrade to latest ENS |

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



