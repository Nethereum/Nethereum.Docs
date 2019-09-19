# Nethereum: Integrating With Azure And Quorum

This article demonstrates how to integrate with the Azure Blockchain Service and Quorum.

For the sake of simplicity, this article is based on a sample using the Standard Token Library Service, you can generate the same service using one of Nethereum Code generators using VsCode, Console, web ui etc.
For more info: https://nethereum.readthedocs.io/en/latest/nethereum-code-generation/

## Setting Up Quorum On Azure 
Our documentation dedicates an article on [how to spin up an instance of Quorum on Azure](set-up-blockchain-on-azure.md)
## Interacting with Quorum 
It is assumed you have already set up validator nodes and transaction nodes as per [this article](set-up-blockchain-on-azure.md).

### Web3 setup and authentication

### Url basic authentication

Basic user/password authentication can be used by including the user name and password in the Url:

```https://<username>:<password>@juanmemberq1.blockchain.azure.com:3200```

To create a read only instance of Web3 you will need to do just the following:

```csharp
var web3 = new Web3("https://juanmemberq1:p455word@juanmemberq1.blockchain.azure.com:3200");
var blockNumber = await web3.Eth.Blocks.GetBlockNumber.SendRequestAsync();
```
### Token based authentication
Access token authentication will use the following format:
```https://juanmemberq1.blockchain.azure.com:3200/<token>```

Creating a read only instance of Web3 will be as follows:

```csharp
var web32 = new Nethereum.Web3.Web3("https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
blockNumber = await web32.Eth.Blocks.GetBlockNumber.SendRequestAsync();
```

# Managed account and Contract interaction

To interact with the the Transaction node (sending transactions) you can create a Managed Account with transaction nodes address and password.
You can read more about Accounts here: https://nethereum.readthedocs.io/en/latest/accounts/

In this sample we create an instance of Web3 using a ManagedAccount address and password. 

Later on, we couple transactions that are executed using the ERC2O standard token service, one to deploy the smart contract, the other to transfer some tokens.


```csharp
  var managedAccount = new ManagedAccount("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c", "p455word");
  var web3Managed = new Web3(managedAccount, "https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
  var balance = await web3Managed.Eth.GetBalance.SendRequestAsync("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c");

  var service = await StandardTokenService.DeployContractAndGetServiceAsync(web3Managed, new EIP20Deployment()
  {
      InitialAmount = BigInteger.Parse("1000000000000000000000000"),
      DecimalUnits = 18,
      TokenName = "TEST",
      TokenSymbol = "TST"
  });

  var receipt = await service.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830c", 10000000);
```
In one single line we have deployed the service, using the EIP20Deployment message providing the constructor parameters for the Initial Amount, Decimal Units, TokeName and Symbol.
The constructor parameters are the same as the Solidity Smart Contract constructor parameters.
```csharp
  var service = await StandardTokenService.DeployContractAndGetServiceAsync(web3Managed, new EIP20Deployment()
  {
      InitialAmount = BigInteger.Parse("1000000000000000000000000"),
      DecimalUnits = 18,
      TokenName = "TEST",
      TokenSymbol = "TST"
  });
```

Then we can make a Transfer transaction as follows:

```csharp
var receipt = await service.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830c", 10000000);
```
For more information on how to interact with smart contracts check the document here: https://nethereum.readthedocs.io/en/latest/nethereum-smartcontrats-gettingstarted/

## Account interaction
To interact using the Account Private key, we will use an Account instead of a Managed Account.

```csharp
var web3MyAccount = new Web3(new Account("0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7"), "https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
var service2 = new StandardTokenService(web3MyAccount, service.ContractHandler.ContractAddress);
var receipt2 = await service2.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830d", 10000);
var balanceMyAccount = await service2.BalanceOfQueryAsync("0x12890d2cce102216644c59daE5baed380d84830c");
```

The rest of the interactions are the same.

### Full Sample
```csharp
public class QuorumNormalTest
    {
        public async Task Run()
        {
            //Basic Authentication
            var web3 = new Web3("https://juanmemberq1:p455word@juanmemberq1.blockchain.azure.com:3200");
            var blockNumber = await web3.Eth.Blocks.GetBlockNumber.SendRequestAsync();


            //access keys
            var web32 = new Nethereum.Web3.Web3("https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
            blockNumber = await web32.Eth.Blocks.GetBlockNumber.SendRequestAsync();


            //access keys websocket
            var websocketClient =
                new WebSocketClient(("wss://juanmemberq1.blockchain.azure.com:3300/QNSQSAAE_WoMyS06TPH8KVa2"));

            var web3WebSocket = new Web3(websocketClient);
            blockNumber = await web3WebSocket.Eth.Blocks.GetBlockNumber.SendRequestAsync();


            //retrieving all accounts of the node
            var accounts = await web3.Eth.Accounts.SendRequestAsync();

            var managedAccount = new ManagedAccount("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c", "p455word");
            var web3Managed = new Web3(managedAccount, "https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
            var balance = await web3Managed.Eth.GetBalance.SendRequestAsync("0xca1e76c9876e5ba1e7c307696a7ea48eb25eec8c");
          

            var service = await StandardTokenService.DeployContractAndGetServiceAsync(web3Managed, new EIP20Deployment()
            {
                InitialAmount = BigInteger.Parse("1000000000000000000000000"),
                DecimalUnits = 18,
                TokenName = "TEST",
                TokenSymbol = "TST"
            });

            var receipt = await service.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830c", 10000000);


            var web3MyAccount = new Web3(new Account("0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7"), "https://juanmemberq1.blockchain.azure.com:3200/QNSQSAAE_WoMyS06TPH8KVa2");
            var service2 = new StandardTokenService(web3MyAccount, service.ContractHandler.ContractAddress);
            var receipt2 = await service2.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830d", 10000);
            var balanceMyAccount = await service2.BalanceOfQueryAsync("0x12890d2cce102216644c59daE5baed380d84830c");


            var websocketClient2 =
               new WebSocketClient("wss://juanmemberq1.blockchain.azure.com:3300/QNSQSAAE_WoMyS06TPH8KVa2");

            var web3WebSocket2 = new Web3(new Account("0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7"), websocketClient);

            var service3 = await StandardTokenService.DeployContractAndGetServiceAsync(web3WebSocket2, new EIP20Deployment()
            {
                InitialAmount = BigInteger.Parse("1000000000000000000000000"),
                DecimalUnits = 18,
                TokenName = "TEST",
                TokenSymbol = "TST"
            });
            var receipt3 = await service3.TransferRequestAndWaitForReceiptAsync("0x12890d2cce102216644c59daE5baed380d84830d", 10000);
            var balanceMyAccount2 = await service2.BalanceOfQueryAsync("0x12890d2cce102216644c59daE5baed380d84830c");

        }
    }

```

