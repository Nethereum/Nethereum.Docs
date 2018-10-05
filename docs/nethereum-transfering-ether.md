
# Sending Ether with Nethereum

This article will walk you through the basics of Nethereum to send Ether using INFURA.

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
var web3 = new Web3("https://mainnet.infura.io");
```
## Prerequisites:

First, let's download the test chain matching your environment from <https://github.com/Nethereum/Testchains>

Start a Geth chain (geth-clique-linux\\, geth-clique-windows\\ or geth-clique-mac\\) using **startgeth.bat** (Windows) or **startgeth.sh** (Mac/Linux). The chain is setup with the Proof of Authority consensus and will start the mining process immediately.

Then, let's add the using statement to Nethereum.Web3.

```csharp
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.Web3.Accounts.Managed;
using Nethereum.Hex.HexTypes;
```

## Sending a transaction

To send a transaction, we will manage our account and sign the raw transaction locally. 

At the time of sending a transaction, the right method to deliver the transaction will be chosen. If using Nethereum **`TransactionManager`**, deploying a contract or using a contract function, the transaction will either be signed offline using the private key or a **`personal\_sendTransaction`** message will be sent using the password.

Here is how to set up a new account by creating an `account` object instance:

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var account = new Account(privateKey);
```

Now, the transaction itself, in this case, we are sending 1 Ether.
```csharp
var toAddress = "0x12890D2cce102216644c59daE5baed380d84830c";
var transaction = await web3.TransactionManager.SendTransactionAsync(account.Address, toAddress, new Nethereum.Hex.HexTypes.HexBigInteger(1));
```

