# A .NET Developer’s Workflow for Creating and Calling Ethereum Smart Contracts

## Prerequisites

* [Visual Studio Code (windows/Linux or Mac)](https://code.visualstudio.com/) 
* [Solidity vscode extension](https://marketplace.visualstudio.com/items?itemName=JuanBlanco.solidity)
* [Visual Studio](https://visualstudio.microsoft.com/)
* Solidity smart contract called [SimpleStorage.sol](https://solidity.readthedocs.io/en/v0.5.7/introduction-to-smart-contracts.html#storage-example)

There are 
[many great tools](https://github.com/ConsenSys/ethereum-developer-tools-list#developer-tools)
 available to create Ethereum Smart Contracts. It can be hard to choose between them. Here you will learn a simple workflow for developing Solidity smart contracts and calling their functions from C#. This workflow is well suited to .NET developers because it minimises the amount of new tools you need to know about. By using the excellent [Nethereum .NET](https://nethereum.com) library you can continue to use the Visual Studio set of tools you are already familiar with.

Imagine your goal is to take the contract called 
[SimpleStorage.sol](https://solidity.readthedocs.io/en/v0.5.7/introduction-to-smart-contracts.html#storage-example)
 from the Solidity documentation and call its functions from a C# project. Your preference is to use Visual Studio where possible. This workflow is suited to situations where smart contracts are changing often (perhaps because you are developing them and the C# at the same time). When smart contracts are changing less often (perhaps because smart contracts are developed by another team) you may prefer [an alternative workflow using VSCode to generate the C# code](https://docs.nethereum.com/en/latest/nethereum-codegen-vscodesolidity/). The alternative workflow allows you to explicitly control when regeneration happens. Both workflows use the same Nethereum code generation.

## Workflow Overview
There are many possible workflows to achieve your goal, and as new versions of tools and plugins are released other options will appear. At the time of writing this workflow was found to be simple and quick:

![Workflow Overview](screenshots/wf_overview.png)

The diagram above shows these steps:

 * Write Solidity smart contracts and compile them in Visual Studio Code. The output of the compilation process are some files representing the ABI and bytecode for the contracts.

 * Use the Nethereum Autogen code generator to automatically build C# API classes that provide access to the smart contracts.

 * Use Visual Studio to write C# to call methods in the generated C# API classes.
In this article the term 
`function`
 refers to a Solidity function and 
`method`
 refers to a C# method.

## Initial Setup

### Create Project
In a command prompt, you will create a new .NET core console project that you’ll use to hold all your files:

```
dotnet new sln --name DevWorkflowExample
dotnet new console --name SimpleStorage
dotnet sln add .\SimpleStorage\SimpleStorage.csproj
cd SimpleStorage
dotnet add package Nethereum.Web3
dotnet add package Nethereum.Autogen.ContractApi
```



### Prepare Visual Studio Code



 1. Open Visual Studio Code.

 2. Open extensions and install the [Solidity extension here](https://marketplace.visualstudio.com/items?itemName=JuanBlanco.solidity) .

 3. Open the SimpleStorage folder we just created. You should see something like this:

![VSCode Tree](screenshots/vscode_tree.png)

4. If at any time, VS Code asks “Required assets to build and debug are missing from ‘SimpleStorage’. Add them?” say yes.
5. Create a new file (ctrl+N).
6. Paste the following solidity code into the file:

```
pragma solidity >=0.4.0 <0.7.0;

contract SimpleStorage {
    uint storedData;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}
```


7. Save the file as 
`SimpleStorage.sol`
 in the root of the SimpleStorage folder.
The contract is from the 
[Solidity documentation](https://solidity.readthedocs.io/en/v0.5.7/introduction-to-smart-contracts.html#storage-example)
 and you can see it is a very simple contract, just 
`set()`
 and 
`get()`
 functions. Now you are ready to begin the main developer workflow. The steps below correspond to the numbers on the diagram above.

## Main Developer Workflow

### Step 1 — Compile Smart Contract in Visual Studio Code
In Visual Studio Code, press Shift-Ctrl-P and choose “Solidity: Compile Current Solidity Contract” or press F5. You should see some new files appearing in the 
`SimpleStorage\bin`
 folder, most importantly 
`SimpleStorage.abi`
 and 
`SimpleStorage.bin`
 .

### Step 2 — Rebuild the C# Project in Visual Studio
Open the solution 
`DevWorkflowExample.sln`
 in Visual Studio (not Visual Studio Code).
Right-click on the SimpleStorage project and choose “Rebuild”. The act of rebuilding the project triggers the 
`Nethereum.Autogen.ContractApi`
 package to build the C# API classes to let you interact with the 
`SimpleStorage.sol`
 contract. You should see a collection of new files added to the project in a folder called 
`SimpleStorage`
 like this:

![VS Tree](screenshots/vs_tree.png)

The generated 
`SimpleStorageService`
 class contains some useful methods:

![Method Table](screenshots/method_table.png)

Notice the C# method naming is different for the 
`set()`
 and 
`get()`
 function calls. This is because 
`set()`
 changes a value on the blockchain, so it costs Ether, so it has be called using an Ethereum transaction, and will return a receipt. The 
`get()`
 function doesn't change any values on the blockchain, so it is a simple call and is free (no transaction and no receipt).

### Step 3 — Call Smart Contract functions from C# in Visual Studio
Now you can call functions from your smart contract in the .NET core console program, by making calls to the generated C# classes mentioned in the previous section. For example, paste the code below into `Program.cs`, replacing everything that is currently there.

```csharp
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using SimpleStorage.SimpleStorage.CQS;
using SimpleStorage.SimpleStorage.Service;
using System;
using System.Threading.Tasks;

namespace SimpleStorage
{
    class Program
    {
        static void Main(string[] args)
        {
            Demo().Wait();
        }

        static async Task Demo()
        {
            try
            {
                // Setup
                // Here we're using local chain eg Geth https://github.com/Nethereum/TestChains#geth
                var url = "http://localhost:8545";
                var privateKey = "0xb5b1870957d373ef0eeffecc6e4812c0fd08f554b37b233526acc331bf1544f7";
                var account = new Account(privateKey);
                var web3 = new Web3(account, url);

                Console.WriteLine("Deploying...");
                var deployment = new SimpleStorageDeployment();
                var receipt = await SimpleStorageService.DeployContractAndWaitForReceiptAsync(web3, deployment);
                var service = new SimpleStorageService(web3, receipt.ContractAddress);
                Console.WriteLine($"Contract Deployment Tx Status: {receipt.Status.Value}");
                Console.WriteLine($"Contract Address: {service.ContractHandler.ContractAddress}");
                Console.WriteLine("");

                Console.WriteLine("Sending a transaction to the function set()...");
                var receiptForSetFunctionCall = await service.SetRequestAndWaitForReceiptAsync(
                    new SetFunction() { X = 42, Gas = 400000 });
                Console.WriteLine($"Finished storing an int: Tx Hash: {receiptForSetFunctionCall.TransactionHash}");
                Console.WriteLine($"Finished storing an int: Tx Status: {receiptForSetFunctionCall.Status.Value}");
                Console.WriteLine("");

                Console.WriteLine("Calling the function get()...");
                var intValueFromGetFunctionCall = await service.GetQueryAsync();
                Console.WriteLine($"Int value: {intValueFromGetFunctionCall} (expecting value 42)");
                Console.WriteLine("");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }

            Console.WriteLine("Finished");
            Console.ReadLine();
        }
    }
}

```


Build the project.
The workflow is done! You can now make further edits to the smart contract in Visual Studio Code, compile it there, and simply rebuild the project in Visual Studio to be able to make C# calls to the amended Solidity functions.

## Program Execution
Of course, you’d like to check that the program runs successfully. For the project to run, it needs to speak to a blockchain and here you do need a new tool. A good option during development is to run a local blockchain as described here: 
[https://github.com/Nethereum/TestChains#geth](https://github.com/Nethereum/TestChains#geth)
 .
With a local blockchain running, run the 
`SimpleStorage`
 console project from Visual Studio. You should get output like below:

```
Contract Deployment Tx Status: 1
Contract Address: 0x243e72b69141f6af525a9a5fd939668ee9f2b354

Sending a transaction to the function set()...
Finished storing an int: Tx Hash: 0xe4c8e72bf18c391c3dd0d18aa4c2ec4672591b974383f7d02120657d766d1bf3
Finished storing an int: Tx Status: 1

Calling the function get()...
Int value: 42 (expecting value 42)

Finished
```



## Where to go from here
The next step in your development process would probably be to add some tests for your Solidity contract. Does this mean you absolutely have to go off and learn Truffle or some other tooling? The answer is no, you don’t. There is an 
[example here](https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Contracts.IntegrationTests)
 of using XUnit test fixtures to launch a local chain before running tests to deploy contracts and call functions.
Note, you don’t have to use the generated 
`SimpleStorageService`
 class to call your smart contract's functions. At the very least, though, it is instructive to see how the calls work in the generated code.

## Alternative Workflow with VSCode
As mentioned, the workflow detailed above is useful when the smart contracts are changing often and you want the C# classes to reflect these changes often. This suitsthe case where you are developing smart contracts and the C# at the same time.
In cases where the smart contracts are stable (e.g. you have been sent ABI and bytecode by another development team) you may prefer to explicitly control when regeneration happens. This can be done by using [VSCode not just to write the smart contracts but also to generate the necessary C# code](https://docs.nethereum.com/en/latest/nethereum-codegen-vscodesolidity/).
