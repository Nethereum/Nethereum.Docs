# Log Processing (aka Event Log Processing)

## Summary
Log processing involves retrieving logs in sequential order and doing something with them. The term processing in this case refers to batch or continual processing requirements.  You simply plug in your own functionality to handle the relevant logs  whilst Nethereum looks after the navigation, retrieval, decoding and progress monitoring.

### What it's good for!
The processing components are primarily designed for longer running processes, where an app, process, thread or service is dedicated to continually processing logs.  It provides the scaffolding for a dedicated process which allows developers to easily plug in the required handling code. 

Typical use cases:
* triggering workflows based on events.
* event reporting.
* auditing.

The processsing classes build on core Nethereum event log classes which are definitely worth understanding first. [Getting started with events](http://docs.nethereum.com/en/latest/Nethereum.Workbooks/docs/nethereum-events-gettingstarted/)

### What it's not for!
* Retrieving and decoding a single event.
* When you don't need continual or batch processing.
* Learning about event retrieval in Nethereum.
* Absolute real-time processing (see below):
    * Strictly speaking, log processing is not real-time, it's an intelligent polling mechanism. It can be configured to be close enough for most needs.  However another option is to use  Web Socket Streaming for data retrieval.  This can makes sense when you only need the newest logs and are not concerned with the past. Example: https://github.com/Nethereum/Nethereum/blob/master/src/Nethereum.WebSocketsStreamingTest/Program.cs

DON'T WORRY THOUGH - Nethereum still fulfils your event requirements. See the docs:  [Getting started with events](http://docs.nethereum.com/en/latest/Nethereum.Workbooks/docs/nethereum-events-gettingstarted/). 

## Too impatient to read further!? Show me the SAMPLES!
There are several varied samples in the Netherum playground: http://playground.nethereum.com/.

## What's a Log Processor?
It is an orchestrator that co-ordinates retrieving logs, applying criteria and invoking the code you plug in.  It minimises the boiler plate code you need to write.  It helps you to filter the events you require and can automatically decode them if necessary.  It takes care of progress tracking so you gain "restartability"!   It has some inbuilt retry logic to cope with connectivity errors during log retrieval.

### Actions (sync and async)
The processor allows you to plug in actions which can be synchronous or async.  This is where you put the code to handle the matching logs. Async actions are ideal for writing to async API's which are common when integrating with external systems and persistence stores. Synchronous actions are great for performance when you don't need async calls.

### Criteria (sync and async)
You can implement criteria which can be synchronous or async.  Criteria dictates whether or not your action is invoked. Async criteria allows you to do dynamic lookups which may involve external calls to registries/databases/web services etc.  For instance, whilst processing you may need to check dynamic registries as part of your criteria and naturally these calls tend to be async.  Synchronous criteria allows you to inject in-memory criteria easily.

### ProcessorHandler
Under the hood - the actions and criteria are loaded into a ProcessorHandler for you.  If you prefer not to use actions and criteria in the form of Lambda's you can inject your own instances of a ProcessorHandler.  This can provide more flexibility, for instance see "Processing multiple specific events" below. The ProcessHandler approach allows you to use your choice of DI framework to build these handlers. 

## Creating a Log Processor
In this example, let's say we want to sequentially retrieve any log for any contract address from the Blockchain.  It could represent some global and generic log monitoring tool.

You'll need the core Nethereum nuget: **Nethereum.Web3**

These namespaces.
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

You need something to do with the logs retrieved. In this example we're going to put them in an in-memory list.  ``` FilterLog ``` is a Nethereum class that contains the log. It contains the fields common to all logs (BlockNumber, TransactionHash etc) as well as the encoded event information. If you require the event parameter values, they are encoded in the Topic array and require an extra step to decode them (e.g. ``` filterLog.DecodeEvent<TEventDto>() ```).  

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

The processor will run until logs for the last block number have been processed.

## Log Processor Creation Options
There are several methods to create a log processor e.g. ``` web3.Processing.Logs.CreateProcessor ```.  They are designed to help you create the right processor for your needs.

### Selecting the logs you want
During processing, logs are requested sequentially by block number range. Selection of the logs to process can occur in two places and it's important to understand them.

1. During Log Retrieval: (when logs are requested from the Blockchain client).

    * Under the hood the processor calls this method to retrieve the next batch of logs ``` web3.Eth.Filters.GetLogs.SendRequestAsync(filter) ```.  It accepts a filter which contains criteria.
    * Only logs matching the filter are returned to the processor.  When a filter is not specified an empty filter is passed containing only block range criteria, which means all logs for that block range are returned to the processor from the Blockchain client.
    * The filter can contain contract addresses, event signatures, block number ranges and indexed event parameter values (aka topics).
    * Some of the CreateProcessor methods create a filter implicitly - see below.
    * For performance reasons it's important to use the appropriate method to create a processor where possible as it limits the amount of data being retrieved and processed.

2. After Log Retrieval: (In the processor criteria).

    * This is the logic you inject into the processor that occurs after the log retrieval stage.  The action injected into the processor is only invoked if the criteria is met.
    * This can be useful when a filter can not support the criteria necessary. (e.g. when the criteria is more complex or dynamic).   

**Log Processor Creation Methods**

### ``` CreateProcessor ```
Any type of log (FilterLog) from the chain.  If you want to process more than one type of event with one processor you will need to use this option. See examples below. You can use criteria to select the logs you want to process.

### ``` CreateProcessor<TEventDTO> ```
Logs for a specific event (via a filter).  Further event specific criteria can be applied.  

### ``` CreateProcessorForContract ```
Logs for a specific contract address (via a filter). Further criteria can be applied.

### ``` CreateProcessorForContract<TEventDTO> ```
Logs for a specific contract address and event (via a filter). Further criteria can be applied.

### ``` CreateProcessorForContracts ```
Logs matching the contract addresses (via a filter). Further criteria can be applied.

### ``` CreateProcessorForContracts<TEventDTO> ```
Logs matching the contract addresses (via a filter) for a specific event. Further criteria can be applied.

## Optional Parameters

* minimumBlockConfirmations
    * This ensures blocks are only processed once the required number of confirmations is met.  This helps to protect against processing data affected by block reorganisation. The default is 12.  
* log
    * An instance of ILog to provide extra logging of processing activity. Default is null.
* blockProgressRepository (vital for restartability!)
    * Storage of the last block number processed. (see below!). Default is an In-Memory repository

## Block Progress Repository
Providing a block progress repository is necessary for continual processing, it allows the processor to begin where it left off.  A block progress repository provides storage of the last block processed.  The ``` IBlockProgressRepository ``` interface is very simple and easy to implement.  You can either use one of the Nethereum implementations or create your own.  If you don't provide a repository an in-memory repository is created for each processor.

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

### Block Repository Example using Azure Table Storage

This demonstrates usage of the block progress repository provided for Azure Tables by Nethereum.  This stores the last block number processed in an Azure storage table.

**Requires Nuget package: Nethereum.BlockchainStore.AzureTables**

Namespace
``` csharp
#r using Nethereum.BlockchainStore.AzureTables.Bootstrap;
```

Create an azure tables repository factory.  You'll need to pass your azure connection string.  You can also provide a table prefix (in the example we're using "samples") which means any table created in Azure by the factory is prefixed.  The prefix allows the same azure storage account to be used for multiple processors.  
``` csharp
var azureTablesRepositoryFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "samples");
```

