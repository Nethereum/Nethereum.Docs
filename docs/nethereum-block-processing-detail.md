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

 Nethereum has all you need to retrieve data from the Blockchain.  Processing is simply a layer on top.  If you have one-off retrieval requirements these are easy to use (e.g. ``` web3.Eth.Blocks  ```,  ``` web3.Eth.Transactions ``` , ``` web3.Eth.Filters ```).  To get started, here's the docs: http://docs.nethereum.com/en/latest/getting-started/.

## Too impatient to read further!? Show me the SAMPLES!
There are several varied samples in the Netherum playground: http://playground.nethereum.com/.

## What's a Block Processor?
It is an orchestrator that co-ordinates retrieving blocks, transactions and logs, applying criteria and invoking the code you plug in.  It minimises the boiler plate code you need to write.  It helps you to filter the data you require and can automatically decode it if necessary.  It takes care of progress tracking so you gain "restartability"!   It has some inbuilt retry logic to cope with connectivity errors during log retrieval.

### Actions (sync and async)
The processor allows you to plug in actions which can be synchronous or async.  This is where you put the code to handle the matching data. Async actions are ideal for writing to async API's which are common when integrating with external systems and persistence stores. Synchronous actions are great for performance when you don't need async calls.

### Criteria (sync and async)
You can implement criteria which can be synchronous or async.  Criteria dictates whether or not your action is invoked. Async criteria allows you to do dynamic lookups which may involve external calls to registries/databases/web services etc.  For instance, whilst processing you may need to check dynamic registries as part of your criteria and naturally these calls tend to be async.  Synchronous criteria allows you to inject in-memory criteria easily.

### ProcessorHandler
Under the hood - the actions and criteria are loaded into a ProcessorHandler for you.  If you prefer not to use actions and criteria in the form of Lambda's you can inject your own instances of a ProcessorHandler.  The ProcessHandler approach allows you to use your choice of DI framework to build these handlers. 

## Creating a Block Processor
In this example, let's say we want to sequentially retrieve any log for any contract address from the Blockchain.  It could represent some global and generic log monitoring tool.

You'll need the core Nethereum nuget: **Nethereum.Web3**

