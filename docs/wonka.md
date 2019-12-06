# Wonka

A business rules engine (for both the .NET platform and the <a target="_blank" href="https://en.wikipedia.org/wiki/Ethereum">Ethereum</a> platform) that is inherently metadata-driven.  Once the rules are written into a markup language and are parsed/deserialized by the .NET form of the engine, these rules can then be serialized onto the blockchain using Nethereum, stored within a smart contract (i.e., the Ethereum version of the engine) built using the Solidity language.  Basically, after providing a number of rules and populating a record, a user can use Nethereum to submit the populated record for validation by the rules engine, whether it exists in .NET or the blockchain.

Repo: https://github.com/Nethereum/Wonka

## Features

* XML markup language for defining a RuleTree, a logical and hierarchical set of rules.  The functionality for these rules can be predefined or user-defined.  There are [multiple](https://github.com/Nethereum/Wonka/blob/master/WonkaSystem/WonkaSystem/TestData/SimpleAccountCheck.xml) [examples](https://github.com/Nethereum/Wonka/blob/master/WonkaSystem/WonkaSystem/TestData/VATCalculationExample.xml) of a RuleTree's markup within the project.
* .NET framework that will parse XML markup and assembly a RuleTree data structure.
* .NET rules engine that can apply a RuleTree to a provided record for various purposes (validation, value assignment, etc.).
* Ethereum (i.e., Solidity contract) rules engine that can apply a RuleTree to a provided record for various purposes.
* .NET layer that can serialize a RuleTree data structure to the Ethereum rules engine.
* Orchestration 'get' functionality in the Ethereum engine, where the engine can be directed to assemble a virtual record by pulling values from other contracts within the blockchain.
* Orchestration 'set' functionality in the Ethereum engine, where the engine can be directed to set values on other contracts within the blockchain.
* Custom Operator functionality in the Ethereum engine, where the engine can execute an user-defined rule by calling a function on another contract within the blockchain.
* Registry and Grove functionality, helping users to discover/reuse existing RuleTree instances and group them into collections.
* Export functionality, so that a RuleTree existing on the blockchain side can be extracted and then serialized into a legible form (like XML).


!!! note
    You have the possibility to run wonka directly in your browser
    by using Nethereum's playground at the following link:[Wonka Rule Engine Preview: Loading external rules and pre validation](http://playground.nethereum.com/csharp/id/1044)
