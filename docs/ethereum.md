#What is Ethereum?

Ethereum is a blockchain-based distributed computing platform featuring [smart contract](/docs/Ethereum-glossary-for-newbies/smart-contracts.md) functionality.
It provides a decentralized Turing-complete virtual machine, which can execute scripts using an international network of public nodes. Ethereum also provides a cryptocurrency token called "Ether", which can be transferred between accounts and used to compensate participant nodes for computations performed. "Gas", an internal transaction pricing mechanism, is used to mitigate spam and allocate resources on the network.

##Blockchain

A blockchain is a distributed ledger composed of records (blocks) , which are linked and secured using cryptography.  By design, blockchains are inherently resistant to modification: once recorded, the data in any written block can't be changed  without the changing all subsequent blocks, which requires a collusion of the network majority. A blockchain can serve as "an open, distributed ledger that can record transactions between two parties efficiently and in a verifiable and permanent way. Blockchains are managed by a peer-to-peer network collectively adhering to a protocol for validating new blocks.

##Blocks
Blocks are records containing transaction occuring on the blockchain.
Each block  contains a hash pointer as a link to a previous block, a timestamp and transaction data.

##Transactions
Transactions are the entities that change the state of the Ethereum blockchain.

In the Ethereum jargon, a “transaction” is a signed data package that stores a message to be sent from an externally owned account to another account on the blockchain.

A transactions contains:
* The recipient of the message
* A signature identifying the sender and proving their intention to send the message via the blockchain to the recipient
* a VALUE field: The amount of wei to transfer from the sender to the recipient
* An optional data field, which can contain the message sent to a contract
* A STARTGAS value, representing the total amount of gas a transaction can use
* A GASPRICE value, representing the fee the sender is willing to pay for gas (one unit of gas corresponds to the execution of one atomic instruction, i.e., a computational step).

##Accounts

See [What is an Ethereum account](/docs/Ethereum-glossary-for-newbies/account.md)

##Smart Contracts

See [What is a Smart Contract](/docs/Ethereum-glossary-for-newbies/smart-contracts.md)