# Block and Block Storage Processing

## Summary
"Block Processing" involves sequentially crawling the Blockchain and injecting your own functionality to handle the data. Nethereum looks after the navigation, retrieval, decoding and progress monitoring whilst you can concentrate on your specific needs. You have the choice of handling all of the data or a subset.

### What it's good for!
The processing components are primarily designed for longer running processes, where an app, process, thread or service is dedicated to continually processing Blockchain data. It provides the scaffolding for a dedicated process which allows developers to easily plug in the required handling code. It's often used to write Blockchain data to a database (see ``` web3.Processing.Blocks.CreateBlockStorageProcessor ```) and Nethereum provides several adaptors for different databases.

 * Auditing
 * Reporting
 * Triggering workflows based on blockchain activity

### What it's NOT for!

Block processing walks each block and each transaction. It's not necessarily the fastest or best way to retrieve data. There are ways to speed it up but it's not the right fit for every need where there are better alternatives available.

 * Event / Log based monitoring
    * If events are the trigger for your requirements there are other preferable options:
        1. [log processing](nethereum-log-processing-detail.md).  It retrieves event logs by sequential block number range. It doesn't request or process each transaction in a block (unless you want it to).  Therefore it's much faster than navigating the whole chain block by block and transaction by transaction.
        2. Web Socket Streaming.  Real time event log retrieval. Example: https://github.com/Nethereum/Nethereum/blob/master/src/Nethereum.WebSocketsStreamingTest/Program.cs
 * One-off data retrieval
 * Inter-contract calls
  * Currently the processor can't access inter-contract calls (calls made between contracts within a single transaction). There are some Geth specific classes in the "Nethereum.Geth" nuget for debugging transactions and some experimental options to parse the stack trace to retrieve inter-contract calls.

 Nethereum has all you need to retrieve data from the Blockchain. Processing is simply a layer on top. If you have one-off retrieval requirements these are easy to use. To get started, here's the docs: http://docs.nethereum.com/en/latest/getting-started/.

 Also see:
 * ``` web3.Eth.Blocks ```
 * ``` web3.Eth.Transactions ```
 * ``` web3.Eth.Filters ```

 There are several easy to use methods to retrieve Blockchain data.

### Block Processing vs Block Storage Processing
Both crawl the Blockchain in the same order and both allow criteria to dictate what is processed.

* Block Processing 
  * e.g ``` web3.Processing.Blocks.CreateBlockProcessor ```
  * Crawls the Blockchain and provides value objects for you to filter and handle completely as you wish. 
* Block Storage Processing 
  * e.g. ``` web3.Processing.Blocks.CreateBlockStorageProcessor ``` 
  * Crawls the Blockchain and stores the data in a persistent store. It also allows criteria to dictate what is stored. Nethereum provides ready made adapters, entities and mapping for this and it is relatively easy to write your own adapter.

#### Nethereum Block Storage Adapters (nugets)
* Nethereum.BlockchainStore.AzureTables
* Nethereum.BlockchainStore.Csv
* Nethereum.BlockchainStore.EF.Sqlite
* Nethereum.BlockchainStore.EFCore.Sqlite 
* Nethereum.BlockchainStore.EF.SqlServer
* Nethereum.BlockchainStore.EFCore.SqlServer
* Nethereum.BlockchainStore.CosmosCore
* Nethereum.BlockchainStore.MongoDb
* Nethereum.BlockchainStore.EF.Hana

The source code for these adapters can be found in the repo below:

Blockchain Storage Repo: https://github.com/Nethereum/Nethereum.BlockchainStorage

## Too impatient to read further!? Show me the SAMPLES!
There are several varied samples in the Netherum playground:
Block Crawl Processing: Process block and cancel	http://playground.nethereum.com/csharp/id/1022
Block Crawl Processing: Process blocks for a specific contract	http://playground.nethereum.com/csharp/id/1023
Block Crawl Processing: Process blocks for a specific function	http://playground.nethereum.com/csharp/id/1024
Block Crawl Processing: Full sample	http://playground.nethereum.com/csharp/id/1025
Block Crawl Processing: With Block Progress Repository	http://playground.nethereum.com/csharp/id/1026
Block Crawl Processing: Transaction criteria	http://playground.nethereum.com/csharp/id/1027
  
