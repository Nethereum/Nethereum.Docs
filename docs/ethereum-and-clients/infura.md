# INFURA 

Since running a local Ethereum/IPFS node is becoming more and more challenging, [Infura](http://www.infura.io) provides a scalable infrastructure of nodes that can be accessed via standard libraries and API (JSON-RPC API, web3 libraries), eliminating the need to have a local or maintained client fully synchronised with the main Ethereum network.

The following will take you through the steps of connecting to [Infura](https://www.infura.io), retrieving the balance of an account from the mainnet (live Ethereum) as well as checking on the chain ID and latest block number.

If you would like to execute the code in this article you can do so by using its [workbook version](Nethereum.Workbooks/docs/nethereum-gettingstarted-infura.workbook)
## Getting started using Infura with Nethereum

The first step to use INFURA is to [sign up](https://infura.io/register) and get an API key. The next step is to choose which Ethereum network to connect to — either the mainnet, or the Kovan, Goerli, Rinkeby, or Ropsten test networks. Both of these will be used in the url we use to initial Nethereum with the format:`https://<network>.infura.io/v3/YOUR-PROJECT-ID`.

For this sample, we’ll use a special API key `7238211010344719ad14a89db874158c`, but for your own project you’ll need your own key.

```csharp
#r "Nethereum.Web3"
```

```csharp
using Nethereum.Web3;
```

Let’s create an instance of Web3, with the infura url for mainnet.

```csharp
var web3 = new Web3("https://mainnet.infura.io/v3/7238211010344719ad14a89db874158c");
```

Using the Eth API we can execute the GetBalance request asynchronously, for our selected account. In this scenario the chosen account belongs to the Ethereum Foundation. “0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae”

```csharp
var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
```

The amount returned is in Wei, the lowest unit of value. We can convert this to Ether using the Convertion utility:

```csharp
var etherAmount = Web3.Convert.FromWei(balance.Value);
```

Using the Net API, we can call and find out which network we’re connected to. This will change depending on which network we chose to connect to previously. For example, Kovan will return `42` and mainnet would be `1`.

```csharp
var networkId = await web3.Net.Version.SendRequestAsync();
```

Next, using the Eth API, we’ll call to get the latest block which has been mined in this network.

```csharp
var latestBlockNumber = await web3.Eth.Blocks.GetBlockNumber.SendRequestAsync();
var latestBlock = await web3.Eth.Blocks.GetBlockWithTransactionsHashesByNumber.SendRequestAsync(latestBlockNumber);
```

One important thing to know when using hosted infrastructure like Infura: INFURA doesn’t store any private keys, so any signing must be done locally and then the raw transaction passed on to the service. Nethereum makes this easy with the `Account` object. See the [Using account objects](https://nethereum.readthedocs.io/en/latest/Nethereum.Workbooks/docs/nethereum-using-account-objects/#sending-a-transaction) for more details.
