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
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Contracts;
using Nethereum.JsonRpc.Client.Streaming;
using Nethereum.JsonRpc.WebSocketStreamingClient;
using Nethereum.RPC.Eth.DTOs;
using Nethereum.RPC.Eth.Subscriptions;
using Nethereum.RPC.Reactive.Eth.Subscriptions;
using Newtonsoft.Json;
using System;
using System.Numerics;
using System.Reactive.Linq;
using System.Threading.Tasks;

namespace Nethereum.WebSocketsStreamingTest
{
    public class Subscriptions
    {
        public static async Task NewBlockHeader_With_Observable_Subscription()
        {
            using(var client = new StreamingWebSocketClient("wss://rinkeby.infura.io/ws"))
            {
                // create the subscription
                // (it won't start receiving data until Subscribe is called)
                var subscription = new EthNewBlockHeadersObservableSubscription(client);

                // attach a handler for when the subscription is first created (optional)
                // this will occur once after Subscribe has been called
                subscription.GetSubscribeResponseAsObservable().Subscribe(subscriptionId =>
                    Console.WriteLine("Block Header subscription Id: " + subscriptionId));

                DateTime? lastBlockNotification = null;
                double secondsSinceLastBlock = 0;

                // attach a handler for each block
                // put your logic here
                subscription.GetSubscriptionDataResponsesAsObservable().Subscribe(block => 
                {
                    secondsSinceLastBlock = (lastBlockNotification == null) ? 0 : (int)DateTime.Now.Subtract(lastBlockNotification.Value).TotalSeconds;
                    lastBlockNotification = DateTime.Now;
                    var utcTimestamp = DateTimeOffset.FromUnixTimeSeconds((long)block.Timestamp.Value);
                    Console.WriteLine($"New Block. Number: {block.Number.Value}, Timestamp UTC: {JsonConvert.SerializeObject(utcTimestamp)}, Seconds since last block received: {secondsSinceLastBlock} ");
                });

                bool subscribed = true;

                // handle unsubscription
                // optional - but may be important depending on your use case
                subscription.GetUnsubscribeResponseAsObservable().Subscribe(response =>
                { 
                    subscribed = false;
                    Console.WriteLine("Block Header unsubscribe result: " + response);
                });

                // open the websocket connection
                await client.StartAsync();

                // start the subscription
                // this will only block long enough to register the subscription with the client
                // once running - it won't block whilst waiting for blocks
                // blocks will be delivered to our handler on another thread
                await subscription.SubscribeAsync();

                // run for a minute before unsubscribing
                await Task.Delay(TimeSpan.FromMinutes(1)); 

                // unsubscribe
                await subscription.UnsubscribeAsync();

                //allow time to unsubscribe
                while (subscribed) await Task.Delay(TimeSpan.FromSeconds(1));
            }
        }

        public static async Task NewBlockHeader_With_Subscription()
        {
            using(var client = new StreamingWebSocketClient("wss://mainnet.infura.io/ws"))
            { 
                // create a subscription 
                // it won't do anything just yet though
                var subscription = new EthNewBlockHeadersSubscription(client);

                // attach our handler for new block header data
                subscription.SubscriptionDataResponse += (object sender, StreamingEventArgs<Block> e) =>
                {
                    var utcTimestamp = DateTimeOffset.FromUnixTimeSeconds((long)e.Response.Timestamp.Value);
                    Console.WriteLine($"New Block: Number: {e.Response.Number.Value}, Timestamp: {JsonConvert.SerializeObject(utcTimestamp)}");
                };

                // open the web socket connection
                await client.StartAsync();

                // subscribe to new block headers
                // blocks will be received on another thread
                // therefore this doesn't block the current thread
                await subscription.SubscribeAsync();

                //allow some time before we close the connection and end the subscription
                await Task.Delay(TimeSpan.FromMinutes(1));

                // the connection closing will end the subscription
            }
        }

