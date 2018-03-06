# Quorum

[Quorum](https://github.com/jpmorganchase/quorum-docs/blob/master/Quorum%20Whitepaper%20v0.1.pdf) is a private/permissioned, blockchain based on the official go implementation of the Ethereum protocol. Quorum client is a forked version of Ethereum's Geth.

Quorum focuses on privacy, unlike Ethereum mainnet which reveals all of its transactions in the clear, Quorum enables private transactions. Quorum also relies on a vote-based form of consensus.

## Install

The simplest and fastest way to setup an instance of Quorum is to use [ConsenSys Quorum Network Manager](https://github.com/ConsenSys/QuorumNetworkManager) (you can find a single script setup option [here](
https://github.com/ConsenSys/QuorumNetworkManager/releases/tag/v0.6-alpha))

Once your Quorum chain is up and running, identify the IP address of one of its running nodes.
Quorum Network Manager returns an ``` enode ``` address ending in an address IP as in this example:

``` enode: enode://71809a795b94d24f0b0cfa2fbd8361ce055f4feb710e6a65614767cd72ed8ecd1bae155c141e097bc74f44dc53cbfc308f3db703283c200eb3b40a8a77e92e82@67.247.25.158:20000?raftport=40000 ```

## Connecting to Quorum

Add the Nethereum.Portable nuget package and the "Using" statement to use Nethereum's Quorum and Web3.

``` #r "Nethereum.Portable" ```

``` using Nethereum.Quorum; ```
``` using Nethereum.Web3; ```


Then set a Web3 instance using your node's IP address and 20010 as port (if you are using Quorum Network Management):

``` var web3Node1 = new Web3Quorum("http://46.165.246.181:20010"); ```


## Querying with Quorum

### Creating an account

``` var newAccount = await web3Node1.Personal.NewAccount.SendRequestAsync("password"); ```

### Retrieving an account balance

``` var balance = await web3Node1.Eth.GetBalance.SendRequestAsync("0xe68bf709a914d3a027d3d90686a3b975c3b82379"); ```

### Retrieving existing accounts

``` var accounts = await web3Node1.Eth.Accounts.SendRequestAsync() ```

## Privatefor

The ``` privateFor ``` parameter causes Quorum to treat a transaction as private. ``` PrivateFor ``` can take multiple addresses in a comma separated list, those addresses will be the only ones allowed to access private transactions in the clear. Those not on the list will simply skip private transactions.

``` PrivateFor ``` will be set as following:

- ``` var web3Node1 = new Web3Quorum(urlNode1); ```
- ``` var privateFor = new List<string>(new[] { "ROAZBWtSacxXQrOe3FGAqJDyJjFePR5ce4TSIzmJ0Bc=" }); ```
``` web3Node1.SetPrivateRequestParameters(privateFor); ```

Afterwards all the transactions will use the PrivateFor parameter.

- ``` var contract = web3Node1.Eth.GetContract(abi, address); ```
- ``` var functionSet = contract.GetFunction("set"); ```
- ``` var txnHash = await transactionService.SendRequestAsync(() => functionSet.SendTransactionAsync(account, 4)); ```
