# What is Nethereum ?

Nethereum is a .NET integration library for Ethereum, simplifying smart contract management and interaction with Ethereum nodes whether they are public, like [ Geth ](https://geth.ethereum.org/), [Parity](https://www.parity.io/) or private, like [Quorum](https://www.jpmorgan.com/global/Quorum) and [Besu](https://besu.hyperledger.org/en/stable/).

Nethereum is being developed targeting .NET Standard 1.1, .NET Framework 4.5.1, and also as a portable library, hence it is compatible with all major operating systems (Windows, Linux, macOS, Android, and iOS) and has been tested on cloud, mobile, desktop, Xbox, HoloLens and Windows IoT.

Upcoming releases will be Ethereum 2.0 compliant (when Ethereum 2.0 is released) and include functionalities such as [DevP2P](https://github.com/ethereum/devp2p), [Plasma](https://plasma.io/plasma.pdf) and Micro-Payments.

## Features

* JSON RPC / IPC Ethereum core methods.
* Geth management API (admin, personal, debugging, miner).
* [Parity](https://www.parity.io/) management API.
* [Quorum](nethereum-azure-quorum.md) integration.
* [Besu](https://besu.hyperledger.org/en/stable/).
* Simplified smart contract interaction for deployment, function calling, transaction and event filtering and decoding of topics.
* [Unity 3D](unity3d-introduction.md) Unity integration.
* [Blockchain processing](nethereum-block-processing-detail.md).  
* ABI to .NET type encoding and decoding, including attribute-based for complex object deserialisation (nethereum-abi-encoding.md).
* [Hd Wallet](nethereum-managing-hdwallets.md) creation and management.
* [Rules engine](wonka.md).
* [HD Wallet integration](nethereum-managing-hdwallets.md).
* Transaction, RLP and message signing, verification and recovery of accounts.
* Libraries for standard contracts Token, [ENS](https://ens.domains/) and [Uport](https://www.uport.me/)
* Integrated TestRPC testing to simplify TDD and BDD (SpecFlow) development.
* Key storage using Web3 storage standard, compatible with Geth and Parity.
* Simplified account life cycle for both managed by third party client (personal) or stand alone (signed transactions).
* Low level Interception of RPC calls.
* Code generation of smart contracts services.