Create the block progress repository - this will create an azure storage table with the required name prefix. 
``` csharp
var blockProgressRepository = azureTablesRepositoryFactory.CreateBlockProgressRepository();
```

In this example the table created would be called "samplesCounters".  The table would contain two columns, Name and Value.  Theoretically other counters can be stored in this table but by default, after processing, there would only be one row with a Name value of "LastBlockProcessed".

Create the log processor and pass in the block progress repository.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(
    action: log => logs.Add(log), 
    blockProgressRepository: blockProgressRepository);
```

Each time a block number is processed the progress repository is updated.

## Generic log processing (non event specific)

An example of processing any log (aka FilterLog) where event parameter decoding is not required.

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

Relevant to:
* ``` CreateProcessor<TEventDTO> ```
* ``` CreateProcessorForContract<TEventDTO> ```
* ``` CreateProcessor<TEventDTO>ForContracts<TEventDTO> ```

Creating a processor for a specific event ensures the processor will only retrieve logs matching the event and can accept event specific actions and criteria.  The logs will be decoded automatically.  Therefore the decoded event log is passed to the criteria and the action.  Therefore you can access the event parameters via typed properties on the event DTO.

In this example were going to process ERC20 Transfer events.  This is where we'll put them:
``` csharp
var transferEventLogs = new List<EventLog<TransferEvent>>(); //somewhere to put matching Transfers
```

Create the Transfer specific processor for a specific contract and inject our event specific action.  In the example we're simply adding the transfer to a list.
``` csharp
var processor = web3.Processing.Logs.CreateProcessorForContract<TransferEvent>(
    "0x109424946d5aa4425b2dc1934031d634cdad3f90", 
    action: tfr => transferEventLogs.Add(tfr));
