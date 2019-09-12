# Subscriptions and Streaming 

Nethereum has support for both subscriptions (aka pub-sub) and streaming using Reactive extensions (observables).  They are mechanisms to receive changes occuring on the Blockchain which do not require you to write any polling code.

## Subscriptions
Geth and Parity subscriptions are supported. 

### **Geth** (from Geth docs):
> From version 1.4 geth has **experimental** support for pub/sub using subscriptions as defined in the JSON-RPC 2.0 specification. This allows clients to wait for events instead of polling for them.

Geth "pub-sub" Documentation
https://geth.ethereum.org/developers/RPC-PUB-SUB

Geth currently supports these subscriptions: "newHeads", "logs", "newPendingTransactions" and "syncing".

### **Parity**  (from Parity docs):
> Starts a subscription (on WebSockets / IPC / TCP transports) to results of calling some other RPC method. For every change in returned value of that RPC call a JSON-RPC notification with result and subscription ID will be sent to a client.

Parity "pubsub" docs:
https://wiki.parity.io/JSONRPC-parity_pubsub-module.html

## Subscription Considerations

From the Geth documentation - but most of it applies to Parity as well:

   > 1. notifications are send for current events and not for past events. If your use case requires you not to miss any notifications than subscriptions are probably not the best option.
   > 2. subscriptions require a full duplex connection. Geth offers such connections in the form of websockets (enable with –ws) and ipc (enabled by default).
   > 3. subscriptions are coupled to a connection. If the connection is closed all subscriptions that are created over this connection are removed.
   > 4. notifications are stored in an internal buffer and sent from this buffer to the client. If the client is unable to keep up and the number of buffered notifications reaches a limit (currently 10k) the connection is closed. Keep in mind that subscribing to some events can cause a flood of notifications, e.g. listening for all logs/blocks when the node starts to synchronize.

## Streaming Considerations

Much the same as subscription in practice.  

**Warning**
As of Nethereum v3.4.0 subscriptions and streaming are not compatible with Blazor.  This is because Blazor does yet not support Reactive and Websockets.

### Other Options:
Where subscriptions and streaming are not suitable, Nethereum provides these alternatives.
 * (Log Processing)[nethereum-log-processing-detail.md]
 * (Block Processing)[nethereum-block-processing-detail.md]
 * "Roll-Your-Own" (e.g. your own polling mechanism) using Nethereum to retrieve the data.

## Example
Below is a sample of streaming and subscriptions.  The same sample is available in the repo: https://github.com/Nethereum/Nethereum/blob/master/src/Nethereum.WebSocketsStreamingTest/Program.cs

### Required Nuget Packages:
* Nethereum.JsonRpc.WebSocketClient
* Nethereum.RPC.Reactive
* Nethereum.Web3

