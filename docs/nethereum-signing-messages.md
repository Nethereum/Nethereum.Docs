# Signing Messages

Sending transactions as messages allows for better interoperability, the following shows how to sign them. 

First, let's load our account in a Web3 object using our privateKey:

```csharp
            var account = new Account("0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7");
            var web3 = new Web3.Web3(account);

```
In order to sign a message, we need to declare the signer's address, the message itself and the signer's private key.  
```csharp
           var address = "0x12890d2cce102216644c59dae5baed380d84830c";
            var msg = "wee test message 18/09/2017 02:55PM";
            var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
```

Now, we need to instantiate a signer object:
```csharp
            var signer = new EthereumMessageSigner();
```

Using EncodeUTF8AndSign, we can sign the message using our private key:
```csharp
            var signature = signer.EncodeUTF8AndSign(msg, new EthECKey(privateKey));
```
It's possible to extract the signer's address using EncodeUTF8AndEcRecover:
```csharp
            var addressRec = signer.EncodeUTF8AndEcRecover(msg, signature);
```