```

Creating a processor with event specific criteria.  In this example the criteria ensures the Transfer value exceeds zero.
``` csharp
var processor = web3.Processing.Logs.CreateProcessorForContract<TransferEvent>(
    "0x109424946d5aa4425b2dc1934031d634cdad3f90", 
    action: tfr => transferEventLogs.Add(tfr),
    criteria: tfr => tfr.Event.Value > 0);
```

## Processing multiple specific events

Let's say you need to process a few specific events.  The setup is slightly more involved and there are 3 main options:

1. Use one processor and provide an array of ProcessorHandler<FilterLog>.  

Each handler evaluates the log returned from the Blockchain node and executes the given action.  Nethereum provides ``` EventLogProcessorHandler<TEventDTO> ``` to achieve this for specific events.  It matches the event signature and does the decoding for you if the signature matches.  This handler ensures that the action is only invoked if the log matches the event.

An example of processing the two popular Transfer events (ERC20 and ERC721).  The example below results in the processor retrieving all logs but only processing logs matching the events.  

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
// to restrict the number of logs being retrieved you could pass a filter
//var filter = new NewFilterInput() { Address = new[] { "0x109424946d5aa4425b2dc1934031d634cdad3f90" } };
//var processor = web3.Processing.Logs.CreateProcessor(logProcessors: processingHandlers, filter: filter); 
```

2. Create an event specific processor for each event you wish to process.   

This is straightforward and can be more efficient.  This is because each processor only retrieves logs matching the event via a filter.  This limits the amount of data being transferred and processed.  However you must ensure that each processor has it's own block progress repository and that the repositories don't share the same persistence store (e.g. database table).

Creating a processor for each event.
``` csharp
var erc20transferEventLogs = new List<EventLog<TransferEvent>>(); // erc20 transfers
var erc721TransferEventLogs = new List<EventLog<Erc721TransferEvent>>(); // erc721 transfers

var p1 = web3.Processing.Logs.CreateProcessor<TransferEvent>(tfr => erc20transferEventLogs.Add(tfr));
var p2 = web3.Processing.Logs.CreateProcessor<Erc721TransferEvent>(tfr => erc721TransferEventLogs.Add(tfr));
```

3. Create a generic processor and apply criteria and specific event decoding.

Applying event signature checks and decoding in the action.
``` csharp
var processor = web3.Processing.Logs.CreateProcessor(
    action: log => 
    {
        if(log.IsLogForEvent<TransferEvent>())
        {
            erc20transferEventLogs.Add(log.DecodeEvent<TransferEvent>());
        }
        if(log.IsForEvent<Erc721TransferEvent>())
        {
            erc721TransferEventLogs.Add(log.DecodeEvent<Erc721TransferEvent>());
        }
    });
```

## Execution

To run the processor call one of the ExecuteAsync overloads.

Execution depends on a block progress repository to dictate which block to start from.  If the repository has not been specified, an in memory repository is created by default.  

The general rule is that processing will start at the block after the last processed block.  However it is possible to set a starting block number for situations where the progress repository is empty or has fallen too far behind.  If the last processed block from the progress repository exceeds the starting block, the value from the repository wins.

### Cancellation
To stop the processor during execution, call ``` cancellationTokenSource.Cancel() ```.

### Processing a specific range:
``` csharp
await processor.ExecuteAsync(
    toBlockNumber: new BigInteger(3146690),
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(3146684));
```

### Processing continually - the block progress repository dictates where to start:
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationToken);
```

### Processing continually - passing a starting block number. 
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(3146684));
```