## What's a Block Processor?

It is an orchestrator that co-ordinates crawling the Blockchain, applying criteria and invoking the code you plug in. It minimises the boiler plate code you need to write to navigate and retrieve the data.  It takes care of progress tracking so you gain "restartability"!  It has some inbuilt retry logic to cope with connectivity errors during log retrieval.

### Value Objects (those classes with a VO suffix!)

As the Blockchain is crawled, data is requested from the node via RPC calls. Some of the DTO objects retrieved from the chain do not contain all of the properties for the parent object or a related object. 

Value Objects are aggregate objects for related data to save you from having to track, retrieve or aggregate. For instance the Transaction DTO object does not contain all of properties from the Block and it does not contain the TransactionReceipt. The ``` TransactionReceiptVO ``` used by processing includes the Block, Transaction and TransactionReceipt.

### Steps
Crawling is split into "Steps". For each Step you can set your criteria and handlers. Without any criteria the processor will crawl everything.

Each step is associated with a value object containing the data for the step.

The Step criteria dictates whether or not any of the handlers for the step are invoked. 

Each handler can have it's own criteria which is evaluated only if the step criteria is matched. For instance you might want to process all transactions from a specific address (step criteria) but require special handling when the transaction meets certain conditions (handler specific criteria).

Steps (in crawl order):
* BlockStep (returns BlockWithTransactions);
* TransactionStep (returns TransactionVO);
* TransactionReceiptStep (returns TransactionReceiptVO);
* ContractCreationStep (returns ContractCreationVO);
* FilterLogStep (returns FilterLogVO);

### Handler Criteria (sync and async)
Criteria can be synchronous or async. Criteria dictates whether or not an action is invoked. Async criteria allows you to do dynamic lookups which may involve external calls to registries/databases/web services etc. For instance, whilst processing you may need to check dynamic registries as part of your criteria and naturally these calls tend to be async. Synchronous criteria allows you to inject in-memory criteria easily.

### Handler Actions (sync and async)
Handler actions can be synchronous or async. This is where you put the code to handle the matching data. Async actions are ideal for writing to async API's which are common when integrating with external systems and persistence stores. Synchronous actions are great for performance when you don't need async calls.

#### Speed Tip (Place your Criteria carefully!)
Each step occurs in order and is dependent on the previous step. The earlier you can place criteria, the faster the processor will be because it will prevent retrieving or crawling irrelevant data. 

For instance, if you can filter transactions in the "TransactionStep" instead of the "TransactionReceiptStep" it prevents the processor from making a call to retrieve the receipts for irrelevant transactions.

## Optional Parameters

* minimumBlockConfirmations
  * This ensures blocks are only processed once the required number of confirmations is met. This helps to protect against processing data affected by block reorganisation. The default is 12. 
* log
  * An instance of ILog to provide extra logging of processing activity. The default is null.
* blockProgressRepository (vital for restartability!)
  * Storage of the last block number processed. (see below!). The default is an In-Memory repository for Block processing. For Block Storage Processing, if the repository factory supports block progress it will use that, else it will fallback to an in-memory implementation.

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

    Console.WriteLine($"Blocks. Expected: 2, Found: {blocks.Count}");
    Console.WriteLine($"Transactions. Expected: 25, Found: {transactions.Count}");
    Console.WriteLine($"Contract Creations. Expected: 5, Found: {contractCreations.Count}");

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
The example below uses an in-memory repository to store block chain data. The in-memory repository is really only for demo and testing purposes. There are several Nethereum adapters for different storage implementations but the setup is common.

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
[Fact]
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

## Block Storage With Azure Storage Tables

