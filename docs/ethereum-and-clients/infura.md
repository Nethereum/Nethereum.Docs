## Infura

Since running a local Ethereum/IPFS node is becoming more and more challenging, [Infura](www.infura.io) provides a scalable infrastructure of nodes that can be accessed via standard libraries and API (JSON-RPC API, web3 libraries).

The following will help you connect to [Infura](www.infura.io) and retrieve the balance of an account from the mainnet (live Ethereum). Infura provides a set of public nodes removing the need to have a local or maintained client fully synchronised with the main Ethereum network.

## Setting up

Add a package reference to the Nethereum.Web3 nuget package and the "Using" statement to use Nethereum's Quorum methods.

```csharp
#r "Nethereum.Web3"
```
Then we need to add our required namespaces for Nethereum:

```csharp
using Nethereum.Web3;
```

# Retrieving the balance of an account on main net using Infura.

The next step is to create an instance of Web3, with the infura url for mainnet.

```csharp
var web3 = new Web3("https://mainnet.infura.io");
```

Using the Eth API we can execute the GetBalance request asynchronously, for our selected account. In this scenario the chosen account is the Ethereum Foundation's. “0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae”

```csharp
var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
```

The amount returned is in Wei, the lowest unit of value. We can convert this to Ether using the Convertion utility:

```csharp
var etherAmount = Web3.Convert.FromWei(balance.Value);
```