``` csharp
using Nethereum.Contracts;
using Nethereum.JsonRpc.WebSocketStreamingClient;
using Nethereum.RPC.Eth.DTOs;
using System;
using System.Reactive.Linq;
using System.Threading;
using Nethereum.Contracts.Extensions;
using Nethereum.ABI.FunctionEncoding.Attributes;
using System.Numerics;
using Nethereum.JsonRpc.Client.Streaming;
using Nethereum.RPC.Eth.Subscriptions;
using Nethereum.RPC.Reactive.Eth;
using Nethereum.RPC.Reactive.Eth.Subscriptions;
using Nethereum.RPC.Reactive.Extensions;

namespace Nethereum.WebSocketsStreamingTest
{
    class Program
    {
        static void Main(string[] args)
        {
            var client = new StreamingWebSocketClient("wss://mainnet.infura.io/ws");

            // var client = new StreamingWebSocketClient("ws://127.0.0.1:8546");
            var blockHeaderSubscription = new EthNewBlockHeadersObservableSubscription(client);

            blockHeaderSubscription.GetSubscribeResponseAsObservable().Subscribe(subscriptionId =>
                Console.WriteLine("Block Header subscription Id: " + subscriptionId));

            blockHeaderSubscription.GetSubscriptionDataResponsesAsObservable().Subscribe(block =>
                Console.WriteLine("New Block: " + block.BlockHash));

            blockHeaderSubscription.GetUnsubscribeResponseAsObservable().Subscribe(response =>
                            Console.WriteLine("Block Header unsubscribe result: " + response));


            var blockHeaderSubscription2 = new EthNewBlockHeadersSubscription(client);
            blockHeaderSubscription2.SubscriptionDataResponse += (object sender, StreamingEventArgs<Block> e) =>
            {
                Console.WriteLine("New Block from event: " + e.Response.BlockHash);
            };

            blockHeaderSubscription2.GetDataObservable().Subscribe(x =>
                 Console.WriteLine("New Block from observable from event : " + x.BlockHash)
                );

            var pendingTransactionsSubscription = new EthNewPendingTransactionObservableSubscription(client);

            pendingTransactionsSubscription.GetSubscribeResponseAsObservable().Subscribe(subscriptionId =>
                Console.WriteLine("Pending transactions subscription Id: " + subscriptionId));

            pendingTransactionsSubscription.GetSubscriptionDataResponsesAsObservable().Subscribe(transactionHash =>
                Console.WriteLine("New Pending TransactionHash: " + transactionHash));

            pendingTransactionsSubscription.GetUnsubscribeResponseAsObservable().Subscribe(response =>
                            Console.WriteLine("Pending transactions unsubscribe result: " + response));


            var ethGetBalance = new EthGetBalanceObservableHandler(client);
            var subs = ethGetBalance.GetResponseAsObservable().Subscribe(balance =>
                            Console.WriteLine("Balance xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: " + balance.Value.ToString()));
           
            var ethBlockNumber = new EthBlockNumberObservableHandler(client);
            ethBlockNumber.GetResponseAsObservable().Subscribe(blockNumber =>
                                Console.WriteLine("Block number: bbbbbbbbbbbbbb" + blockNumber.Value.ToString()));


            var ethLogs = new EthLogsObservableSubscription(client);
            ethLogs.GetSubscriptionDataResponsesAsObservable().Subscribe(log =>
                Console.WriteLine("Log Address:" + log.Address));

            //no contract address

            var filterTransfers = Event<TransferEventDTO>.GetEventABI().CreateFilterInput();

            var ethLogsTokenTransfer = new EthLogsObservableSubscription(client);
            ethLogsTokenTransfer.GetSubscriptionDataResponsesAsObservable().Subscribe(log =>
            {
                try
                {
                    var decoded = Event<TransferEventDTO>.DecodeEvent(log);
                    if (decoded != null)
                    {
                        Console.WriteLine("Contract address: " + log.Address +  " Log Transfer from:" + decoded.Event.From);
                    }
                    else
                    {
                        Console.WriteLine("Found not standard transfer log");
                    }
                }
                catch (Exception ex){
                    Console.WriteLine("Log Address: "+ log.Address + " is not a standard transfer log:", ex.Message);
                }
            });

            

            client.StartAsync().Wait();

            blockHeaderSubscription.SubscribeAsync().Wait();

            blockHeaderSubscription2.SubscribeAsync().Wait();

            pendingTransactionsSubscription.SubscribeAsync().Wait();
            
            ethGetBalance.SendRequestAsync("0x742d35cc6634c0532925a3b844bc454e4438f44e", BlockParameter.CreateLatest()).Wait();

            ethBlockNumber.SendRequestAsync().Wait();

            ethLogs.SubscribeAsync().Wait();

            ethLogsTokenTransfer.SubscribeAsync(filterTransfers).Wait();

            Thread.Sleep(30000);
            pendingTransactionsSubscription.UnsubscribeAsync().Wait();

            Thread.Sleep(20000);

            blockHeaderSubscription.UnsubscribeAsync().Wait();

            Thread.Sleep(20000);
        }


        public partial class TransferEventDTO : TransferEventDTOBase { }

        [Event("Transfer")]
        public class TransferEventDTOBase : IEventDTO
        {
            [Parameter("address", "_from", 1, true)]
            public virtual string From { get; set; }
            [Parameter("address", "_to", 2, true)]
            public virtual string To { get; set; }
            [Parameter("uint256", "_value", 3, false)]
            public virtual BigInteger Value { get; set; }
        }


    }
}
```

## Source Code Links

* https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.JsonRpc.WebSocketStreamingClient
* https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.RPC.Reactive
* https://github.com/Nethereum/Nethereum/tree/master/src/Nethereum.Parity.Reactive
