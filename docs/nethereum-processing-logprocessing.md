# Log Processing (aka Event Log Processing)

## Summary
Log processing involves retrieving logs in sequential order and doing something with them.  What you do with them is up to you! The idea is that plug in your own functionality to handle the relevant event logs whilst Nethereum looks after the navigation, retrieval, decoding and progress monitoring.

### What it's good for!
The processing components are primarily designed for longer running processes, where an app/process/thread/service is dedicated to continually retrieving logs.  It provides the scaffolding for a dedicated process which allows developers to easily plug in the required handling code. 

Typical use cases:
* triggering workflows based on events.
* event reporting.
* auditing.

The processsing classes use other core Nethereum event log classes which are worth understanding first. [Getting started with events](http://docs.nethereum.com/en/latest/Nethereum.Workbooks/docs/nethereum-events-gettingstarted/)

### What it's not for!
* When you don't need to track progress.
* When you don't need continual processing - it's a one off.
* Learning about event retrieval

Nethereum still provides all you need to retrieve your events. See the docs:  [Getting started with events](http://docs.nethereum.com/en/latest/Nethereum.Workbooks/docs/nethereum-events-gettingstarted/). 

## Too impatient to read further!? Give me samples!
There are several samples in the Netherum playground: http://playground.nethereum.com/.

## What's a Log Processor?
It orchestrates retrieving the logs and invoking the code you plug in.  It minimises the boiler plate code you need to write.  It helps you to filter the events you require and can automatically decode them if necessary.  It takes care of progress tracking so you don't need to write your own.   It has some inbuilt retry logic to cope with connectivity errors during log retrieval.

### Actions
It allows you to plug in actions which can be synchronous or async.  This is where you put the code to handle the matching logs. Async actions are ideal for writing to async API's which are common when integrating with external systems and persistence stores.  

### Criteria
You can also implement criteria which again can be synchronous or async.  Criteria can dictate whether or not your action is invoked. Async criteria allows you to do dynamic lookups which may involve external calls to registries/databases/web services etc. 

## Creating a Log Processor
Let's say we want to sequentially retrieve any log from the Blockchain.

You'll need these namespaces.
``` csharp
using Nethereum.RPC.Eth.DTOs;
using Nethereum.Web3;
using System;
using System.Collections.Generic;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;
```

You'll need an instance of Web3 configured for the network you want to target.
``` csharp
//if using Infura, you'll need to replace this value "7238211010344719ad14a89db874158c" with your own Infura PROJECT-ID
var web3 = new Web3("https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c");
```

You'll need somewhere to put the logs retreived, in this example we're using an in-memory list.  ``` FilterLog ``` is a Nethereum class that contains the complete log (block number, transaction hash, event topics etc). It can represent any event but the event parameters are encoded and therefore decoding is necessary to read the actual event parameters.  
``` csharp
var logs = new List<FilterLog>(); // somewhere to put our logs
```

Create the processor and inject a lambda to handle each log.  In this case - we're simply adding it to the list.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(log => logs.Add(log));
```

Execute the processor for a specific block range.  
``` csharp
//if we need to stop the processor mid execution - call cancel on the cancellation token source
var cancellationTokenSource = new CancellationTokenSource();

await processor.ExecuteAsync(
    toBlockNumber: new BigInteger(3146690),
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(3146684));
```

## Log Processor Options
There are several methods to create a log processor e.g. ``` web3.Processing.Logs.CreateProcessor ```.  They were designed to help you create the right processor for the right purpose.

### Filtering and Criteria
During processing, logs are requested one block number range at a time. Filtration of logs to process can occur in two places and it's important to understand how it works.

1. During Log Retrieval: (via a Filter when logs are requested from the Blockchain client, ``` web3.Eth.Filters.GetLogs.SendRequestAsync(filter) ```).

    * Only logs matching the filter are returned to the processor.  When a filter is not specified an empty filter is passed containing only block range criteria, which means all logs for that block range are returned to the processor from the Blockchain client.
    * The filter can contain contract addresses, event signatures, block number ranges and indexed event parameter values (aka topics).
    * Some of the CreateProcessor methods create a filter implicitly (see below).
    * For performance reasons it's important to use the appropriate method to create a processor where possible as it limits the amount of data being retrieved and processed.

2. After Log Retrieval: (In the processor criteria).

    * This is the logic you inject into the processor that occurs after the log retrieval stage.  The action injected into the processor is only invoked if the criteria is met.
    * This can be useful when a filter does not support the criteria necessary (e.g. when criteria involves an event parameter which is not indexed).   

### CreateProcessor
This processor will retrieve any type of log (FilterLog) from the chain.  If you want to process more than one event you will need to use this option. You can also use client side criteria to select the logs you want to process.

### CreateProcessor<TEventDTO>
This processor will only retrieve logs for a specific event (via a filter).  Further event specific criteria can then be applied.  

### CreateProcessorForContract
The processor will only retrieve logs for a specific contract address (via a filter). Further criteria can then be applied.

### CreateProcessorForContract<TEventDTO>
The processor will only retrieve logs for a specific contract address and event (via a filter). Further criteria can then be applied.

### CreateProcessorForContracts
The processor will only retrieve logs from one of the required contracts (via a filter). Further criteria can then be applied.

### CreateProcessorForContracts<TEventDTO>
The processor will only retrieve logs matching an event from one of the required contract addresses (via a filter). Further criteria can then be applied.

## Optional Parameters

* minimumBlockConfirmations
    * Ensure blocks are only processed if the required number of confirmations is met.  This protects against block reorganisation. Default is 12.
* log
    * An instance of ILog to provide extra logging of processing activity. Default is null.
* blockProgressRepository
    * see below! Default is an In-Memory repository

## Progress Repositories
Providing a block progress repository allows the processor to begin where it left off.  A block progress repository provides storage of the last block processed.  The ``` IBlockProgressRepository ``` interface is very simple and easy to implement.  You can either create your own or use one of the Nethereum implementations.

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

### Azure Storage Table Block Progress Repository Example

This demonstrates usage of the block progress repository provided for Azure Tables by Nethereum. 

**Requires Nuget package: Nethereum.BlockchainStore.AzureTables**

Namespace
``` csharp
#r using Nethereum.BlockchainStore.AzureTables.Bootstrap;
```

Create an azure tables repository factory.  You'll need to pass your azure connection string.  You can also provide a table prefix (in the example we're using "samples") which means any table created in Azure by the factory is prefixed.  It allows the same azure storage account to be used for multiple processors.
``` csharp
var azureTablesRepositoryFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "samples");
```

Create the block progress repository - this will create an azure storage table with the required name prefix. 
``` csharp
var blockProgressRepository = azureTablesRepositoryFactory.CreateBlockProgressRepository();
```

Create the log processor and pass in the block progress repository.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(
    action: log => logs.Add(log), 
    blockProgressRepository: blockProgressRepository);
```

Once the events in a block range are processed the progress repository is updated.

## Generic log processing (non event specific)

An example of processing any log (aka FilterLog).

``` csharp
var logs = new List<FilterLog>(); // somewhere to put the logs
```

Adding any log to the list.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(
    action: log => logs.Add(log));
```

Applying some criteria.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(
    action: log => logs.Add(log), 
    criteria: log => log.Removed == false);
```

## Event specific processing

Creating a processor for a specific event ensures the processor can accept event specific actions and criteria. If the log matches the event it will be decoded automatically.  Therefore the decoded event log is passed to the criteria and the action.

``` csharp
var transferEventLogs = new List<EventLog<TransferEvent>>(); //somewhere to put matching Transfers
```

Processing Transfer events for a specific contract with event specific action.
``` csharp
var processor = web3.Processing.Logs.CreateProcessorForContract<TransferEvent>(
    "0x109424946d5aa4425b2dc1934031d634cdad3f90", 
    action: tfr => transferEventLogs.Add(tfr));
```

Event specific criteria.  This criteria ensures the Transfer value exceeds zero.
``` csharp
var processor = web3.Processing.Logs.CreateProcessorForContract<TransferEvent>(
    "0x109424946d5aa4425b2dc1934031d634cdad3f90", 
    action: tfr => transferEventLogs.Add(tfr),
    criteria: tfr => tfr.Event.Value > 0);
```

## Processing multiple specific events

Let's say you need to process a few specific events.  There are 2 options:

1. Use one processor and provide an array of ProcessorHandler<FilterLog>.  Each handler evaluates the log returned from the Blockchain node and executes the given action.  Nethereum provides ``` EventLogProcessorHandler<TEventDTO> ``` to achieve this for specific events.  It matches the event signature and does the decoding for you if the signature matches.  This handler ensures that the action is only invoked if the log matches the event.

An example of processing the two popular Transfer events (ERC20 and ERC721).
``` csharp
var erc20transferEventLogs = new List<EventLog<TransferEvent>>(); // erc20 transfers
var erc721TransferEventLogs = new List<EventLog<Erc721TransferEvent>>(); // erc721 transfers

var erc20TransferHandler = new EventLogProcessorHandler<TransferEvent>(
    eventLog => erc20transferEventLogs.Add(eventLog));

var erc721TransferHandler = new EventLogProcessorHandler<Erc721TransferEvent>(
    eventLog => erc721TransferEventLogs.Add(eventLog)); 

var processingHandlers = new ProcessorHandler<FilterLog>[] {
    erc20TransferHandler, erc721TransferHandler};

var processor = web3.Processing.Logs.CreateProcessor(processingHandlers);
```

2. Create an event specific processor for each event you wish to process.   

This is straightforward and may be more efficient.  This is because each processor only retrieves logs matching the event via a filter.  This limits the amount of data being transferred and processed.  However you must ensure that each processor has it's own block progress repository and that the repositories don't share the same persistence store (e.g. database table).
e.g.
``` csharp
var erc20transferEventLogs = new List<EventLog<TransferEvent>>(); // erc20 transfers
var erc721TransferEventLogs = new List<EventLog<Erc721TransferEvent>>(); // erc721 transfers

var p1 = web3.Processing.Logs.CreateProcessor<TransferEvent>(tfr => erc20transferEventLogs.Add(tfr));
var p2 = web3.Processing.Logs.CreateProcessor<Erc721TransferEvent>(tfr => erc721TransferEventLogs.Add(tfr));
```

## Execution

Execution depends on the block progress repository to dictate which block to start from.  If the repository has not been specified an in memory repository is created by default.  The general rule is that processing will start at the last processed block plus one.  However if the progress repository is empty or has fallen too far behind it is possible to set a starting block number ("startAtBlockNumberIfNotProcessed").  If the last processed block in the progress repository exceeds the starting block the value from the repository wins.

To stop the processor during execution, call ``` cancellationTokenSource.Cancel() ```.

Processing a specific range:
``` csharp
await processor.ExecuteAsync(
    toBlockNumber: new BigInteger(3146690),
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(3146684));
```

Processing continually - the block progress repository dictates where to start:
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationToken);
```

Processing continually - passing a starting block numbert. 
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(3146684));
```





