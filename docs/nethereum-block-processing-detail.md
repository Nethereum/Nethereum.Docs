# Block Processing

## Summary
"Block Procesing" means sequentially crawling the block chain and injecting your own functionality to handle the data you require.  Nethereum looks after the navigation, retrieval, decoding and progress monitoring whilst you can concentrate on your specific needs.  You have the choice of handling all data or a subset.

### What it's good for!
The processing components are primarily designed for longer running processes, where an app, process, thread or service is dedicated to continually processing Blockchain data.  It provides the scaffolding for a dedicated process which allows developers to easily plug in the required handling code.  It's often used to write Blockchain data to a database (see ``` web3.Processing.Blocks.CreateBlockStorageProcessor ```) and Nethereum provides several adaptors for different databases.

 * Auditing
 * Reporting
 * Triggering workflows based on blockchain activity

### What it's NOT for!

Block processing walks each block and each transaction. It's not necessarily the fastest or best way to retrieve data.  There are ways to speed it up but it's not the right fit for every need where there are better alternatives available.

 * Event / Log based monitoring
    * If events are the trigger for your requirements, use [log processing](nethereum-log-processing-detail.md) instead.  It retrieves event logs by sequential block number range. It doesn't request or process each transaction in a block (unless you want it to).  Therefore it's much faster than navigating the whole chain block by block and transaction by transaction.
 * One-off data retrieval
 * Inter-contract calls
    * Currently the processor can't access inter-contract calls (calls made between contracts within a single transaction). There are some Geth specific classes in the "Nethereum.Geth" nuget for debugging transactions and some experimental options to parse the stack trace to retrieve inter-contract calls.

 Nethereum has all you need to retrieve data from the Blockchain.  Processing is simply a layer on top.  If you have one-off retrieval requirements these are easy to use.  To get started, here's the docs: http://docs.nethereum.com/en/latest/getting-started/.

 Also see:
 * ``` web3.Eth.Blocks  ```
 * ``` web3.Eth.Transactions ```
 * ``` web3.Eth.Filters ```

## Too impatient to read further!? Show me the SAMPLES!
There are several varied samples in the Netherum playground: http://playground.nethereum.com/.

## What's a Block Processor?
It is an orchestrator that co-ordinates retrieving blocks, transactions and logs, applying criteria and invoking the code you plug in.  It minimises the boiler plate code you need to write.  It helps you to filter the data you require and can automatically decode it if necessary.  It takes care of progress tracking so you gain "restartability"!   It has some inbuilt retry logic to cope with connectivity errors during log retrieval.

## Creating a Block Processor

## Value Objects (those classes with a VO suffix!)

As the Blockchain is crawled, data is requested in chunks.  Some of the DTO objects retrieved from the chain do not contain all of the properties for the parent object or a related object. 

Value Objects are containers for related data to save you from having to track or retrieve it separately. For instance a Transaction does not contain all of properties from the Block and it does not contain the TransactionReceipt.  The ``` TransactionReceiptVO ``` used by processing includes the Block, Transaction and TransactionReceipt.

### Steps
Crawling is split into "Steps".  For each Step you can set your criteria and handlers.  Without any criteria the processor will crawl everything.

Each step is associated with a value object containing the data for the step.

The Step criteria dictates whether or not any of the handlers for the step are invoked.  

Each handler can have it's own criteria which is processed if the step criteria is matched.  For instance you might want to process all transactions from a specific address (this is step criteria) but require special handling when the transaction meets certain conditions (this is handler specific criteria).

Steps (in crawl order):
* BlockStep (returns BlockWithTransactions);
* TransactionStep (returns TransactionVO);
* TransactionReceiptStep (returns TransactionReceiptVO);
* ContractCreationStep (returns ContractCreationVO);
* FilterLogStep (returns FilterLogVO);

### Handler Actions (sync and async)
The processor allows you to plug in actions which can be synchronous or async.  This is where you put the code to handle the matching data. Async actions are ideal for writing to async API's which are common when integrating with external systems and persistence stores. Synchronous actions are great for performance when you don't need async calls.

### Handler Criteria (sync and async)
You can implement criteria which can be synchronous or async.  Criteria dictates whether or not your action is invoked. Async criteria allows you to do dynamic lookups which may involve external calls to registries/databases/web services etc.  For instance, whilst processing you may need to check dynamic registries as part of your criteria and naturally these calls tend to be async.  Synchronous criteria allows you to inject in-memory criteria easily.

#### Speed Tip! (Place your Criteria carefully)
Each step occurs in order and is dependant on the previous step.  The earlier you can place criteria, the faster the processor will be because you prevent retrieving or crawling irrelevant data in subsequent steps.  

For instance, if you can filter transactions without requiring the receipt information then apply the criteria in the TransactionStep.   This prevents the processor from making a call to retrieve the receipts for irrelevant transactions.

## Block Processing Example
The example below crawls a specific block range and injects handlers which put the data into in-memory lists. There is no criteria so everything is processed.

You'll need the core Nethereum nuget: **Nethereum.Web3**

