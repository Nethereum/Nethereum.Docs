
# Nethereum Getting Started: Getting an Account Balance From Infura

This simple sample will show you how to set up your environment with Nethereum, connect to [Infura](https://www.infura.io) and retrieve the balance of an account from the mainnet (live Ethereum). 

Infura provides a set of public nodes removing the need to have a local or maintained client fully synchronised with the main Ethereum network.

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
For this Tutorial, you will need  [Nethereum Portable](https://www.nuget.org/packages/Nethereum.Web3/):

```
$ dotnet add package Nethereum.Portable
```

The next step is to create an instance of Web3, with the infura url for mainnet.

```csharp
var web3 = new Web3("https://mainnet.infura.io");
```

Using the Eth API we can execute the GetBalance request asynchronously, for our selected account. In this scenario I have chosen the Ethereum Foundation account. “0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae”

```csharp
var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
```

The amount returned is in Wei, the lowest unit of value. We can convert this to Ether using the Convertion utility:

```csharp
var etherAmount = Web3.Convert.FromWei(balance.Value);
```
