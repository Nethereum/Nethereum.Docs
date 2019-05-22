# Event Log Processing

So... you want to get event logs from the chain.  Why?

- your app executes a blockchain transaction and needs to wait for an event to confirm success or trigger a workflow.
- you need to capture event data for custom smart contracts that popular blockchain explorers can't show.
- you are harvesting events for reporting.
- you need an audit.
- you are monitoring your own contract.
- you are monitoring many contracts.
- you need to monitor many contracts and many events.
- you are just nosey and want to see what's going on in the blockchain.

Actually, the Nethereum.Web3 nuget package does give you all you need to do that. However, there is a bit of a learning curve.  There are also some challenges due to the differing behaviour and limitations of the various clients and hosts (geth, infura, parity etc).  

The Nethereum.BlockchainProcessing library aims to simplify event processing and get you going quickly.  The components are built to be flexible and extensible so that most needs can be catered for.

## EventLogProcessor

This class is definitely where you should start.  With a few lines of code you can be processing events.

The EventLogProcessor navigates the blockchain in sequential block order and provides functionality to retrieve, decode and filter events.  You just need to plug in your event subscriptions.  It has some error handling and retry logic built in to cope with common problems and provide some resilience.   It's a class that brings together an entire library of processing components which can also be used in isolation.

## Samples
There are complete samples in the repository below.

* Event subscription for one or many contracts
* Event subscription for specific events
* "Catch All" event subscriptions
* Filtering
* Storing progress in Azure Table Storage
* Storing event logs in an Azure Table Storage
* Adding event logs to an Azure Queue
* Adding events logs to an Azure Search Index

https://github.com/Nethereum/Nethereum.BlockchainProcessing/blob/master/Nethereum.BlockchainProcessing.Samples/SimpleEventLogProcessing.cs

### Prerequisites
1. Nuget package: Nethereum.BlockchainProcessing 

### Super Basic Example

**Subscribing to a specific event on a contract**

``` csharp
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.BlockchainProcessing.Processing.Logs;
using System;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;

namespace Nethereum.BlockchainProcessing.Samples
{
    public class EventLogProcessingSample
    {
        /// <summary>
        /// Represents a typical ERC20 Transfer Event
        /// </summary>
        [Event("Transfer")]
        public class TransferEventDto : IEventDTO
        {
            [Parameter("address", "_from", 1, true)]
            public string From { get; set; }

            [Parameter("address", "_to", 2, true)]
            public string To { get; set; }

            [Parameter("uint256", "_value", 3, false)]
            public BigInteger Value { get; set; }
        }

        public async Task RunAsync()
        {
            // create and configure the processor
            var processor =
                new EventLogProcessor(blockchainUrl: "<url>", contractAddress: "<contract address>")
                .Subscribe<TransferEventDto>((events) => { /* do something with the events here */ });

            // create a cancellation token
            // in this sample we're automatically cancelling after 2 minutes
            var cancellationTokenSource = new CancellationTokenSource(TimeSpan.FromMinutes(2));

            // Run the processor
            var blockRangesProcessed = await processor.RunAsync(cancellationTokenSource.Token);
        }
    }
}

```

``` csharp
// OR - if you want an async subscription handler - wire it up like this
var processor =
    new EventLogProcessor(blockchainUrl: "<url>", contractAddress: "<contract address>")
    .Subscribe<TransferEventDto>(async (events) => { await YourTask(events); }); // replace "YourTask" with your code!!
```

The code above sets up an event log processor which subscribes to ERC20 Transfer events from a specific contract address.  It will start from the current block on the chain but it is possible to dictate a specific starting block.  It passes matching events to a lambda so you can trigger your own code. 

### Contract API's and Code Generation

