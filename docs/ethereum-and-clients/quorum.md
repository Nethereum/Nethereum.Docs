# Quorum

[Quorum](https://github.com/jpmorganchase/quorum-docs/blob/master/Quorum%20Whitepaper%20v0.1.pdf) is a private/permissioned, blockchain based on the official go implementation of the Ethereum protocol. Quorum client is a forked version of Ethereum's Geth.

Quorum focuses on privacy, unlike Ethereum mainnet which reveals all of its transactions in the clear, Quorum enables private transactions. Quorum also relies on a vote-based form of consensus.

## Install

The simplest and fastest way to setup an instance of Quorum is to use [ConsenSys Quorum Network Manager](https://github.com/ConsenSys/QuorumNetworkManager) (you can find a single script setup option [here](
https://github.com/ConsenSys/QuorumNetworkManager/releases/tag/v0.6-alpha))

Once your Quorum chain is up and running, identify the IP address of one of its running nodes.
Quorum Network Manager returns an ``` enode ``` address ending in an address IP as in this example:

```` enode: enode://71809a795b94d24f0b0cfa2fbd8361ce055f4feb710e6a65614767cd72ed8ecd1bae155c141e097bc74f44dc53cbfc308f3db703283c200eb3b40a8a77e92e82@67.247.25.158:20000?raftport=40000 ```

## Connecting to Quorum

Add the Nethereum.Web3 nuget package and the "Using" statement to use Nethereum's Quorum methods.

``` #r "Nethereum.Web3" ```
``` using Nethereum.Web3; ```

Then set a Web3 instance using your node's IP address and 20010 as port:

``` var web3Node1 = new Web3Quorum("http://46.165.246.181:20010"); ```


## Querying a node

You can now try to query a node with:

``` var balance = await web3Node1.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"); ```