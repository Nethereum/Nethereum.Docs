# Signing Messages

Sending transactions as messages allows for better interoperability, the following shows how to sign them. 

### Offline message signing

First, let's load our account in a Web3 object:

```csharp
            var account = new Account("0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7");
            var web3 = new Web3.Web3(account);

```
Then, let's define a simple transfer interface:
```csharp
        public class TransferFunction : FunctionMessage
        {
            [Parameter("address", "_to", 1)]
            public string To { get; set; }

            [Parameter("uint256", "_value", 2)]
            public int TokenAmount { get; set; }
        }
```

Then, define a message: in this case, a simple token transfer:

```csharp 
            var transfer = new TransferFunction()
            {
                To = "0x12890d2cce102216644c59daE5baed380d84830c",
                TokenAmount = 10,
                Nonce = 1, //we set the nonce so it does not get the latest
                Gas = 100, //we set the gas so it does not try to estimate it
                GasPrice=100 // we set the gas price so it does not retrieve the latest averate
            };
```
            
Finally, the signature itself:

```csharp
            var signedMessage = await web3.Eth.GetContractHandler("0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe")
                .SignTransactionAsync(transfer);

```