``` csharp
using Nethereum.BlockchainProcessing.Processor;
using Nethereum.RPC.Eth.DTOs;
using Nethereum.Web3;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;

public class BlockProcessing_StartHere
{
    /// <summary>
    /// Crawl the chain for a block range and injest the data
    /// </summary>
    public static async Task Main(string[] args)
    {
        var blocks = new List<BlockWithTransactions>();
        var transactions = new List<TransactionReceiptVO>();
        var contractCreations = new List<ContractCreationVO>();
        var filterLogs = new List<FilterLogVO>();

        var web3 = new Web3("https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c");

        //create our processor
        var processor = web3.Processing.Blocks.CreateBlockProcessor(steps =>
        {
            // inject handler for each step
            steps.BlockStep.AddSynchronousProcessorHandler(b => blocks.Add(b));
            steps.TransactionReceiptStep.AddSynchronousProcessorHandler(tx => transactions.Add(tx));
            steps.ContractCreationStep.AddSynchronousProcessorHandler(cc => contractCreations.Add(cc));
            steps.FilterLogStep.AddSynchronousProcessorHandler(l => filterLogs.Add(l));
        });

        //if we need to stop the processor mid execution - call cancel on the token
        var cancellationToken = new CancellationToken();

        //crawl the required block range
        await processor.ExecuteAsync(
            toBlockNumber: new BigInteger(2830145),
            cancellationToken: cancellationToken,
            startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

        Console.WriteLine($"Blocks.  Expected: 2, Found: {blocks.Count}");
        Console.WriteLine($"Transactions.  Expected: 25, Found: {transactions.Count}");
        Console.WriteLine($"Contract Creations.  Expected: 5, Found: {contractCreations.Count}");

        Log(transactions, contractCreations, filterLogs);
    }

    private static void Log(
        List<TransactionReceiptVO> transactions, 
        List<ContractCreationVO> contractCreations, 
        List<FilterLogVO> filterLogs)
    {
        Console.WriteLine("Sent From");
        foreach (var fromAddressGrouping in transactions.GroupBy(t => t.Transaction.From).OrderByDescending(g => g.Count()))
        {
            var logs = filterLogs.Where(l => fromAddressGrouping.Any((a) => l.Transaction.TransactionHash == a.TransactionHash));

            Console.WriteLine($"From: {fromAddressGrouping.Key}, Tx Count: {fromAddressGrouping.Count()}, Logs: {logs.Count()}");
        }

        Console.WriteLine("Sent To");
        foreach (var toAddress in transactions
            .Where(t => !t.Transaction.IsToAnEmptyAddress())
            .GroupBy(t => t.Transaction.To)
            .OrderByDescending(g => g.Count()))
        {
            var logs = filterLogs.Where(l => toAddress.Any((a) => l.Transaction.TransactionHash == a.TransactionHash));

            Console.WriteLine($"To: {toAddress.Key}, Tx Count: {toAddress.Count()}, Logs: {logs.Count()}");
        }

        Console.WriteLine("Contracts Created");
        foreach (var contractCreated in contractCreations)
        {
            var tx = transactions.Count(t => t.Transaction.IsTo(contractCreated.ContractAddress));
            var logs = filterLogs.Count(l => transactions.Any(t => l.Transaction.TransactionHash == t.TransactionHash));

            Console.WriteLine($"From: {contractCreated.ContractAddress}, Tx Count: {tx}, Logs: {logs}");
        }
    }
}
```

## Block Storage Processing Example
The example below uses an in-memory repository to store block chain data.  The in-memory repository is really only for demo and testing purposes.  There are several Nethereum adapters for different storage implementations but the setup is common.

Nethereum Block Storage Adapters (nugets)
* Nethereum.BlockchainStore.AzureTables
* Nethereum.BlockchainStore.Csv
* Nethereum.BlockchainStore.EF.Sqlite
* Nethereum.BlockchainStore.EFCore.Sqlite 
* Nethereum.BlockchainStore.EF.SqlServer
* Nethereum.BlockchainStore.EFCore.SqlServer
* Nethereum.BlockchainStore.CosmosCore
* Nethereum.BlockchainStore.MongoDb
* Nethereum.BlockchainStore.EF.Hana

``` csharp
using Nethereum.BlockchainProcessing.BlockStorage.Repositories;
using Nethereum.RPC.Eth.DTOs;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;
using Xunit;
using Xunit.Abstractions;
```

``` csharp
public async Task BlockStorageWithoutCriteria()
{
    var web3 = new Web3.Web3("https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c");

    //create an in-memory context and repository factory 
    var context = new InMemoryBlockchainStorageRepositoryContext();
    var repoFactory = new InMemoryBlockchainStoreRepositoryFactory(context);

    //create our processor
    var processor = web3.Processing.Blocks.CreateBlockStorageProcessor(repoFactory);

    //if we need to stop the processor mid execution - call cancel on the token
    var cancellationToken = new CancellationToken();

    //crawl the required block range
    await processor.ExecuteAsync(
        toBlockNumber: new BigInteger(2830145),
        cancellationToken: cancellationToken,
        startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

    Assert.Equal(2, context.Blocks.Count);
    Assert.Equal(25, context.Transactions.Count);
    Assert.Equal(5, context.Contracts.Count);
    Assert.Equal(55, context.AddressTransactions.Count);
    Assert.Equal(28, context.TransactionLogs.Count);
}

[Fact]
public async Task BlockStorageWithCriteria()
{
    var web3 = new Web3.Web3("https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c");

    //create an in-memory context and repository factory 
    var context = new InMemoryBlockchainStorageRepositoryContext();
    var repoFactory = new InMemoryBlockchainStoreRepositoryFactory(context);

    //create our processor - we're only interested in tx from a specific address
    var processor = web3.Processing.Blocks.CreateBlockStorageProcessor(repoFactory, configureSteps: steps => {
        steps.TransactionStep.SetMatchCriteria(t => t.Transaction.IsFrom("0x1cbff6551b8713296b0604705b1a3b76d238ae14"));
    });

    //if we need to stop the processor mid execution - call cancel on the token
    var cancellationToken = new CancellationToken();

    //crawl the required block range
    await processor.ExecuteAsync(
        toBlockNumber: new BigInteger(2830145),
        cancellationToken: cancellationToken,
        startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

    Assert.Equal(2, context.Blocks.Count);
    Assert.Equal(2, context.Transactions.Count);
    Assert.Equal(4, context.TransactionLogs.Count);
}
```



