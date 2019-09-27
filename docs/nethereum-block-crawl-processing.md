# Crawling Blockchains with Nethereum Blockchain Processor

Nethereum provides Blockchain processing capabilities in order to facilitate the following operations to and from an Ethereum blockchain: 
- data storage
- search
- event-specific functionalities
- indexation    
more about Nethereum Blockchain processor on https://github.com/Nethereum/Nethereum.BlockchainProcessing

The following demonstrates basic chain crawling functions (Blockchain exploration) enabled by Nethereum: 

Required assemblies:
```csharp
using Nethereum.BlockchainProcessing.Processor;
using Nethereum.RPC.Eth.DTOs;
using Nethereum.Web3;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;
```
The main Blockchain data types we are going to manipulate are:
- Blocks
- Transactions
- Contracts
- Logs

Let's create variables representing each of  these chain datasets: 

```csharp
        var blocks = new List<BlockWithTransactions>();
        var transactions = new List<TransactionReceiptVO>();
        var contractCreations = new List<ContractCreationVO>();
        var filterLogs = new List<FilterLogVO>();
```
We'll use the Rinkeby testchain as data source, let's instantiante a Web3 object with rinkeby's IRL:

```csharp
        var web3 = new Web3("https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c");
```

### 1- Processing Blocks for a Specific Contract:

The Blockchain processor can be parametered to target the data pertaining to a specific contract:
```csharp
const string ContractAddress = ""0x5534c67e69321278f5258f5bebd5a2078093ec19"";
```

```csharp
var processor = web3.Processing.Blocks.CreateBlockProcessor(steps => {

steps.TransactionStep.SetMatchCriteria(t => t.Transaction.IsTo(ContractAddress));
steps.TransactionReceiptStep.AddSynchronousProcessorHandler(tx => transactions.Add(tx));
steps.FilterLogStep.AddSynchronousProcessorHandler(l => filterLogs.Add(l));
        });

        Console.WriteLine($""Transactions. Expected: 2, Actual: {transactions.Count}"");
        Console.WriteLine($""Logs. Expected: 8, Actual: {filterLogs.Count}"");
```
### 2- Processing Blocks for a Specific Function:

It's also possible to target the data pertaining to a specific contract, the below shows the contract's C# interface:
```csharp
    [Function(""buyApprenticeChest"")]
    public class BuyApprenticeFunction : FunctionMessage
    {
        [Parameter(""uint256"", ""_region"", 1)]
        public BigInteger Region { get; set; }
    }
```

The data we will handle are the transactions transactions that occurred with this contract as well as logs:
```csharp
        var transactions = new List<TransactionReceiptVO>();
        var filterLogs = new List<FilterLogVO>();
```
At this point, we can create our processor instance specifying the scope of data we need to retrieve, in this case, anything around our targeted contract. The transactions will have to match the `to` address and function signature.
  
```csharp
        var processor = web3.Processing.Blocks.CreateBlockProcessor(steps => {
                
            steps.TransactionStep.SetMatchCriteria(t => 
                t.Transaction.IsTo(""0xc03cdd393c89d169bd4877d58f0554f320f21037"") && 
                t.Transaction.IsTransactionForFunctionMessage<BuyApprenticeFunction>());

            steps.TransactionReceiptStep.AddSynchronousProcessorHandler(tx => transactions.Add(tx));
            steps.FilterLogStep.AddSynchronousProcessorHandler(l => filterLogs.Add(l));
        });

        Console.WriteLine($""Transactions. Expected: 1, Actual: {transactions.Count}"");
        Console.WriteLine($""Logs. Expected: 1, Actual: {filterLogs.Count}"");
```

### 3- Processing Transactions Matching Specific Criteria:
Here is another example of block crawling with a delimited scope: we will only retrive transactions that came from account address `0x1cbff6551b8713296b0604705b1a3b76d238ae14`:
```csharp
var transactions = new List<TransactionReceiptVO>();
var filterLogs = new List<FilterLogVO>();
```

We can create our processor specifying the type of transaction we're interested in handling.
```csharp
var processor = web3.Processing.Blocks.CreateBlockProcessor(steps => {
            steps.TransactionStep.SetMatchCriteria(t => t.Transaction.IsFrom(""0x1cbff6551b8713296b0604705b1a3b76d238ae14""));
            steps.TransactionReceiptStep.AddSynchronousProcessorHandler(tx => transactions.Add(tx));
            steps.FilterLogStep.AddSynchronousProcessorHandler(l => filterLogs.Add(l));
        });
```

```csharp
Console.WriteLine($""Transactions. Expected: 2, Actual: {transactions.Count}"");
Console.WriteLine($""Logs. Expected: 4, Actual: {filterLogs.Count}"");
```

### 4- Cancelling Processing:

If we need to stop the processor mid execution we can call cancel on the token:
```csharp
var cancellationToken = new CancellationToken();
```
In the following sample, we'll crawl the required block range, which is exactly one block:
```csharp
    await processor.ExecuteAsync(
        toBlockNumber: new BigInteger(2830145),
        cancellationToken: cancellationToken,
        startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

    Console.WriteLine($""Expected 65 logs. Logs found: {logs.Count}."");
```
