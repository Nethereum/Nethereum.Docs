# Blockchain Storage on Azure Tables

## Summary
Storing a copy of Blockchain data is a common request.  Wether it's a fragment or entire copy there are a variety of common reasons:

+ Keeping a snapshot of your own data on the chain
+ Providing a Blockchain data based trigger for workflows
+ Audits
+ Alerts
+ Providing a data source that's easy to move and copy

This document focuses specifically on Azure Table Storage but for more on general block processing read [Block Processing](nethereum-block-processing-detail.md). 

Using Azure Storage Tables for storage is a pragmatic and cheap.  Nethereum provides an off-the-shelf solution which is really easy to use.

Within the Nethereum.Web3 nuget (aka Nethereum core) there are block processing components which provide navigation, retrieval and filtration.  It also defines common interfaces for objects in the chain such as blocks, transactions and logs etc.  The Azure tables implementation provides repositories and entities which implement and extend these interfaces.  This makes writing Blockchain data to Azure Storage Tables very straightforward.  You really only need the Azure connection string to get started.

**Disclaimer:**
The Azure storage library is primarily concerned with persistence.  The idea was to quickly and easily write the Blockchain data into tables with sensible pre-defined schema's.  But, whilst it does provide a minimal query interface, to analyse the data captured in more depth you may require 3rd party packages or design your own queries using the WindowsAzure.Storage nuget.

## Sample (in full)

This is a full sample. Feel free to copy and paste and play with it.  It demonstrates storing the data for a particular block.  To run the code all you need to do is set your Azure connection string.

Beneath the sample, the individual steps are explained and broken down.

### Prerequisites
Nuget: **Nethereum.BlockchainStore.AzureTables (includes Nethereum.Web3)**

