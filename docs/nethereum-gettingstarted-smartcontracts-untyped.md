# Quick introduction to smart contracts integration with Nethereum

The purpose of this sample is the following:

* Creating an account using a private key

* Deploying a smart contract (the sample provided is the standard ERC20 token contract)

* Estimating the gas cost of a contract transaction

* Sending a transaction to the smart contract (in this scenario transfering balance)

* Making a call to a smart contract (in this scenario get the balance of an account)
        
!!! note
    The following article uses lines of code, you have the possibility to run similar code directly in your browser by using Nethereum's playground at the following link:
    [Smart Contracts: (Untyped) Deployment, Calls(Querying), Transactions](http://playground.nethereum.com/csharp/id/1045)

## Prerequisites:
        
First off we will add the using statement:        

```csharp
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts.CQS;
using Nethereum.Util;
using Nethereum.Hex.HexConvertors.Extensions;
using Nethereum.Contracts;
using Nethereum.Contracts.Extensions;
using Nethereum.RPC.Eth.DTOs;
```
### Instantiating Web3 and the Account
    
To create an instance of web3 we first provide the url of our testchain and the private key of our account. 
Here we are using http://testchain.nethereum.com:8545 which is our simple single node Nethereum testchain.
When providing an Account instantiated with a  private key, all our transactions will be signed by Nethereum.

```csharp
        var url = "http://testchain.nethereum.com:8545";
        var privateKey = "0x7580e7fb49df1c861f0050fae31c2224c6aba908e116b8da44ee8cd927b990b0";
        var account = new Account(privateKey);
        var web3 = new Web3(account, url);
```

This is the contract bytecode (compile executable) and Abi

```csharp
        var contractByteCode =
            "0x60606040526040516020806106f5833981016040528080519060200190919050505b80600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005081905550806000600050819055505b506106868061006f6000396000f360606040523615610074576000357c010000000000000000000000000000000000000000000000000000000090048063095ea7b31461008157806318160ddd146100b657806323b872dd146100d957806370a0823114610117578063a9059cbb14610143578063dd62ed3e1461017857610074565b61007f5b610002565b565b005b6100a060048080359060200190919080359060200190919050506101ad565b6040518082815260200191505060405180910390f35b6100c36004805050610674565b6040518082815260200191505060405180910390f35b6101016004808035906020019091908035906020019091908035906020019091905050610281565b6040518082815260200191505060405180910390f35b61012d600480803590602001909190505061048d565b6040518082815260200191505060405180910390f35b61016260048080359060200190919080359060200190919050506104cb565b6040518082815260200191505060405180910390f35b610197600480803590602001909190803590602001909190505061060b565b6040518082815260200191505060405180910390f35b600081600260005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008573ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905061027b565b92915050565b600081600160005060008673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561031b575081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505410155b80156103275750600082115b1561047c5781600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a381600160005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600260005060008673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060003373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505403925050819055506001905061048656610485565b60009050610486565b5b9392505050565b6000600160005060008373ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000505490506104c6565b919050565b600081600160005060003373ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600050541015801561050c5750600082115b156105fb5781600160005060003373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282825054039250508190555081600160005060008573ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828282505401925050819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905061060556610604565b60009050610605565b5b92915050565b6000600260005060008473ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005060008373ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060005054905061066e565b92915050565b60006000600050549050610683565b9056";
        var abi =
            @"[{""constant"":false,""inputs"":[{""name"":""_spender"",""type"":""address""},{""name"":""_value"",""type"":""uint256""}],""name"":""approve"",""outputs"":[{""name"":""success"",""type"":""bool""}],""type"":""function""},{""constant"":true,""inputs"":[],""name"":""totalSupply"",""outputs"":[{""name"":""supply"",""type"":""uint256""}],""type"":""function""},{""constant"":false,""inputs"":[{""name"":""_from"",""type"":""address""},{""name"":""_to"",""type"":""address""},{""name"":""_value"",""type"":""uint256""}],""name"":""transferFrom"",""outputs"":[{""name"":""success"",""type"":""bool""}],""type"":""function""},{""constant"":true,""inputs"":[{""name"":""_owner"",""type"":""address""}],""name"":""balanceOf"",""outputs"":[{""name"":""balance"",""type"":""uint256""}],""type"":""function""},{""constant"":false,""inputs"":[{""name"":""_to"",""type"":""address""},{""name"":""_value"",""type"":""uint256""}],""name"":""transfer"",""outputs"":[{""name"":""success"",""type"":""bool""}],""type"":""function""},{""constant"":true,""inputs"":[{""name"":""_owner"",""type"":""address""},{""name"":""_spender"",""type"":""address""}],""name"":""allowance"",""outputs"":[{""name"":""remaining"",""type"":""uint256""}],""type"":""function""},{""inputs"":[{""name"":""_initialAmount"",""type"":""uint256""}],""type"":""constructor""},{""anonymous"":false,""inputs"":[{""indexed"":true,""name"":""_from"",""type"":""address""},{""indexed"":true,""name"":""_to"",""type"":""address""},{""indexed"":false,""name"":""_value"",""type"":""uint256""}],""name"":""Transfer"",""type"":""event""},{""anonymous"":false,""inputs"":[{""indexed"":true,""name"":""_owner"",""type"":""address""},{""indexed"":true,""name"":""_spender"",""type"":""address""},{""indexed"":false,""name"":""_value"",""type"":""uint256""}],""name"":""Approval"",""type"":""event""}]";
```

##### DEPLOYING THE SMART CONTRACT
 
The solidity smart contract constructor for this standard ERC20 smart contract is as follows:

```js
//SOLIDITY: Constructor
function Standard_Token(uint256 _initialAmount) 
{         balances[msg.sender] = _initialAmount;         
         _totalSupply = _initialAmount;     
}
```[Smart Contracts: Query ERC20 Smart contract balance](http://playground.nethereum.com/csharp/id/1005)
This means we need to supply a parameter to a constructor on deployment

```csharp
        var totalSupply = BigInteger.Parse("1000000000000000000");
        var senderAddress = account.Address;
```

When working with untyped smart contract definitions the parameters are passed as part of a params object array, and recognised and mapped using the full json abi:

We first estimate the cost of the deployment transaction, so we can provide the right amount of gas to the deployment transaction. Providing the abi, bytecode and constructor parameters (totalSuppy).

And finally we send the deployment transaction in a similar way, included the estimated gas amount.

```csharp
        var estimateGas = await web3.Eth.DeployContract.EstimateGasAsync(abi, contractByteCode, senderAddress, totalSupply);
        
        var receipt = await web3.Eth.DeployContract.SendRequestAndWaitForReceiptAsync(abi,
            contractByteCode, senderAddress, estimateGas, null, totalSupply);
        Console.WriteLine("Contract deployed at address: " + receipt.ContractAddress);
```

Using our contract address we can interact with the contract by providing the json abi and contract address.

```csharp
        var contract = web3.Eth.GetContract(abi, receipt.ContractAddress);
```

Now the contract object enables us to retrieve functions using their name:

```csharp
        var transferFunction = contract.GetFunction("transfer");
        var balanceFunction = contract.GetFunction("balanceOf");
        var newAddress = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
```
A function, has different methods, the main ones are:

* CallAsync:  where you query the values of a smart contract, but you don't change the blockchain state. For example, GetBalance of an adddress.
* SendTransactionAsync and SendTransactionAndWaitForReceiptAsync : where you commit some changes to the change and creates a transaction on included in the next block. For example Transfer Amount.
* EstimateGasAsync: where the transaction is simulated on chain to calculate the gas amount necessary to send the transaction.


Using a CallAsync we can query the smart contract for values:

This is the solidity function to get balance:

```js
//SOLIDITY: balanceOf address
 function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

```
This is the csharp call: 

```csharp
        var balance = await balanceFunction.CallAsync<int>(newAddress);
        Console.WriteLine($"Account {newAddress} balance: {balance}");
        Console.WriteLine("Transfering 1000 tokens");
        var amountToSend = 1000;
```

Sending transactions will commit the information to the chain, before submission we need to estimate the gas (cost of the transaction)
In a similar way, any parameters required by the function are included at the end of the method in the same order as per the solidity function.

This is a simplified solidity smart contract transfer

```js
function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        return true;
    }
```

Csharp transaction call and estimation

```csharp
        var gas = await transferFunction.EstimateGasAsync(senderAddress, null, null, newAddress, amountToSend);
        var receiptAmountSend =
            await transferFunction.SendTransactionAndWaitForReceiptAsync(senderAddress, gas, null, null, newAddress,
                amountToSend);

        balance = await balanceFunction.CallAsync<int>(newAddress);
        Console.WriteLine($"Account {newAddress} balance: {balance}");
```
