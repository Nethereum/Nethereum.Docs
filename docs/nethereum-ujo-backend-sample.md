# Ujo Nethereum backend reference architecture

This Backend Ethereum integration uses Nethereum, Blockchain Processing, Data Processing, Azure Search, Azure Table Storage, Queuing, Web jobs and Ipfs. The Ujo elements were deprecated due to a change on architecture direction, but this serves as an example reference architecture on smart contract data driven scenarios (permissioned chains, consortiums, sidechains, etc), and the integration with cloud components in Azure. 

The solution for this problem domain focuses on the performance needs required to monitor and process events and log changes of millions of smart contracts (ie artists or works) which are part of common registry. It becomes rather hard to create and maintain filter logs using the bloom filters for that huge amount of smart contracts, which will then be queued or injected interface implentation for further processing of the smart contract changes.

The backend solution is split in several parts:

## Common Components / Infrastructure 
The CCC layer or common infrastructure layer, this is the current reference architecture for Nethereums Blokchain Log Processing and Smart contract data processing.

### Blockchain Processing 

The blockchain processing component provides a pluggable infrastructure to monitor and process transactions, smart contracts changes on state and / or events (logs) raised.

For example, the continuous processing and monitoring of token transfers (Erc20) made by a specific address, or in a more complex scenario the monitoring and processing of all the transactions made by many token contracts (Erc20) registered in an exchange.
Processing can be of any type, storage of transaction history, indexing of data, data analytics, monitoring of payments, etc.

https://github.com/Nethereum/ujo-backend/tree/master/Consensys.Common/CCC.BlockchainProcessing

### Registry Processing, a common smart contract registry service
The registry processing component provides the components to monitor and backend processing of registration and unregistrations of addresses on a standard registration contract.

https://github.com/Nethereum/ujo-backend/tree/master/Consensys.Common/CCC.Contracts.Registry.Processing

### Data Processing, a common data processing layer 
The standard data processing component allows to monitor and backend processing all the data changed events of contracts which follow the standard.

#### Standard DataLog Processor
The StandardDataLogProcessor is an implementation of the ILogProcessor, allowing it to be plugged into the Blockchain Log Processor.
The log processor validates matching event logs and if contracts belong to the standard data registry.
#### IStandardDataProcessingService
Different implementations of the IStandardDataProcessingService can be configured / registered either by code or Queues. Current implementations stores the data in Azure Search for indexing, Azure Table Storage and Azure Sql.

https://github.com/Nethereum/ujo-backend/tree/master/Consensys.Common/CCC.Contracts.StandardData.Processing

## Other commmon services:

### IPFS image services 	
The IPFS image services provide a webjob queing processing to resize ipfs hosted images and republish them. https://github.com/Nethereum/ujo-backend/tree/master/Ipfs.Services

## Ujo / Music domain specific implementation including

### Azure search 

https://github.com/Nethereum/ujo-backend/tree/master/Ujo.Work/Ujo.Work.Search.Service

###	Azure Storage  

Library to store the blockchain in Azure Table Storage, which will allow specific Blockchain Services to retrieve its data, as opposed to having a direct dependency with geth. Partionkeys and rows are indexed in a way so that services can retrieve information specific for their contracts (or vice versa).

https://github.com/Nethereum/ujo-backend/tree/master/Ujo.Work/Ujo.Work.Storage

### Azure Sql 
https://github.com/Nethereum/ujo-backend/tree/master/Ujo.Work/Ujo.Repository

### Web job 

https://github.com/Nethereum/ujo-backend/tree/master/Ujo.Work/Ujo.WorkRegistry.WebJob

### Ethereum integration component

https://github.com/Nethereum/ujo-backend/tree/master/Ujo.Work/Ujo.Work.Services.Ethereum

# Road map and Future

* The generic blockchain processing and log processing have been hardened and simplified for usage in the Nethereum.BlockchainProcessing project.

* The Standard Data and Registry will be refactored in the near future to provide a basic smart contract data repository layer, with generic support also for all the cloud components like Search, Storage, Processing (Web jobs), Machine learning (ML.net) etc.

* All these components will be the basis for other specific domain solutions like Commerce or integrated with the Wonka Rule Engine.