``` csharp
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.BlockchainProcessing.BlockStorage.Entities.Mapping;
using Nethereum.BlockchainStore.AzureTables.Bootstrap;
using Nethereum.BlockchainStore.AzureTables.Repositories;
using Nethereum.Contracts;
using Nethereum.Hex.HexTypes;
using Nethereum.RPC.Eth.DTOs;
using Nethereum.Web3;
using Newtonsoft.Json;
using System;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;

namespace BlockchainStorageSample
{
    class Program
    {
        static Task Main(string[] args)
        {
            var example = new AzureTableStorageExample();
            return example.RunAsync();
        }
    }

    public class AzureTableStorageExample
    {
        private readonly Web3 _web3;
        private readonly string _azureConnectionString = "<Your Azure Connection String>";
        private const string URL = "https://rinkeby.infura.io/v3/7238211010344719ad14a89db874158c";

        public AzureTableStorageExample()
        {
            _web3 = new Web3(URL);
        }

        public async Task RunAsync()
        {
            var repoFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "bspsamples");

            try
            {
                //create our processor
                var processor = _web3.Processing.Blocks.CreateBlockStorageProcessor(repoFactory);

                //if we need to stop the processor mid execution - call cancel on the token source
                var cancellationTokenSource = new CancellationTokenSource();

                // process the required block range
                await processor.ExecuteAsync(
                    toBlockNumber: new BigInteger(2830144),
                    cancellationToken: cancellationTokenSource.Token,
                    startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

                // PROCESSING IS NOW COMPLETE!
                // retrieve the data from Azure Table Storage
                var blockRepository = repoFactory.CreateBlockRepository() as BlockRepository;
                var transactionRepository = repoFactory.CreateTransactionRepository() as TransactionRepository;
                var addressTransactionRepository = repoFactory.CreateAddressTransactionRepository() as AddressTransactionRepository;
                var transactionLogRepository = repoFactory.CreateTransactionLogRepository() as TransactionLogRepository;
                var contractRepository = repoFactory.CreateContractRepository() as ContractRepository;
                var blockProgressRepository = repoFactory.CreateBlockProgressRepository() as BlockProgressRepository;

                BigInteger? lastBlockProcesed = await blockProgressRepository.GetLastBlockNumberProcessedAsync();
                Console.WriteLine($"Last Block Processed: {lastBlockProcesed}");

                //retrieve a block from storage
                var block = await blockRepository
                    .FindByBlockNumberAsync(new HexBigInteger(2830144));

                Console.WriteLine();
                Console.WriteLine("BLOCK:");
                Console.WriteLine(JsonConvert.SerializeObject(block));

                //retrieve the transactions
                var transactions = await transactionRepository.GetManyAsync(block.BlockNumber);

                foreach(var transaction in transactions)
                { 
                    Console.WriteLine();
                    Console.WriteLine("TRANSACTION:");
                    Console.WriteLine(JsonConvert.SerializeObject(transaction));

                    // Azure storage tables have limited indexes
                    // A single transaction table can not support queries by block, transaction hash and address
                    // Therefore Nethereum creates a duplicate Transaction table
                    // It's partition key is the Address, and the row key is a combination of block number and transaction hash
                    var addressTransaction = await addressTransactionRepository.FindByAddressBlockNumberAndHashAsync(
                        transaction.AddressFrom, 
                        new HexBigInteger(BigInteger.Parse(block.BlockNumber)), 
                        transaction.Hash);

                    if (!string.IsNullOrEmpty(addressTransaction.NewContractAddress))
                    {
                        var contract = await contractRepository.FindByAddressAsync(addressTransaction.NewContractAddress);
                        Console.WriteLine();
                        Console.WriteLine("NEW CONTRACT:");
                        Console.WriteLine(JsonConvert.SerializeObject(contract));
                    }

                    //retrieve the logs
                    var logs = await transactionLogRepository.GetManyAsync(transaction.Hash);

                    foreach (var log in logs)
                    {
                        Console.WriteLine();
                        Console.WriteLine("LOG:");
                        Console.WriteLine(JsonConvert.SerializeObject(log));

                        // inspect the event
                        // for this example - if it's a Transfer event - we'll decode it to retrieve the actual event values
                        var filterLog = log.ToFilterLog();
                        if (filterLog.IsLogForEvent<TransferEventDTO>())
                        {
                            var decodedEvent = filterLog.DecodeEvent<TransferEventDTO>();
                            Console.WriteLine("TRANSFER:");
                            Console.WriteLine(JsonConvert.SerializeObject(decodedEvent));
                        }
                    }
                }
            }
            finally
            {
                await repoFactory.DeleteAllTables();
            }
        }
    }

    [Event("Transfer")]
    public class TransferEventDTO : IEventDTO
    {
        [Parameter("address", "_from", 1, true)]
        public string From { get; set; }

        [Parameter("address", "_to", 2, true)]
        public string To { get; set; }

        [Parameter("uint256", "_value", 3, false)]
        public BigInteger Value { get; set; }
    }
}

```

## The Breakdown

Firstly, create a web3 object. It's the home to lots of Nethereum goodness!  It can be thought of as a proxy to the Blockchain.  The URL is specific to the node/Blockchain client you wish to target.

``` csharp
_web3 = new Web3(URL);
```

Next we create a repository factory.  The factory is responsible for creating repositories for each table.  During processing, the tables are created if they don't exist.  The Azure connection string is required as is a table prefix.  The prefix is added to the table name to provide a means of separation for different data sets.   For instance you might use the name of the network as the prefix e.g. "rinkeby", "ropsten, "mainnet" etc.  Therefore you can have separate copies of Blockchain data using the same Azure account.  The prefix can be an empty string if not required.  The prefix must follow Azure table naming rules, google these if you're not familiar.

``` csharp
// replace "bspsamples" with your choice of prefix
var repoFactory = new AzureTablesRepositoryFactory(_azureConnectionString, "bspsamples");
```
### Tables

These are the tables involved in storage.  Each table will be created with the specified prefix (e.g. "yourPrefixBlocks", "yourPrefixTransactions").  

+ Blocks
+ Transactions
+ AddressTransactions
    - A copy of the transactions table which is keyed by address.  
    - Each address involved in the transaction results in a new row for the transaction.  
    - The address field is the partition key which stores all transaction for an address together.
+ TransactionLogs
    - Home to the transaction logs / aka events.
    - The data is encoded but can be decoded later.
+ Contracts
    - When contract creation transactions are found, the contracts are persisted here.
+ Counters
    - Where block progress is stored and read from.

### Upserts
When persisting data each call is an "Upsert", if it exists, update it else insert it.  Therefore if you need to re-run the processor for the same block range the repository will cope.

