# Creating a Scrypt Based KeyStore with Nethereum

This article explains how to create a keystore file using Nethereum.  


!!! note
    You also have the possibility to run similar code directly in your browser
    by using Nethereum's playground at the following link:
    [Key Store: Create Scrypt based KeyStore using custom params](http://playground.nethereum.com/csharp/id/1021)


Definition: A keystore is a JSON-encoded file that contains a single (randomly generated) private key, encrypted by a passphrase for extra security (using https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition#scrypt).
Keystores are a standard way to store private keys locally to let clients such as Geth handle privateKey/signin for you. 
Nethereum offers a dedicated 'keystore' service to facilitate the creation and management of keystore files.

Required assemblies:
```csharp
using System;
using System.Text;
using Nethereum.Hex.HexConvertors.Extensions;
using System.Threading.Tasks;
using Nethereum.Web3;
using Nethereum.KeyStore.Model;
```

### 1- Creating a Keystore File:

We first need to create an instance of `KeyStoreScryptService`: 
```csharp
var keyStoreService = new Nethereum.KeyStore.KeyStoreScryptService();
```
Then prepare the required parameters to encrypt our file using `scrypt`
```csharp
var scryptParams = new ScryptParams {Dklen = 32, N = 262144, R = 1, P = 8};
```
The `EthEcKey` function generates an Ethereum compliant privateKey: 

```csharp
var ecKey = Nethereum.Signer.EthECKey.GenerateKey();
```
The last element that we need to generate our file is a password:

```csharp
var password = "testPassword";
```
We can finally encrypt and serialize using our custom scrypt params:

```csharp
var keyStore = keyStoreService.EncryptAndGenerateKeyStore(password, ecKey.GetPrivateKeyAsBytes(), ecKey.GetPublicAddress(), scryptParams);
var json = keyStoreService.SerializeKeyStoreToJson(keyStore);
```

### 2- Decrypting a key

Extracting our private key is achieved using `DecryptKeyStoreFromJson`
```csharp
var key = keyStoreService.DecryptKeyStoreFromJson(password, json);
```

