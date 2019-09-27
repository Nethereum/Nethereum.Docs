# Nethereum: Integrating With Azure And Quorum

This article demonstrates how to integrate with the Azure Blockchain Service and Quorum.

## 1 - Creating an [Azure Account](https://azure.microsoft.com/en-us/resources/videos/sign-up-for-microsoft-azure/) or [sign](https://azure.microsoft.com/en-us/account/) in if you already have one

## 2 - Creating A Quorum Blockchain Member On Your Azure Dashboard
![](set-up-blockchain-on-azure1.png)
Creating a Blockchain member will spin up a network with two validator nodes and one transaction node on Azure, create a consortium and make you a member of that consortium. If you create a member in an existing consortium, Azure will add your account as a member.

## Interacting with Quorum 

### Web3 setup and authentication

![](set-up-blockchain-on-azure3.png)

Select the name of your newly created consortium member, then select "transaction nodes", choose the node
you need to connect to from the list of nodes, then "sample code" and finally select the 'Nethereum' tab. You'll obtain a list of pre-filled methods you can pick from to connect to your particular Quorum instance.

#### Url basic authentication

Basic user/password authentication can be used by including the user name and password in the Url:

```https://<username>:<password>@membername.blockchain.azure.com:3200```

To create a read only instance of Web3 you will need to do just the following:

```csharp
var web3 = new Web3("https://membername:p455word@membername.blockchain.azure.com:3200");
var blockNumber = await web3.Eth.Blocks.GetBlockNumber.SendRequestAsync();
```
#### Token based authentication

Authentication tokens can be found on your Azure dashboard at ```home > {quorumMemberName} - Transaction nodes > {quorumMemberName} - Access Keys```
Access token authentication will use the following format:

```https://membername.blockchain.azure.com:3200/<token>```

Creating a read/write instance of Web3 will be as follows:

```csharp
var web32 = new Nethereum.Web3.Web3("https://membername.blockchain.azure.com:3200/<token>");
blockNumber = await web32.Eth.Blocks.GetBlockNumber.SendRequestAsync();
```

# Managed account and Contract interaction

To interact with the the Transaction node (sending transactions) you can create a Managed Account with transaction nodes address and password.
You can read more about Accounts here: https://nethereum.readthedocs.io/en/latest/accounts/

In this sample we create an instance of Web3 using a ManagedAccount address and password. 

Later on, we couple transactions that are executed using the ERC2O standard token service, one to deploy the smart contract, the other to transfer some tokens.

## Creating A Web3 Instance Using A Managed Account

```csharp
  var managedAccount = new ManagedAccount("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c", "password");
  var web3Managed = new Web3(managedAccount, "https://membername.blockchain.azure.com:3200/<token>");
  var balance = await web3Managed.Eth.GetBalance.SendRequestAsync("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c");
```
## Deploying A Token Contract

To deploy a contract, we can use its bytecode version and use Nethereum's generic token deployment function message definition;
```csharp
        public class StandardTokenDeployment : ContractDeploymentMessage
        {

                        public static string BYTECODE = "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";
                        public StandardTokenDeployment() : base(BYTECODE){}

                        [Parameter("uint256", "totalSupply")]
                        public BigInteger TotalSupply { get; set; }
            }
```
We can now deploy our token contract:

```csharp
                //New ERC20 smart contract
                var deploymentMessage = new StandardTokenDeployment
                {
                            TotalSupply = 100000
                };

                var deploymentHandler = web3Managed.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
                //Deploying
                var transactionReceipt = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);

                var contractAddress = transactionReceipt.ContractAddress;
```

Then we can make a Transfer transaction as follows:

```csharp
var receipt = await service.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830c", 10000000);
```
For more information on how to interact with smart contracts check the document here: https://nethereum.readthedocs.io/en/latest/nethereum-smartcontrats-gettingstarted/


## Interacting with Quorum in Private mode

Interacting with Quorum in private mode requires the specialised Web3Quorum object. This can be found in the Nuget Nethereum.Quorum.

### The Quorum account.

The QuorumAccount is a new type of Account which simplifies the interaction with smart contracts in Quorum private mode. In a similar way to the ManagedAccount or Account, it wil be created as follows:
```csharp
var coinbaseNode1 = "0xded453f2515e7287b0d94b9db710c0fffb3098a7";
var uriWithAccessTokenNode1 = "https://membername.blockchain.azure.com:3200/<token>";

//Initialising Web3Quorum with a custom QuorumAccount
var web3Private = new Web3Quorum(new QuorumAccount(coinbaseNode1), uriWithAccessTokenNode1);
```

The Quorum Account does not accept a password as it requires to be Unlocked before sending a transaction.
```csharp
//Unlock account to enable access
var unlocked = await web3Private.Personal.UnlockAccount.SendRequestAsync(coinbaseNode1, "password", 30);
```

### The Private transaction and Private nodes
To make a private transaction we will setup private nodes for our Quorum Web3 instance, these private nodes will be used for all the transactions made for Web3 until changed or removed.