Nethereum provides an adaptor for Azure Storage Tables which is really simple to configure and run.  It will create the necessary tables if they don't exist.

It's focus is on writing the data to the storage tables rather than the ability to query them. If you want to run queries you can use the WindowsAzure.Storage nuget to help.

Required Nuget Package: **Nethereum.BlockchainStore.AzureTables**

Required Namespace:
``` csharp
#r using Nethereum.BlockchainStore.AzureTables.Bootstrap;
```

Create a repository factory - this will create the necessary Azure Storage Tables and provide a repository that writes to them. You'll need an Azure connection string. The second argument "samples" is a table prefix. You can use the prefix to separate Blockchain data from different sources or for different purposes using the same Azure storage account.
``` csharp
var repoFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "samples");
```

Create the processor passing in the repository factory. By default block progress will be stored in an azure table.
``` csharp
var processor = _web3.Processing.Blocks.CreateBlockStorageProcessor(repoFactory);
```

Run the processor.
``` csharp
//if we need to stop the processor mid execution - call cancel on the token
var cancellationToken = new CancellationToken();

//crawl the required block range
await processor.ExecuteAsync(
  toBlockNumber: new BigInteger(2830145),
  cancellationToken: cancellationToken,
  startAtBlockNumberIfNotProcessed: new BigInteger(2830144));
```

## Block Progress Repository
Providing a block progress repository is necessary for continual processing, it allows the processor to begin where it left off. A block progress repository provides storage of the last block processed. The ``` IBlockProgressRepository ``` interface is very simple and easy to implement. You can either use one of the Nethereum implementations or create your own. If you don't provide a repository, an in-memory repository is created for each processor.

For Block Storage Processing - each Nethereum provided adapter includes a default Block Progress repository. However if you want to keep block progress persistence separate to the Blockchain data storage you can dictate a specific block progress repository. For instance you might want to keep block progress in a file whilst the Blockchain data goes in a database.

The Nethereum.Web3 nuget provides the following simple implementations:

* Nethereum.BlockchainProcessing.ProgressRepositories.InMemoryBlockchainProgressRepository (default)
* Nethereum.BlockchainProcessing.ProgressRepositories.JsonBlockProgressRepository

Nethereum provides other implementations in the following nuget packages:

* Nethereum.BlockchainStore.AzureTables
* Nethereum.BlockchainStore.Csv
* Nethereum.BlockchainStore.EF.Sqlite
* Nethereum.BlockchainStore.EFCore.Sqlite 
* Nethereum.BlockchainStore.EF.SqlServer
* Nethereum.BlockchainStore.EFCore.SqlServer
* Nethereum.BlockchainStore.CosmosCore
* Nethereum.BlockchainStore.MongoDb
* Nethereum.BlockchainStore.EF.Hana

### Block Repository using Azure Table Storage

This demonstrates usage of the block progress repository provided for Azure Tables by Nethereum. This stores the last block number processed in an Azure storage table.

**Requires Nuget package: Nethereum.BlockchainStore.AzureTables**

Namespace
``` csharp
#r using Nethereum.BlockchainStore.AzureTables.Bootstrap;
```

Create an azure tables repository factory. You'll need to pass your azure connection string. You can also provide a table prefix (in the example we're using "samples") which means any table created in Azure by the factory is prefixed. The prefix allows the same azure storage account to be used for multiple processors. 
``` csharp
var azureTablesRepositoryFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "samples");
```

Create the block progress repository - this will create an azure storage table with the required name prefix. 
``` csharp
var blockProgressRepository = azureTablesRepositoryFactory.CreateBlockProgressRepository();
```

Create a repository storage factory and block processor passing in the Azure tables block progress repository.
``` csharp
var context = new InMemoryBlockchainStorageRepositoryContext();
var repoFactory = new InMemoryBlockchainStoreRepositoryFactory(context);
var processor = web3.Processing.Blocks.CreateBlockStorageProcessor(blockchainStorageFactory: repoFactory, blockProgressRepository: blockProgressRepository);
```
