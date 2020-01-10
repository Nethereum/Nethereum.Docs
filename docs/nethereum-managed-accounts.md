# Using Nethereum managed accounts

Documentation about Nethereum can be found at: <https://docs.nethereum.com>

**Note:** the following code relies on messages. If you are not familiar with the use of messages in Nethereum, they are explained in ["Getting started with Smart Contracts"](Nethereum.Workbooks/docs/nethereum-smartcontrats-gettingstarted.workbook)


## The use for Managed accounts

Clients retrieve the private key for an account (if stored on their keystore folder) using a password provided to decrypt the file. This is done when unlocking an account, or just at the time of sending a transaction if using `personal_sendTransaction` with a password.

Having an account unlocked for a certain period of time might be a security issue, so the prefered option in this scenario, is to use the rpc method `personal_sendTransaction`.

Nethereum.Web3 wraps this functionality by using a ManagedAccount, having the managed account storing the account address and the password information.

An instance `ManagedAccount` object can simply be declared using the "sender" account public address as well as its password.

This article explains how to use managed accounts to facilitate private key management and secure transactions.

## Quick environment setup

```csharp
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.Web3.Accounts.Managed;
using Nethereum.Hex.HexTypes;
using Nethereum.Hex.HexConvertors;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts.CQS;
using Nethereum.Util;
using Nethereum.Contracts;
using Nethereum.Contracts.Extensions;
using System.Numerics;
```

### Web3

Web3 provides a simple interaction wrapper with Ethereum clients. To create an instance of Web3, we need to supply our Account and the RPC uri of the Ethereum client. In this scenario we recommend installing a geth instance of [Testchains](https://github.com/Nethereum/TestChains) which is very responsive as it operates on a PoA consensus.  

```csharp
var senderAddress = "0x12890d2cce102216644c59daE5baed380d84830c";
var password = "password";
var account = new ManagedAccount(senderAddress, password);
var web3 = new Nethereum.Web3.Web3(account. "http://127.0.0.1:8545");
```

When used in conjuction with Web3, now in the same way as an "Account", you can:

### Deploy a contract

In the context of this post, the contract to deploy is `StandardTokenDeployment`


```csharp
public class StandardTokenDeployment : ContractDeploymentMessage
{

            public static string BYTECODE = "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";

    public StandardTokenDeployment() : base(BYTECODE){}

    [Parameter("uint256", "totalSupply")]
    public BigInteger TotalSupply { get; set; }
}

```

Now let's define the function messages that we'll use along this tutorial:


### Deployment message

```csharp
var deploymentMessage = new StandardTokenDeployment
{
    TotalSupply = 100000
};
```

### Balance

```csharp
[Function("balanceOf", "uint256")]
public class BalanceOfFunction : FunctionMessage
{
    [Parameter("address", "_owner", 1)]
    public string Owner { get; set; }
}

### Transfer

[Function("transfer", "bool")]
public class TransferFunction : FunctionMessage
{
    [Parameter("address", "_to", 1)]
    public string To { get; set; }

    [Parameter("uint256", "_value", 2)]
    public BigInteger TokenAmount { get; set; }
}
```

### Contract Deployment

```csharp
var deploymentHandler = web3.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
var transactionReceipt1 = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);
var contractAddress1 = transactionReceipt1.ContractAddress;
```

### Interacting with a Contract

Once we have deployed the contract, we can start interacting with it.

#### Querying the balance of an account

To retrieve the balance of an address we can create an instance of the BalanceFunction message and set the parameter as our account "Address", since we are the "owner" of the Token, the full balance has been assigned to us.

```csharp
var balanceOfFunctionMessage = new BalanceOfFunction()
{
    Owner = account.Address,
};

var balanceHandler = web3.Eth.GetContractQueryHandler<BalanceOfFunction>();
var balance = await balanceHandler.QueryAsync<BigInteger>(contractAddress1, balanceOfFunctionMessage);
```

#### Transfer

Lastly let's perform a token transfer. In this scenario we will need to create a TransactionHandler using the TransferFunction definition.

In the transfer message, we will include the receiver address "To", and the "TokenAmount" to transfer.

The final step is to Send the request, wait for the receipt to be “mined” and get the contract address:

```csharp
var receiverAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
var transferHandler = web3.Eth.GetContractTransactionHandler<TransferFunction>();
var transfer = new TransferFunction()
{
    To = receiverAddress,
    TokenAmount = 100
};
var transactionReceipt2 = await transferHandler.SendRequestAndWaitForReceiptAsync(contractAddress1, transfer);
var transactionHash = transactionReceipt2.TransactionHash;
```