        public static async Task NewPendingTransactions()
        {
            using(var client = new StreamingWebSocketClient("wss://mainnet.infura.io/ws"))
            { 
                // create the subscription
                // it won't start receiving data until Subscribe is called on it
                var subscription = new EthNewPendingTransactionObservableSubscription(client);

                // attach a handler subscription created event (optional)
                // this will only occur once when Subscribe has been called
                subscription.GetSubscribeResponseAsObservable().Subscribe(subscriptionId =>
                    Console.WriteLine("Pending transactions subscription Id: " + subscriptionId));

                // attach a handler for each pending transaction
                // put your logic here
                subscription.GetSubscriptionDataResponsesAsObservable().Subscribe(transactionHash =>
                {     
                    Console.WriteLine("New Pending TransactionHash: " + transactionHash);
                });

                bool subscribed = true;

                //handle unsubscription
                //optional - but may be important depending on your use case
                subscription.GetUnsubscribeResponseAsObservable().Subscribe(response =>
                {
                    subscribed = false;
                    Console.WriteLine("Pending transactions unsubscribe result: " + response);
                });

                //open the websocket connection
                await client.StartAsync();

                // start listening for pending transactions
                // this will only block long enough to register the subscription with the client
                // it won't block whilst waiting for transactions
                // transactions will be delivered to our handlers on another thread
                await subscription.SubscribeAsync();

                // run for minute
                // transactions should appear on another thread
                await Task.Delay(TimeSpan.FromMinutes(1));

                // unsubscribe
                await subscription.UnsubscribeAsync();

                // wait for unsubscribe 
                while (subscribed) 
                { 
                    await Task.Delay(TimeSpan.FromSeconds(1));
                }
            }
        }

        public static async Task GetLogs_Observable_Subscription()
        {
            using(var client = new StreamingWebSocketClient("wss://mainnet.infura.io/ws"))
            { 
                // create the subscription
                // nothing will happen just yet though
                var subscription = new EthLogsObservableSubscription(client);

                // attach our handler for each log
                subscription.GetSubscriptionDataResponsesAsObservable().Subscribe(log =>
                    Console.WriteLine("Log Address:" + log.Address));

                // create the web socket connection
                await client.StartAsync();

                // begin receiving subscription data
                // data will be received on another thread
                await subscription.SubscribeAsync();

                // allow to run for a minute
                await Task.Delay(TimeSpan.FromMinutes(1));

                // unsubscribe
                await subscription.UnsubscribeAsync();

                // allow some time to unsubscribe
                await Task.Delay(TimeSpan.FromSeconds(5));
            }
        }

        public static async Task GetLogsTokenTransfer_Observable_Subscription()
        {
            // ** SEE THE TransferEventDTO class below **

            using(var client = new StreamingWebSocketClient("wss://mainnet.infura.io/ws"))
            { 
                // create a log filter specific to Transfers
                // this filter will match any Transfer (matching the signature) regardless of address
                var filterTransfers = Event<TransferEventDTO>.GetEventABI().CreateFilterInput();

                // create the subscription
                // it won't do anything yet
                var subscription = new EthLogsObservableSubscription(client);

                // attach a handler for Transfer event logs
                subscription.GetSubscriptionDataResponsesAsObservable().Subscribe(log =>
                {
                    try
                    {
                        // decode the log into a typed event log
                        var decoded = Event<TransferEventDTO>.DecodeEvent(log);
                        if (decoded != null)
                        {
                            Console.WriteLine("Contract address: " + log.Address + " Log Transfer from:" + decoded.Event.From);
                        }
                        else
                        {
                            // the log may be an event which does not match the event
                            // the name of the function may be the same
                            // but the indexed event parameters may differ which prevents decoding
                            Console.WriteLine("Found not standard transfer log");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("Log Address: " + log.Address + " is not a standard transfer log:", ex.Message);
                    }
                });

                // open the web socket connection
                await client.StartAsync();

                // begin receiving subscription data
                // data will be received on a background thread
                await subscription.SubscribeAsync(filterTransfers);

                // run for a while
                await Task.Delay(TimeSpan.FromMinutes(1));

                // unsubscribe
                await subscription.UnsubscribeAsync();

                // allow time to unsubscribe
                await Task.Delay(TimeSpan.FromSeconds(5));
            }
        }

        // This class describes the Transfer event
        // It allows untyped logs to be decoded into typed representations
        // This allows the event parameters to be decoded
        // It also provides a basis for creating filters which are used to retrieve matching logs 
        // It can be created by hand but often this class is code generated 
        // It is marked as partial to allow you to extend it without breaking everytime the code is regenerated
        // http://docs.nethereum.com/en/latest/Nethereum.Workbooks/docs/nethereum-events-gettingstarted/
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