``` csharp
var processor = _web3.Processing.Blocks.CreateBlockStorageProcessor(repoFactory);
```

Next we create our block storage processor using our web3 instance.  This processor is from Nethereum core.  It will orchestrate the navigation, retrieval, filtration and invoke the actions necessary.  There's no magic, it's just managing common Nethereum components which are easily accessible via the web3 object.  In this case, the action is to persist the data.  We're passing in our Azure tables repository factory implementation.  That hands out the repositories which are invoked every time something needs persisting.

#### Creating a processor with criteria
If you want to only process specific blockchain data you can specify criteria.  In this example we're only storing transactions sent from a specific address.  This will prevent the processor from retrieving and storing transaction receipts and logs for unrelated transactions.

The minimum block confirmations can also be specified to ensure the processor remains a safe distance from the front of the chain and therefore avoid block re-organisation.

The log parameter accepts an instance of a ``` Common.Logging.ILog ``` implementation.  This can be useful for tracking progress whilst processing.

``` csharp
var processor = _web3.Processing.Blocks.CreateBlockStorageProcessor(
    repoFactory, 
    minimumBlockConfirmations: 6, 
    configureSteps => 
    {

        configureSteps.TransactionStep.SetMatchCriteria(t => t.Transaction.IsFrom("xyz"));
    },
    log: null);
```

#### Adding custom actions

It's possible for custom actions to be invoked at each step.  In the example below we're writing the next block number to the console.
``` csharp
var processor = _web3.Processing.Blocks.CreateBlockStorageProcessor(
    repoFactory, 
    minimumBlockConfirmations: 6, 
    configureSteps => 
    {
        configureSteps.BlockStep.AddProcessorHandler(block => Task.Run(() => Console.WriteLine($"Processing Block: {block.Number.Value}"))); 
    });
```

``` csharp
var cancellationTokenSource = new CancellationTokenSource();
```
Whilst the processor is executing, to cancel it, call Cancel on the cancellation token source.

### Execution

The processor supports two main execution options. 
- Option 1 is running for a specific block range.  
- Option 2 is a continuous processing model.

The parameter "startAtBlockNumberIfNotProcessed" is optional.  By default block progress is read from and updated in a table in Azure ("Counters").  Ordinarily this table would dictate what the next block to process is.  However if you no previous progress, or the last processed block is too old this parameter will dictate the starting block number.

Execution is async - but it's not parallel.  Any code following ExecuteAsync will not be invoked until execution is finished. 

#### Running for a specific block range
``` csharp
await processor.ExecuteAsync(
    toBlockNumber: new BigInteger(2830144),
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(2830144));
```

#### Running continuously from a starting block number
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(2830144));
```

#### Running continuously from the last block processed
``` csharp
await processor.ExecuteAsync(
    cancellationToken: cancellationTokenSource.Token);
```

#### Running on a background thread
``` csharp
var executionTask = processor.ExecuteAsync(
    toBlockNumber: new BigInteger(2830144),
    cancellationToken: cancellationTokenSource.Token,
    startAtBlockNumberIfNotProcessed: new BigInteger(2830144));

