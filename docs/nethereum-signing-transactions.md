# Signing Transactions

Signing transactions is a requirement on Ethereum where transactions need to be verifiable. Transactions can be signed either "offline" without using a client or "online" by letting a client manage the private key and sign the transaction. 

### Offline transaction signing

The "OfflineTransactionSigning" class enables the signing of transactions, get the sender address or verify already signed transactions without interacting directly with the client.

```csharp
web3.OfflineTransactionSigning.SignTransaction
web3.OfflineTransactionSigning.GetSenderAddress
web3.OfflineTransactionSigning.VerifyTransaction
```

To provide offline transaction signing in Nethereum you can do the following:

First, you will need your private key, and sender address. You can retrieve the sender address from your private key using Nethereum.Core.Signing.Crypto.EthECKey.GetPublicAddress(privateKey); if you only have the private key.

```csharp
var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
var senderAddress = "0x12890d2cce102216644c59daE5baed380d84830c";
```

Now using web3 first you will need to retrieve the total number of transactions of your sender address.

```csharp
var web3 = new Web3(); var txCount = await web3.Eth.Transactions.GetTransactionCount.SendRequestAsync(senderAddress);
```

The txCount will be used as the nonce to sign the transaction.

Now using web3 again, you can build an encoded transaction as following:

```csharp
var encoded = web3.OfflineTransactionSigning.SignTransaction(privateKey, receiveAddress, 10, txCount.Value);
```

If you need to include the data and gas there are overloads for it.

You can verify an encoded transaction:

```csharp
Assert.True(web3.OfflineTransactionSigning.VerifyTransaction(encoded));
```

Or get the sender address from an encoded transaction:

```csharp
web3.OfflineTransactionSigning.GetSenderAddress(encoded);
```

To send the encoded transaction you will use the RPC method "SendRawTransaction"

```csharp
var txId = await web3.Eth.Transactions.SendRawTransaction.SendRequestAsync("0x" + encoded);
```

The complete example can be found on the [Transactions signing unit tests](https://github.com/Nethereum/Nethereum/blob/master/src/Nethereum.Web3.Tests/TransactionSigningTests.cs)
or you can see a complete use case on the [Game sample](https://github.com/Nethereum/Nethereum.Game.Sample/) and its service [Source code](https://github.com/Nethereum/Nethereum.Game.Sample/blob/master/Forms/Core/Ethereum/GameScoreService.cs)

### Transaction Request To Offline Signed Transaction Interceptor

The web3 transaction request to an offline signed transaction interceptor, provides a mechanism to intercept all transactions and automatically offline sign them and send a raw transaction with a preconfigured private key.

```csharp
  var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
  var senderAddress = "0x12890d2cce102216644c59daE5baed380d84830c";

  var web3 = new Web3();
  var transactionInterceptor = new TransactionRequestToOfflineSignedTransactionInterceptor(senderAddress, privateKey, web3);
  web3.Client.OverridingRequestInterceptor = transactionInterceptor;
```

The interceptor requires the private key, the corresponding address and an instance of web3. Once the web3 rpc client is configured all the requests will be the same.

```csharp
    var txId = await web3.Eth.DeployContract.SendRequestAsync(abi, contractByteCode, senderAddress, new HexBigInteger(900000), 7);
```
### Signing Transactions Online

Signing transactions online can be simply done by using a managed account (managed accounts enable clients like Geth to manage private key's account when signing a transaction). 

```csharp
var senderAddress = "0x12890d2cce102216644c59daE5baed380d84830c";
var password = "password";

var account = new ManagedAccount(senderAddress, password);
var web3 = new Web3.Web3(account);
```

When transferring an amount to another address using the transaction manager the signing will be done automatically:

```csharp
await web3.TransactionManager.SendTransactionAsync(account.Address, addressTo, new HexBigInteger(20));

```

