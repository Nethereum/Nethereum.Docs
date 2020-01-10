# Multiple output parameters and function DTOs

There are many scenarios where a function might return multiple outputs, structured using structs and mappings, or simply by having multiple outputs.
The simplest way to decode all this data is by using Function DTOs similarly to Event DTOs explained previously.

## Video guide

This video provides an introduction on how to store and retrieve data from structs, mappings and arrays decoding multiple output parameters to Data Transfer Objects.

[![Mappings, Structs, Arrays and complex Functions Output (DTOs)](http://img.youtube.com/vi/o8UC96K0rg8/0.jpg)](https://www.youtube.com/watch?v=o8UC96K0rg8 "Mappings, Structs, Arrays and complex Functions Output (DTOs)")

## The test contract

The following contract returns multiple values, the amount and the currency as a string:

```javascript
contract MultipleBalanceReturn {

    function GetBalance(address owner) public returns (int amount, string memory currency) {
       return (10, "DAI");
    }
}
```

## Retrieving the output using a DTO

### The ABI for the mapping

If we inspect the ABI and find "documents" we can see that it is a function and has multiple outputs: `amount` and `currency`. The outputs match the parameter outputs of our function.
    
```json
[
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "name": "GetBalance",
    "outputs": [
      {
        "internalType": "int256",
        "name": "amount",
        "type": "int256"
      },
      {
        "internalType": "string",
        "name": "currency",
        "type": "string"
      }
    ],
    "payable": false,
    "stateMutABIlity": "nonpayable",
    "type": "function"
  }
]

```
### The function DTO

To create a function output DTO we start by decorating a class with the [FunctionOutput] attribute and the interface IFunctionDTO

```csharp
 [FunctionOutput]
public class GetBalanceOutputDTO: IFunctionOutputDTO 
{
    [Parameter("int256", "amount", 1)]
    public virtual BigInteger Amount { get; set; }
    [Parameter("string", "currency", 2)]
    public virtual string Currency { get; set; }
}
```

The next step is to "map" each of the properties to the function parameters. The property needs to be decorated with the Parameter attribute, providing the type, name and parameter order.
When retrieving the data each parameter will be decoded based on the type defined.

### Accessing the data
Given that we have already deployed the contract, we can call it as follows:

```csharp
   var balanceFunction = contract.GetFunction("GetBalance");
   var balance = await balanceFunction.CallDeserializingToObjectAsync<GetBalanceOutputDTO>(account.Address);

   Console.WriteLine(balance.Amount);
   Console.WriteLine(balance.Currency);
```

### The final code


```csharp
using Nethereum.Web3;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts.CQS;
using Nethereum.Util;
using Nethereum.Web3.Accounts;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.Contracts;
using Nethereum.Contracts.Extensions;
using Nethereum.RPC.Eth.DTOs;
using System;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;

public class GetStartedSmartContracts
{

        //This sample demonstrates how to interact with a smart contract function that returns multiple parameters 

        // Given a solidity smart contract:
        /******************
        
        contract MultipleBalanceReturn {

                function GetBalance(address owner) public returns (int amount, string memory currency) {
                    return (10, "DAI");
                }
        }
        
        **************/

        //We can define an ouput DTO, including the Amount and Currency multiple parameters in the output:

         [FunctionOutput]
         public class GetBalanceOutputDTO: IFunctionOutputDTO 
         {
            [Parameter("int256", "amount", 1)]
            public virtual BigInteger Amount { get; set; }
            [Parameter("string", "currency", 2)]
            public virtual string Currency { get; set; }
         } 



    public static async Task Main()
    {

#region Web3 and Deployment region
        // Instantiating Web3 and the Account
        // To create an instance of web3 we first provide the url of our testchain and the private key of our account. 
        // Here we are using http://testchain.nethereum.com:8545 which is our simple single node Nethereum testchain.
        // When providing an Account instantiated with a  private key, all our transactions will be signed by Nethereum.

        var url = "http://testchain.nethereum.com:8545";
        var privateKey = "0x7580e7fb49df1c861f0050fae31c2224c6aba908e116b8da44ee8cd927b990b0";
        var account = new Account(privateKey);
        var web3 = new Web3(account, url);

        //This is the contract bytecode and ABI after compiling our contract
        var contractByteCode =
            "608060405234801561001057600080fd5b50610121806100206000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c806343e2e50414602d575b600080fd5b605060048036036020811015604157600080fd5b50356001600160a01b031660cc565b6040518083815260200180602001828103825283818151815260200191508051906020019080838360005b838110156091578181015183820152602001607b565b50505050905090810190601f16801560bd5780820380516001836020036101000a031916815260200191505b50935050505060405180910390f35b5060408051808201909152600381526244414960e81b6020820152600a9156fea265627a7a72315820d57fb3347ed5d978951aa39de3588c454023e7a3293ce8cee405447b1998fe7364736f6c634300050d0032";
        var ABI =
            @"[{""constant"":false,""inputs"":[{""internalType"":""address"",""name"":""owner"",""type"":""address""}],""name"":""GetBalance"",""outputs"":[{""internalType"":""int256"",""name"":""amount"",""type"":""int256""},{""internalType"":""string"",""name"":""currency"",""type"":""string""}],""payable"":false,""stateMutABIlity"":""nonpayable"",""type"":""function""}]";


        //Deploying the smart contract:

        var senderAddress = account.Address;
        //estimating the gas
        var estimatedGas = await web3.Eth.DeployContract.EstimateGasAsync(ABI, contractByteCode, senderAddress);
        // deploying the contract
        var receipt = await web3.Eth.DeployContract.SendRequestAndWaitForReceiptAsync(ABI,
            contractByteCode, senderAddress, estimatedGas);
        Console.WriteLine("Contract deployed at address: " + receipt.ContractAddress);

#endregion

      //Using our contract address we can interact with the contract as follows:
      var contract = web3.Eth.GetContract(ABI, receipt.ContractAddress);

      var balanceFunction = contract.GetFunction("GetBalance");
      var balance = await balanceFunction.CallDeserializingToObjectAsync<GetBalanceOutputDTO>(account.Address);

       Console.WriteLine(balance.Amount);
       Console.WriteLine(balance.Currency);
    }
}
```

