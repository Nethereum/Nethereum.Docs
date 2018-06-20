
# Nethereum Started Guide for Windows

Documentation about Nethereum can be found at: <https://nethereum.readthedocs.io>

## Pre-requisites

First, make sure your environment is set to work with .NET Core, either in CLI mode or using [Visual Studio](https://visualstudio.microsoft.com/), you can find all the instructions on https://www.microsoft.com/net/learn/get-started

Once done setting your .NET environment, you can now add Nethereum to your environment by installing one of [Nethereum Nugets](https://www.nuget.org/packages?q=nethereum) 

To apply the following Tutorial, you will need  [Nethereum Nugets](https://www.nuget.org/packages/Nethereum.Web3/) 
 
First, let's download the test chain matching your environment from <https://github.com/Nethereum/Testchains>

Start a Geth chain (geth-clique-linux\\, geth-clique-windows\\ or geth-clique-mac\\) using **startgeth.bat** (Windows) or **startgeth.sh** (Mac/Linux). The chain is setup with the Proof of Authority consensus and will start the mining process immediately.

To get started, reference the NuGet package

```csharp
#r "Nethereum.Portable"
```

First, we need to new up a web3 object for localhost:8545 (this uses RPC)

```csharp
var web3 = new Nethereum.Web3.Web3();
```
We are now ready to interact with our devchain, the below gives an overview of basic commands:
## Checking if we are mining 
```csharp
var isMining = await web3.Eth.Mining.IsMining.SendRequestAsync()
```

## Listing all pre-defined accounts in the devchain

```csharp
var accounts = await web3.Eth.Accounts.SendRequestAsync()
```

## Getting the balance for the default account

```csharp
var balance = await web3.Eth.GetBalance.SendRequestAsync("0x12890d2cce102216644c59dae5baed380d84830c")
```

## Creating a new account
```csharp
var account = await web3.Personal.NewAccount.SendRequestAsync("password");
```
## Performing a simple transaction

The simplest (and most frequently needed) type of transaction is to transfer some Ether.


To interact with this function using Nethereum we will need to define the address to which we want to send the Ether as well as the amount we intend to send:

```csharp
var newAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
```

```csharp
var amountToSend = 1000;
```

Before we execute the transaction, we can “estimate” how much the transaction will cost in gas, by simulating it. This will allow us to avoid supplying too much or too little gas.

## Estimating the gas cost of a transaction
To estimate the gas cost in our transfer function we can call \*\*EstimateGasAsync \*\* passing the same parameters.

```csharp
var gas = await transferFunction.EstimateGasAsync(senderAddress, null, null, newAddress, amountToSend);
```

Now that we defined the “estimated gas”, we can use **gas **that value as one of the parameters for the transaction.

```csharp
var receiptFirstAmountSend = await web3.TransactionManager.SendTransactionAsync(senderAddress, gas, null, null, newAddress, amountToSend);
```