## Interacting with Quorum in Private mode
Interacting with Quorum in private mode requires the specialised Web3Quorum object. This can be found in the Nuget Nethereum.Quorum.

### The Quorum account.
The QuorumAccount is a new type of Account which simplifies the interaction with smart contracts in Quorum private mode. In a similar way to the ManagedAccount or Account, it wil be created as follows:
```csharp
var coinbaseNode1 = "0x83e0ebe69d8758f9450425fa39ef08692e55340d";
var uriWithAccessTokenNode1 = "https://juanquorum1.blockchain.azure.com:3200/nNkcS8DyDSCLIC9oAoCw1orS";

//Initialising Web3Quorum with a custom QuorumAccount
var web3Private = new Web3Quorum(new QuorumAccount(coinbaseNode1), uriWithAccessTokenNode1);
```

The Quorum Account does not accept a password as it requires to be Unlocked before sending a transaction.
```csharp
 //Unlock account to enable access
  var unlocked = await web3Private.Personal.UnlockAccount.SendRequestAsync(coinbaseNode1, "P455word1?1234", 30);
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
  var erc20service = await StandardTokenService.DeployContractAndGetServiceAsync(web3Private, new EIP20Deployment()
  {
      InitialAmount = BigInteger.Parse("1000000000000000000000000"),
      DecimalUnits = 18,
      TokenName = "TEST",
      TokenSymbol = "TST",
  });

  //After deploying the smart contract the owner "coinbaseNode1" will have a balance of 1000000000000000000000000
  var balanceOwnerAccount = await erc20service.BalanceOfQueryAsync(coinbaseNode1);

  //Transfering 10000
  var transferReceipt = await erc20service.TransferRequestAndWaitForReceiptAsync("0xc45ed03295fdb5667206c4c18f88b41b4f035358", 10000);

```

### Full Sample
```csharp
//The quorum account
  var coinbaseNode1 = "0x83e0ebe69d8758f9450425fa39ef08692e55340d";
  var uriWithAccessTokenNode1 = "https://juanquorum1.blockchain.azure.com:3200/nNkcS8DyDSCLIC9oAoCw1orS";

  //Initialising Web3Quorum with a custom QuorumAccount
  var web3Private = new Web3Quorum(new QuorumAccount(coinbaseNode1), uriWithAccessTokenNode1);

  //Set the nodes to work in private mode for this web3 instance
  web3Private.SetPrivateRequestParameters(new[] { "LHTjKEqQPy6gbo4r9ouj8ztfbB+F7kWd9vosSmeQcEw=", "sXVr5ENaJeqAA8eTKm74f6epYTMcbsl8Ovp+Y8Q3dzA=" });

  //Unlock account to enable access
  var unlocked = await web3Private.Personal.UnlockAccount.SendRequestAsync(coinbaseNode1, "P455word1?1234", 30);

  //Deploying new ERC20 smart contract using the Standard token library service
  var erc20service = await StandardTokenService.DeployContractAndGetServiceAsync(web3Private, new EIP20Deployment()
  {
      InitialAmount = BigInteger.Parse("1000000000000000000000000"),
      DecimalUnits = 18,
      TokenName = "TEST",
      TokenSymbol = "TST",
  });

  //After deploying the smart contract the owner "coinbaseNode1" will have a balance of 1000000000000000000000000
  var balanceOwnerAccount = await erc20service.BalanceOfQueryAsync(coinbaseNode1);

  //Transfering 10000
  var transferReceipt = await erc20service.TransferRequestAndWaitForReceiptAsync("0xc45ed03295fdb5667206c4c18f88b41b4f035358", 10000);

  //Validate that we get the new balance
  var balanceOwnerAfterTransfer = await erc20service.BalanceOfQueryAsync(coinbaseNode1);
  var balanceReceiverAccount = await erc20service.BalanceOfQueryAsync("0xc45ed03295fdb5667206c4c18f88b41b4f035358");

  //Create a web3 instance in a different node not included in the Private list
  var web3NoAccess = new Web3("https://juanquorum3-juanquorum1.blockchain.azure.com:3200/ekgKWCEhxcq6d_HH3N10g9W0");

  //initialising a new StardandTokenService with the same contract address
  var erc20noAccess = new StandardTokenService(web3NoAccess, erc20service.ContractHandler.ContractAddress);
  //validate we don't receive any amount
  var balanceOwnerAccountNoAccess = await erc20noAccess.BalanceOfQueryAsync(coinbaseNode1);

```

