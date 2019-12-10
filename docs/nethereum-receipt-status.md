# Using Receipt Status


Since the Byzantium fork, Ethereum provides with a way to know if a transaction succeeded by checking its receipt `status`. A receipt status can have a value of `0` or `1` which translate into:

* `0` transaction has failed (for whatever reason)

* `1` transaction was succesful.

## How to retrieve a transaction status with Nethereum

Ethereum allows to retrieve this property after retrieving a transaction receipt via methods such as `SendTransactionAndWaitForReceiptAsync`,  `SendRequestAndWaitForReceiptAsync`, `TransferRequestAndWaitForReceiptAsync`, or `DeployContractAndWaitForReceiptAsync`

We'll demonstrate how to use transactions `status` after deploying a contract and after a token transfer.

## Pre-requisites:

```csharp
using Nethereum.RPC.Eth.Transactions;
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.Web3.Accounts.Managed;
using Nethereum.Signer;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.KeyStore;
using Nethereum.Hex.HexConvertors;
using Nethereum.Hex.HexTypes;
using Nethereum.RPC.NonceServices;
using Nethereum.RPC.TransactionReceipts;
using System.Threading.Tasks;
using Nethereum.RPC.Eth.DTOs;
```

We first need to create an instance of an account, then use it to instantiate a `web3` object in order to interact with Ethereum.

Let's first declare our new `Account`:

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var account = new Nethereum.Web3.Accounts.Account(privateKey);
```

### Web3

Web3 provides a simple interaction wrapper with Ethereum clients. To create an instance of Web3, we need to supply our Account and the RPC uri of the Ethereum client. In this scenario we will use Nethereum's public testchain uri: “http://testchain.nethereum.com:8545”

```csharp
var web3 = new Web3(account,"http://testchain.nethereum.com:8545");
```

Let's now deploy our contract.
In the context of this post, the contract to deploy is `StandardTokenDeployment`:

```csharp
public class StandardTokenDeployment : ContractDeploymentMessage
{

            public static string BYTECODE = "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";

    public StandardTokenDeployment() : base(BYTECODE){}

    [Parameter("uint256", "totalSupply")]
    public BigInteger TotalSupply { get; set; }
}
```
We'll deploy this contract with an initial supply of 100000, by using Nethereum's StandardTokenDeployment function definition:

```csharp
var deploymentMessage = new StandardTokenDeployment
{
    TotalSupply = 100000
};
```

The deployment method will return a receipt object, here `deploymentTransactionReceipt`

```csharp
var deploymentHandler = web3.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
var deploymentTransactionReceipt = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);
```

We can now get the value of the transaction `status` which will give us the outcome of our deployment transaction, `1` for success, `0` for failure.

```csharp
var deploymentValidityStatus = deploymentTransactionReceipt.Status.Value;
```

The function definitions of the smart contract we just deployed are as follows: 

```csharp
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
```

We can also assess if any other transaction has been succesful, for example, we can assess if a token transfer has been performed:

```csharp
var receiverAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
var transferHandler = web3.Eth.GetContractTransactionHandler<TransferFunction>();
var transfer = new TransferFunction()
{
    To = receiverAddress,
    TokenAmount = 100
};
var transactionReceipt = await transferHandler.SendRequestAndWaitForReceiptAsync(deploymentTransactionReceipt.ContractAddress, transfer);
var transferValidityStatus = transactionReceipt.Status.Value;
```