The TransferEventDto in the sample is a class (aka DTO) representing an Event.  It is an example of "typed" event processing (see [Typed vs UnTyped Processing](#Typed-vs-UnTyped-Processing)).  From this DTO, Nethereum can derive the event signature and be able to decode event information from a log.  In some scenarios it is easy to create the event DTOs you need manually especially if there are only a few events you want to subscribe to. However using code generation to generate your contract API's is less error prone and a lot faster.  All you need is the ABI file (compiled Solidity contract). 

See: http://docs.nethereum.com/en/latest/nethereum-code-generation/ or http://codegen.nethereum.com/

### Construction and Configuration
Use the constructor parameters and methods below to configure the processor.  Do this before invoking any of the "Run" methods.

The fluent methods aim to make setup quick and intuitive by chaining together configuration and setup calls.  There are public properties on the processor you can access to inspect what has been done by the methods.  You can also make modifications directly to these properties.

**Blockchain Url** - the client or node URL (e.g. https://mainnet.infura.io/v3/<your_access_key>)
It is also possible to pass an instance of the Nethereum Web3 object if you already have one.

**ContractAddress** - restricts the processor to events emitted by this contract.
``` csharp
var processor = new EventLogProcessor(blockchainUrl: "<url>", contractAddress: "<contract address>")
```

**ContractAddresses** - restricts the processor to events emitted by any of these addresses.
``` csharp
var processor = new EventLogProcessor(blockchainUrl: "<url>", contractAddresses: new []{"<contract addresses>"})
```

**MinimumBlockNumber** - if you have not processed anything previously or the last processed block number in the block progress repository has fallen too far behind - this enables you to set a minimum block number at which to start processing.

**MaximumBlocksPerBatch** - a single batch is processed for a specific block number range  (e.g. 10 - 20).  This property limits the number of blocks in that range.  If you're on a busy chain and have lots of matching events you may need to experiment with this value to avoid errors thrown by the node/client when their thresholds are exceeded.

**MinimumBlockConfirmations** - to help cope with forks on the chain (and avoid processing orphaned blocks) you can set the number of block confirmations you wish to wait before reading the events.  There are Ethereum recommendations for this but these can change depending on the type of chain you are targetting.  The default value is 0 but it is recommended that you alter this to suit your needs.

``` csharp
// creating and configuring a processor
var processor = new EventLogProcessor(blockchainUrl: "<put url here>")
    .Configure(c => c.MaximumBlocksPerBatch = 1) //optional: restrict number of blocks in a batch, default is 100
    .Configure(c => c.MinimumBlockNumber = 7540102) //optional: default is to start at current block on chain
    .Configure(c => c.MinimumBlockConfirmations = 10) //optional: but it's best to set it explicity (default is 0)
    .Subscribe<TransferEventDto>(events => { /*  handle events here  */ })
```

### Running the Processor

**Important**: Fully configure the processor BEFORE before running it.

* **RunAsync**: 
    This continually processes until the cancellation token is invoked.  It blocks the current thread whilst running.  If your app is specific to event processing then you might want to use this option.

* **RunInBackgroundAsync**: 
    This continually processes but on a background thread so you can work in parallel.  It is also stopped using the cancellation token. This allows your app to continue with other work whilst processing continues.

``` csharp
var backgroundTask = await processor.RunInBackgroundAsync(cancellationTokenSource.Token);
// the await ensures the setup phase runs and you can catch set up or configuration errors
// the processing phase begins on a background thread and therefore does not block the current thread
```

* **RunForLatestBlocksAsync**: 
    This processes the next block number range.  If there were no blocks waiting to be processed (e.g. processing is already up to date) it will return null.  The number of blocks to process in a batch is dictated by the MaximumBlocksPerBatch property.  It uses the BlockProgressRepository to define which block to start from.   You would normally favour this option to run processing on a timer (e.g. WebJob). 

### Keeping Track of Block Progress
The processor needs to know where to start from and what has already been processed. By default the processor keeps track of blocks processed in memory.  That's fine for short lived processing but for resilience and to survive restarts you may consider a persistent block progress repository.  See the options below:

**Json File** 
``` csharp
var processor = new EventLogProcessor(blockchainUrl: "<url>")
    // tell the processor to use a Json File based Block Progress Repository
    .UseJsonFileForBlockProgress(jsonFilePath);
```

**Azure Table Storage**
``` csharp
var processor = new EventLogProcessor(blockchainUrl: "<url>")
    // tell the processor to reference an Azure Storage table for block progress
    // this is an extension method from Nethereum.BlockchainStore.AzureTables
    // "EventLogProcessing" is the prefix for the table in Azure
    // The table prefix is useful when you want to run different processors with their own progress
    .UseAzureTableStorageForBlockProgress(azureStorageConnectionString, "EventLogProcessing");
```

**Custom / Roll Your Own Progress Repository**
``` csharp
// Your own class implementing IBlockProgressRepository
public class CustomBlockProgressRepo : IBlockProgressRepository
{
    /*
    Task UpsertProgressAsync(ulong blockNumber);
    Task<ulong?> GetLastBlockNumberProcessedAsync();
    */
}
var processor = new EventLogProcessor(blockchainUrl: "<url>")
    .UseBlockProgressRepository(new CustomBlockProgressRepo());    
```
### Monitoring the processor

It's good to know how processing is going.  Maybe you just want to know it's alive or you want to trigger some logging every time a batch is processed.  This is what the "OnBatchProcessed" callback if for.  Each time a batch is processed this callback is invoked.  It reports the total number of batches (aka ranges) processed so far and the range that was last processed.  It you need to cancel processing this is an ideal place to call Cancel on the cancellation token source. 

``` csharp
var processor = new EventLogProcessor(blockchainUrl: "<url>")
    .OnBatchProcessed((batchesProcessedSoFar, lastBlockRange) => { /* your monitoring code goes here - or maybe cancellationTokenSource.Cancel() */});
```

### Per Batch Iteration Workflow
On a single batch iteration the processor follows the high level workflow below.  If you're not seeing the events you expect - double check this.

* Get event logs By current block number range 
    * Without filters - grab all logs fgit or current block range
    *  OR
    * With filters - For each filter, retrieve all matching logs for the current block range. Then amalgamate and dedupe into one list.
* Pass each log from the list to each log processor (e.g. processor.Processors) to define if it is a match (e.g. IsLogForEvent?) and add matching logs to batches per log processor (the same log can be processed by many processors).
* Instruct each log processor to process their batch of logs.

### Adding Your Own Processor

The EventLogProcessor is really just an orchestration for a list of log processors  (e.g. processor.Processors).

Calling Subscribe() on the Fluent API adds an instance of one of the out of the box log processor implementations.  These implementations do the event signature matching and decoding for you.  They just require a lambda to be passed in where you implement your own functionality with the decoded event log. 

However, should you wish to have more control - it is also possible to inject your own log processor.  Each log processor must implement the simple ILogProcessor interface - see below.  

``` csharp
//untyped - non event specific
public class CustomLogProcessor : ILogProcessor
{
    public bool IsLogForEvent(FilterLog log){/* decide if the log is of interest */}

    public async Task ProcessLogsAsync(params FilterLog[] eventLogs){/* do something with these logs */}
}

//typed - event specific
public class CustomLogProcessor<TEventDto> : ILogProcessor where TEventDto : class, IEventDTO, new()
{
    public bool IsLogForEvent(FilterLog log){ /* e.g return log.IsLogForEvent<TEventDto>(); */}

    public async Task ProcessLogsAsync(params FilterLog[] eventLogs)
    {
        /* e.g. decode them
                 var decodedEvents = eventLogs.DecodeAllEvents<TEventDto>();
          */
    }
}

var processor =
    new EventLogProcessor(blockchainUrl: "<url>", contractAddress: "<contract address>")
    .Subscribe(new CustomLogProcessor()) // any event log
    .Subscribe(new CustomLogProcessor<TransferEventDto>()); // transfer logs
```

### Filters

**Important: Filters are easily misunderstood - so please read this!!**

Step one in a processing iteration is to retrieve the logs for the current block range.  This is done before any of the log processors are invoked.  It is possible to filter at this stage to limit the number of event logs being retrieved from the chain and passed for evaluation to the log processors.

In the context of event log processing, a filter is used as a query to request matching logs from the chain. If you specify a contract address then a filter will be automatically created to ensure that only logs for that contract are requested from the chain.  This happens BEFORE the log processors are called.  If you don't specify a contract address and have not specified additional filters then ALL events for the current block range will be requested.  That could be a lot of data being transferred from the client across the network to your app.

Having multiple filters means running multiple requests to the chain to retrieve logs for each filter.  The logs returned by each filter are then deduped (using a composite key involving block number, transaction hash and log index) and amalgamated in to one list for processing.  **To be processed - an event log only has to match ONE of the filters - not all of them**.

### Topic / Event Parameter Filtration

Providing a smart contract event has indexed parameters then event logs matching those parameters can be retrieved.  For event processing this allows you to request all event logs matching a event signature (e.g a Transfer event) and specific parameter value or values (e.g. From and To).

``` csharp
// transfer events from and to specific addresses
var transferFromAndToAddressFilter = new NewFilterInputBuilder<TransferEventDto>()
    .AddTopic(t => t.From, "<from address>")
    .AddTopic(t => t.To, "<to address")
    .Build();

// setup the processor for only events matching this filter
var processor = new EventLogProcessor(TestConfiguration.BlockchainUrls.Infura.Mainnet)
    .Filter(transferFromAndToAddressFilter) 
    .Subscribe<TransferEventDto>((events) => { /* do something with the filtered events here */ }); 

```

### Catch All Events

In some cases you may want to catch all matching events to do something common to all of them.  This might be for logging different event types or maybe you require an interception point for debug purposes.  The "CatchAll" method creates a log processor which matches any event log (post filter). 

With "CatchAll" you're not dealing with Typed event DTOs, you are dealing with an array of FilterLog objects.  A FilterLog is a Nethereum class used to contain the generic event log information.  This means the event parameters aren't decoded. However you do get direct access to the block number, transaction hash, log index and encoded topics etc.  This may be sufficient for some needs.  You may wish to store the FilterLog somewhere and decode it at a later date (which is straightforward).  Alternatively you might just want to store minimal info like the transaction hash and log index.

**For a specific contract address**
``` csharp
var processor = new EventLogProcessor(TestConfiguration.BlockchainUrls.Infura.Mainnet, ContractAddress)
    .CatchAll((events) => { /* your code goes here */}); 

```
**For a specific event on any contract**
``` csharp
var processor = new EventLogProcessor(TestConfiguration.BlockchainUrls.Infura.Mainnet)
    .Filter<TransferEventDto>() 
    .CatchAll((events) => { /* your monitoring code goes here */});
```

### Handing Fatal Errors

The processor has some inbuilt reliability and retry logic.  However there may be times when a fatal error is thrown whilst processing and processing stops.  To react use the OnFatalError callback.

``` csharp
var processor = new EventLogProcessor(TestConfiguration.BlockchainUrls.Infura.Mainnet, ContractAddress)
    .Subscribe<TransferEventDto>((events) => erc20Transfers.AddRange(events)) // transfer events
    .OnFatalError((ex) => { /* do something with exception here */});
```

### Typed vs UnTyped Processing

**typed**
The example above uses the typed approach to contract interaction which is normally recommended.  This is shown in the line ``` .Subscribe<TransferEventDto>() ```.  The TransferEventDto is a class that represents the event the sample wants to capture.  The typed approach means using classes to represent event arguments and function inputs and outputs.  It is generally the best way to interact with Ethereum as it is easier to understand, less error prone and can be code generated (see below).  When using the typed approach, the event arguments are automatically decoded for you and filtering is made easier.  

**untyped**
Occasionally the untyped approach is better.  This is particularly useful when processing does not need to capture event arguments and only requires information which is common to all logs regardless of the event emitted.   It means you do not have to create or maintain event DTOs.   To use the processor in an untyped way, use the methods ``` .Subscribe(logs => ....) ``` and ``` .CatchAll(logs => ....) ``` methods.  These are the methods without generic arguments.  In this scenario, instead of handling a decoded event specific object, you handle FilterLog objects.  The FilterLog contains all of the blockchain event log data but the event arguments are not decoded.  It is possible to decode them later though e.g. ``` filterLog.DecodeEvent<TEventDto>() ```.


