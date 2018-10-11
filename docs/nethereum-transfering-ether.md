
# Sending Ether with Nethereum

This article will show you how to send Ether using INFURA.

## Pre-requisites

The below instructions apply to Windows, Mac and Linux OSes.

### Install .NET

First, make sure your environment is set to work with .NET Core, you can find all the instructions on [https://www.microsoft.com/net/learn/get-started](https://www.microsoft.com/net/learn/get-started)

### Create a .NET app

In a new directory, use the dotnet command to create a new console app:

```
$ dotnet create new console
```
 
Your app directory now contains a file named: `Program.cs` this is the file that we will use throughout this tutorial.

### Install Nethereum packages.
You can now add Nethereum to your stack by installing one of [Nethereum Nugets](https://www.nuget.org/packages?q=nethereum)

For this Tutorial, you will need  [Nethereum Web3](https://www.nuget.org/packages/Nethereum.Web3/):

```
$ dotnet add package Nethereum.Web3
```
The next step is to create an instance of Web3, with the infura url for mainnet.

```csharp
var web3 = new Web3();
```
## Prerequisites:

First, let's download the test chain matching your environment from <https://github.com/Nethereum/Testchains>

Start a Geth chain (geth-clique-linux\\, geth-clique-windows\\ or geth-clique-mac\\) using **startgeth.bat** (Windows) or **startgeth.sh** (Mac/Linux). The chain is setup with Proof of Authority consensus and will start the mining process immediately.

Then, let's add using statements to Nethereum.Web3.

```csharp
using System;
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.Web3.Accounts.Managed;
using Nethereum.Hex.HexTypes;
```

## Sending a transaction

To send a transaction, we will manage our account and sign the raw transaction locally. 

### Sending a transaction with a `ManagedAccount` object

 Nethereum's managed accounts are maintained by the Ethereum client (geth/parity), allowing to automatic sign transactions and to manage the account's private key securely:


At the time of sending a transaction, the right method to deliver the transaction will be chosen. If using Nethereum **`TransactionManager`**, deploying a contract or using a contract function, the transaction will either be signed offline using the private key or a **`personal\_sendTransaction`** message will be sent using the password.

Here is how to set up a new account by creating an `account` object instance:

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var account = new Account(privateKey);
```
## Converting Ether to Wei

Ether needs to be converted to Wei before sending it, for this we will use the Conversion Utility.

So if we were going to send 1 Ether we will use:

```csharp
var wei = Web3.Convert.ToWei(1);
```
Finally we will just set the address that we want to send some Ether to, and using the Transaction manager this will be signed with our private key and and sent to the network.

```csharp
var toAddress = "0x12890D2cce102216644c59daE5baed380d84830c";
var transaction = await web3.TransactionManager.SendTransactionAsync(account.Address, toAddress, new Nethereum.Hex.HexTypes.HexBigInteger(wei));
var receipt = await web3.Eth.GetEtherTransferService().TransferEtherAndWaitForReceiptAsync(toAddress, 1.11m, 2);
```