while(executionTask.IsCompleted == false)
{
    // simulate doing something else whilst processing happens in the background
    // this gives an opportunity for cancellation if necessary (e.g. cancellationTokenSource.Cancel())
    Console.WriteLine("Waiting....");
    await Task.Delay(100);
}
```

## Reading from the table storage

Access to the data in the tables is via the repositories.  The repository factory provides methods to create repositories for the tables involved.  By default the method signatures on the factory return a repository interface.  The repository interface is in core Nethereum and is deliberately simple and restricted.  This is because any of the storage adapters (Azure Tables, Sql Server, Cosmos, SqLite) are required to implement the interface.  By casting the repository to it's concrete type, more implementation specific methods are available which can be useful for reading or querying.

``` csharp
var blockRepository = repoFactory.CreateBlockRepository() as BlockRepository;
var transactionRepository = repoFactory.CreateTransactionRepository() as TransactionRepository;
var addressTransactionRepository = repoFactory.CreateAddressTransactionRepository() as AddressTransactionRepository;
var transactionLogRepository = repoFactory.CreateTransactionLogRepository() as TransactionLogRepository;
var contractRepository = repoFactory.CreateContractRepository() as ContractRepository;
var blockProgressRepository = repoFactory.CreateBlockProgressRepository() as BlockProgressRepository;
```

### Retrieving the last block processed

``` csharp
BigInteger? lastBlockProcesed = await blockProgressRepository.GetLastBlockNumberProcessedAsync();
```

### Retrieving a block
``` csharp
var block = await blockRepository.FindByBlockNumberAsync(new HexBigInteger(2830144));
```

### Retrieving the transactions for a block
(Ensure you've casted the transaction repo (e.g. ``` repoFactory.CreateTransactionRepository() as TransactionRepository) ```, otherwise you won't see the "GetManyAsync" method)
``` csharp
var transactions = await transactionRepository.GetManyAsync(block.BlockNumber);
```

### Retrieving a single transaction
``` csharp
var transaction = await transactionRepository.FindByBlockNumberAndHashAsync(block.BlockNumber, transactionHash);
```

### Retrieving transactions by address
Azure storage tables have limited indexes, so it's not feasible to query the transaction table easily and quickly by address.  Azure table storage has two primary identifiers, the partition key which can be treat as a grouping and a row key which is like a primary key for a record within a partition key grouping.  The transaction table uses the block number as a partition key and the row key is the transaction hash.  Therefore it can't be used to query by address.  Consequently Nethereum creates a duplicate Transaction table with an extra field called "Address" which is the partition key, and the row key is a combination of block number and transaction hash.  This allows transactions to be retrieved by address.

For each unique address involved in a transaction a new row is written to the AddressTransaction table. The following addresses are captured from a transaction.

+ From Address
+ To Address (if not empty)
+ Newly Created Contract Address
+ Any contract address from the transaction log (aka event log)

This means that inter contract calls can be tracked providing they emit events.  Let's say you called Contract A which internally calls Contract B.  If you retrieved this transaction you would not see the call to Contract B as it is neither the From or To address.  However if Contract B had emitted an event during your transaction then the address of Contract B would be captured from the logs in the transaction receipt and persisted in the AddressTransaction table.

One transaction for block, transaction hash and address:
``` csharp
var addressTransaction = await addressTransactionRepository.FindByAddressBlockNumberAndHashAsync(
    transaction.AddressFrom, 
    new HexBigInteger(BigInteger.Parse(block.BlockNumber)), 
    transaction.Hash);
```

All transactions for address:
``` csharp
var addressTransactions = await addressTransactionRepository.GetManyAsync(address);
```

### Retrieving a contract
Contracts are persisted to the contract table each time a "contract creation" transaction is encountered.  (The processor won't retrospectively add contracts to this table).

``` csharp
var contract = await contractRepository.FindByAddressAsync(addressTransaction.NewContractAddress);
```

### Retrieving logs
Each log emitted by a transaction is persisted.  The event topics from the Blockchain are split into specific fields: EventHash, IndexedVal1, IndexedVal2, IndexedVal3.  This means that events can be identified as well as indexed parameters by their hash.  The "Data" is also stored which means the event can be fully decoded if necessary.
``` csharp
var logs = await transactionLogRepository.GetManyAsync(transaction.Hash);
```

#### Decoding a stored log into an Event.
This relies on a few extensions methods in Netherum core which are in a variety of namespaces. Ensure you have the required "using" statements from the full sample above.  It also relies on having a DTO to describe the event to decode.  In this example see "TransferEventDTO" in the full sample above.  

The log persisted in table storage is first converted to a FilterLog, which is a core Nethereum class for a transaction log.  That is then checked to see if the event signature matches our event. If it does match, the event is decoded from the log.  For instance, we can now obtain the transfer event parameter values (to, from and value).  
``` csharp
var filterLog = log.ToFilterLog();
if (filterLog.IsLogForEvent<TransferEventDTO>())
{
    var decodedEvent = filterLog.DecodeEvent<TransferEventDTO>();
    Console.WriteLine("TRANSFER:");
    Console.WriteLine(JsonConvert.SerializeObject(decodedEvent));
}
```

## Clearing all data!
If you wish to clear existing data and start again you can delete the tables in Azure storage.

``` csharp
// WARNING you can't undo this!!
await repoFactory.DeleteAllTables(); 
```
