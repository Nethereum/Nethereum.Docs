
# Sending Ether with Nethereum

This article will show you how to send Ether using a local Ethereum Node.

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

### Install Nethereum packages
You can now add Nethereum to your stack by installing one of [Nethereum Nugets](https://www.nuget.org/packages?q=nethereum)

For this Tutorial, you will need  [Nethereum Web3](https://www.nuget.org/packages/Nethereum.Web3/):

```
$ dotnet add package Nethereum.Web3
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

Here is how to set up a new account by creating an `account` object instance:

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var account = new Account(privateKey);
```
The next step is to create an instance of Web3, with our *account* object as argument.

```csharp
var web3 = new Web3(account);
```
We also need to instantiate a variable with our recipient's address as value:
```csharp
var toAddress = "0x13f022d72158410433cbd66f5dd8bf6d2d129924";
```
We can now send the transaction itself using the transaction manager. In this case, we let the transaction manager use the default amount of gas to pay for the transaction.

Note: when using the transaction manager,  Ether needs to be converted to Wei before sending, for this we will use the Conversion Utility.

Assuming we need to send 1 Ether we will use:

```csharp
var wei = Web3.Convert.ToWei(1);
```
### Sending Ether using default gas amount
Sending the transaction with the default amount of gas can be done as such:
```csharp
var transaction = await web3.TransactionManager.SendTransactionAsync(account.Address, toAddress, new Nethereum.Hex.HexTypes.HexBigInteger(1));
```

### Sending Ether using specific gas amount
We can also choose the amount of gas we want to attribute to our transaction, by adding its amount as an argument (in this case, the last argument):
```csharp
var transaction = await web3.TransactionManager.SendTransactionAsync(account.Address, toAddress, new Nethereum.Hex.HexTypes.HexBigInteger(1),2);
```
### Using a HD Wallet

Required Namespaces:
```csharp
Nethereum.Web3, Nethereum.HdWallet;
```
The process of transferring Ether using a HD Wallet is the same as using a standalone account, the only difference lies in initiating a HD Wallet and loading one of its accounts in a Web3 instance.
```csharp
string Words = "ripple scissors kick mammal hire column oak again sun offer wealth tomorrow wagon turn fatal";
                string Password = "password";
var wallet = new Wallet(Words, Password);
var account = wallet.GetAccount(0);
var toAddress = "0x13f022d72158410433cbd66f5dd8bf6d2d129924";
var web3 = new Web3(account);
var transaction = web3.TransactionManager.SendTransactionAsync(account.Address, toAddress, new Nethereum.Hex.HexTypes.HexBigInteger(1));
```