```csharp
//Set the nodes to work in private mode for this web3 instance
  web3Private.SetPrivateRequestParameters(new[] { "LHTjKEqQPy6gbo4r9ouj8ztfbB+F7kWd9vosSmeQcEw=", "sXVr5ENaJeqAA8eTKm74f6epYTMcbsl8Ovp+Y8Q3dzA=" });
```
## Interacting with a smart contract
Interacting with the smart contract will now be the same as with any other smart contract, but now all the transactions and smart contract interactions will only be visible to members in the list.

```csharp
//Deploying new ERC20 smart contract using the Standard token library service

  var deploymentMessage1 = new StandardTokenDeployment
  {
      TotalSupply = 100000
  };

  var deploymentHandler1 = web3Private.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
  //Deploying
  var transactionReceipt1 = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);
  var contractAddress1 = transactionReceipt1.ContractAddress;

  var receiverAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
  var transfer = new TransferFunction()
      {
          To = receiverAddress,
          TokenAmount = 100
      };

  var transferHandler = web3Private.Eth.GetContractTransactionHandler<TransferFunction>();
  var transactionReceipt2 = await transferHandler.SendRequestAndWaitForReceiptAsync(contractAddress1, transfer);

```

### Full Sample
```csharp
using Nethereum.Web3;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts.CQS;
using Nethereum.Util;
using Nethereum.Web3.Accounts;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.Contracts;
using Nethereum.Contracts.Extensions;
using Nethereum.Web3.Accounts.Managed;
using System;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;
using Nethereum.Quorum;


public class Program
{
        public class StandardTokenDeployment : ContractDeploymentMessage
        {

                        public static string BYTECODE = "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";
                        public StandardTokenDeployment() : base(BYTECODE){}

                        [Parameter("uint256", "totalSupply")]
                        public BigInteger TotalSupply { get; set; }
            }

    [Function("transfer", "bool")]
    public class TransferFunction : FunctionMessage
    {
        [Parameter("address", "_to", 1)]
        public string To { get; set; }

        [Parameter("uint256", "_value", 2)]
        public BigInteger TokenAmount { get; set; }
    }

    [Function("balanceOf", "uint256")]
    public class BalanceOfFunction : FunctionMessage
    {
        [Parameter("address", "_owner", 1)]
        public string Owner { get; set; }
    }

    static async Task Main(string[] args)
    {
                var web3 = new Web3("https://nethereummember1.blockchain.azure.com:3200/<token>");

                var blockNumber = await web3.Eth.Blocks.GetBlockNumber.SendRequestAsync();
                Console.WriteLine(blockNumber.Value);

                //This is the member address and the password
                var managedAccount = new ManagedAccount("0x1a5123c35a8abf9ee0be1bb9409f6003578ebb8a", "password");
              var web3Managed = new Web3(managedAccount, "https://nethereummember1.blockchain.azure.com:3200/<token>_");
                //Balance of member account should be 0 as we don't need Ether
              var balance = await web3Managed.Eth.GetBalance.SendRequestAsync("0x1a5123c35a8abf9ee0be1bb9409f6003578ebb8a");

                //New ERC20 smart contract
                var deploymentMessage = new StandardTokenDeployment
                {
                            TotalSupply = 100000
                };

                var deploymentHandler = web3Managed.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
                //Deploying
                var transactionReceipt = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);

                var contractAddress = transactionReceipt.ContractAddress;

   var coinbaseNode1 = "0xded453f2515e7287b0d94b9db710c0fffb3098a7";
   var uriWithAccessTokenNode1 = "https://nethereummember1.blockchain.azure.com:3200/<token>_";

//Initialising Web3Quorum with a custom QuorumAccount
var web3Private = new Web3Quorum(new QuorumAccount(coinbaseNode1), uriWithAccessTokenNode1);
var unlocked = await web3Private.Personal.UnlockAccount.SendRequestAsync(coinbaseNode1, "password", 30);

//Set the nodes to work in private mode for this web3 instance
 web3Private.SetPrivateRequestParameters(new[] { "8pZ4ekcWwnmQsz/Ea4Y/djWveSm57yQ4CZx79DwyOSk=", "UzQSRcULS1jHCFmcQkAoYh5vt7nL9U8pfy26qB+gy00=" });

//Deploying new ERC20 smart contract using the Standard token library service

  var deploymentMessage1 = new StandardTokenDeployment
  {
      TotalSupply = 100000
  };

  var deploymentHandler1 = web3Private.Eth.GetContractDeploymentHandler<StandardTokenDeployment>();
  //Deploying
  var transactionReceipt1 = await deploymentHandler.SendRequestAndWaitForReceiptAsync(deploymentMessage);

  var contractAddress1 = transactionReceipt1.ContractAddress;

  var receiverAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
  var transfer = new TransferFunction()
      {
          To = receiverAddress,
          TokenAmount = 100
      };
  var transferHandler = web3Private.Eth.GetContractTransactionHandler<TransferFunction>();
  var transactionReceipt2 = await transferHandler.SendRequestAndWaitForReceiptAsync(contractAddress1, transfer);
    }
}
```
    
