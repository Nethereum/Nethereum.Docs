# Estimating the cost of a transaction with Nethereum

Documentation about Nethereum can be found at: <https://docs.nethereum.com>

The purpose of this sample is to estimate the gas cost of a simple transaction and modify the assigned values of `gas` and `gasprice`.

## Ethereum and Gas: a primer

Gas is the pricing system used for running a transaction or contract in Ethereum.
The gas system is not very different from the use of kW-h for measuring electricity home use. One difference from actual energy market is that the originator of the transaction sets the price of gas, which the miner can accept or not, this causes an emergence of a market around gas. You can see the evolution of the price of gas at: <https://etherscan.io/chart/gasprice>.

The gas price per transaction or per contract is set up to deal with the Turing Complete nature of Ethereum and its EVM (Ethereum Virtual Machine Code) – the idea is to prevent infinite loops. If there is not enough Ether in the account to perform the transaction or message then it is considered invalid. The idea is to stop denial of service attacks from infinite loops, encourage efficiency in the code – and to make an attacker pay for the resources they use, from bandwidth through to CPU calculations through to storage.

Here are the terms needed to define the **gas** cost of a transaction:

* **Gas limit** refers to the maximum amount of gas you’re willing to spend on a particular transaction.

* **Gas price** refers to the amount of Ether you’re willing to pay for every unit of gas, and is usually measured in “Gwei”.

It would be difficult to send transaction without an idea of their cost in gas, fortunately  Ethereum provides ways to obtain a gas estimate prior to sending a transaction.

The following article explains how to anticipate the cost of an unsent transaction by returning an estimation.

##### A word of caution

Because of the Turing completeness of the EVM, it is easy to write functions that will take different code paths with wildly different gas costs. For example, a function could choose to take different code paths according to the value of some global state variable. The real code path taken in the function is not known until transaction execution time. Therefore the gas estimate can only give an approximation of the actual cost of a transaction.


!!! note
    You can run the below code directly in your browser by using Nethereum's playground at the following link:
[Smart Contracts: Smart Contracts Deployment, Querying, Transactions, Nonces, Estimating Gas, Gas Price](http://playground.nethereum.com/csharp/id/1007)

## Quick environment setup

```csharp
using Nethereum.Web3;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts.CQS;
using Nethereum.Util;
using Nethereum.Web3.Accounts;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.Contracts;
using Nethereum.Contracts.Extensions;
using System.Numerics;
```

### Web3

Web3 provides a simple interaction wrapper with Ethereum clients. To create an instance of Web3, we need to supply our Account and the RPC uri of the Ethereum client. In this scenario we will use Nethereum's public testchain, on the default RPC uri “http://testchain.nethereum.com:8545”

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var account = new Nethereum.Web3.Accounts.Account(privateKey);
var web3 = new Web3(account,"http://testchain.nethereum.com:8545");
```
## Contract setup and deployment
First let's declare our smart contracts BYTECODE, the function definitions and deploy our contract.  

```csharp
   public static string BYTECODE = "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";

    public StandardTokenDeployment() : base(BYTECODE){}

    [Parameter("uint256", "totalSupply")]
    public BigInteger TotalSupply { get; set; }
}

[Function("balanceOf", "uint256")]
public class BalanceOfFunction : FunctionMessage
{
    [Parameter("address", "_owner", 1)]
    public string Owner { get; set; }
}

[Function("transfer", "bool")]
public class TransferFunction : FunctionMessage
{
    [Parameter("address", "_to", 1)]
    public string To { get; set; }

    [Parameter("uint256", "_value", 2)]
    public BigInteger TokenAmount { get; set; }
}

var deploymentMessage = new StandardTokenDeployment
{
    TotalSupply = 100000
};

var deploymentHandler = web3.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
var transactionReceipt = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);
string contractAddress = transactionReceipt.ContractAddress;
```

### Setting up sender address

```csharp
var senderAddress = "0x12890d2cce102216644c59daE5baed380d84830c";

```

## Transfering token

Making a transfer will change the state of the blockchain, so in this scenario we will need to create a TransactionHandler using the TransferFunction definition.

In the transfer message, we will include the receiver address `To`, and the `TokenAmount` to transfer.

The final step is to Send the request, wait for the receipt to be “mined” and included in the blockchain.

```csharp
var receiverAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
var transferHandler = web3.Eth.GetContractTransactionHandler<TransferFunction>();
var transfer = new TransferFunction()
{
    To = receiverAddress,
    TokenAmount = 100
};
var transactionReceipt = await transferHandler.SendRequestAndWaitForReceiptAsync(contractAddress, transfer);
```

### Gas Price

Nethereum automatically sets the GasPrice if not provided by using the clients "GasPrice" call, which provides the average gas price from previous blocks.

If you want to have more control over the GasPrice these can be set in both `FunctionMessages` and `DeploymentMessages`.

The GasPrice is set in "Wei" which is the lowest unit in Ethereum, so if we are used to the usual "Gwei" units, this will need to be converted using the Nethereum Conversion utilities.

```csharp
  transfer.GasPrice =  Nethereum.Web3.Web3.Convert.ToWei(25, UnitConversion.EthUnit.Gwei);
```

### Estimating Gas

Nethereum does an automatic estimation of the total gas necessary to make the function transaction by calling the `EthEstimateGas` internally with the "CallInput".

If needed, this can be done manually, using the TransactionHandler and the "transfer" transaction FunctionMessage.

```csharp
 var estimate = await transferHandler.EstimateGasAsync(contractAddress, transfer);
 transfer.Gas = estimate.Value;
```

Now the transaction will have the correct amount of `gas` at the right `gasprice`:

```csharp
var secondTransactionReceipt = await transferHandler.SendRequestAndWaitForReceiptAsync(contractAddress, transfer);
var receiptHash = secondTransactionReceipt.TransactionHash;
```
