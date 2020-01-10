#IPC

Nethereum provides an IPC client to communicate with other Ethereum clients. IPC communication behaves in the same way as RPC / HTTP, the only change is the Client implementation.

First you will need to install the ``` Nethereum.JsonRpc.IpcClient ``` nuget. 

There are two types of IPC Clients, Windows which uses NamedPipes and Unix/Linux.

## Windows environment

In Windows we need to use the ```Nethereum.JsonRpc.IpcClient.IpcClient```. The new IpcClient will be configured with the NamedPipes file name. Geth uses as default `geth.ipc` and Parity `jsonrpc.ipc`.

```csharp
var client = Nethereum.JsonRpc.IpcClient.IpcClient("jsonrpc.ipc");
```

## Unix environment

In Unix / Linux we need to use the ```Nethereum.JsonRpc.IpcClient.UnixIpcClient```. The new IpcClient will be configured with the full file path of the IPC file. In this scenario, because we have configured the Geth path `devChain`, the file will be found in the root directory.

```csharp
var client = Nethereum.JsonRpc.IpcClient.UnixIpcClient("/Users/juanblanco/Documents/Repos/Nethereum.Workbooks/testchain/clique/devChain/geth.ipc");
```
## Creating a Web3 instance

Finally, we can create an instance of Web3 using the new IPC Client.

```csharp
var web3 = new Nethereum.Web3.Web3(client);
```

