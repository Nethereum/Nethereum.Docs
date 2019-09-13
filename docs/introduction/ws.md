# WS

Nethereum provides websocket clients.  They can be used instead of the default HTTP channel and to support subscriptions.

## Websocket Clients

Typically, once established, a connection is maintained by the websocket client. This is both for performance reasons and also to support streaming subscriptions.  The connection is closed on disposal of the client.

There are two main Websocket clients provided by Nethereum.

## WebSocketClient

**Related Nuget Packages:**

+ Nethereum.JsonRpc.WebSocketClient
+ Nethereum.Web3

Full Name: Nethereum.JsonRpc.WebSocketClient.WebSocketClient

An instance of this can be be injected into a normal web3 object. Therefore it can be used in place of the default HTTP based client for all node based communication.  It maintains an open web socket connection until it is disposed.

### Creating and using a WebSocketClient

Retrieving the current block number:
``` csharp
using Nethereum.JsonRpc.WebSocketClient;
using Nethereum.Web3;
using Nethereum.Web3.Accounts.Managed;
using System;
using System.Threading.Tasks;

namespace NethereumSocketsAndStreaming
{
    public class WS
    {
        public static async Task GetBlockNumberViaWebSocketAsync()
        {
            var account = new ManagedAccount("0x12890d2cce102216644c59daE5baed380d84830c", "password");
            using(var clientws = new WebSocketClient("wss://rinkeby.infura.io/ws"))
            { 
                var web3ws = new Web3(account, clientws);
                var blockNumber = await web3ws.Eth.Blocks.GetBlockNumber.SendRequestAsync(); //task cancelled exception
                Console.WriteLine("Block Number: " + blockNumber);
            }
        }
    }
}

```

## StreamingWebSocketClient

**Related Nuget Packages:**

+ Nethereum.JsonRpc.WebSocketClient
+ Nethereum.RPC.Reactive
+ Nethereum.Parity.Reactive
+ Nethereum.Web3

Full Name: Nethereum.JsonRpc.WebSocketStreamingClient

This is used to create subscriptions over a websocket connection. It keeps the connection open until disposed.  Subscriptions are only active whilst the connection is open.  

Subscriptions are available in these nuget packages:
* Nethereum.RPC.Reactive
* Nethereum.Parity.Reactive

### Subscription Documentation
See [subscription docs](../nethereum-subscriptions-streaming.md) for more detail and examples.

### Creating and using a StreamingWebSocketClient

Creating a NewBlockHeader subscription:
``` csharp
using Nethereum.JsonRpc.WebSocketStreamingClient;
using Nethereum.RPC.Reactive.Eth.Subscriptions;
using Newtonsoft.Json;
using System;
using System.Reactive.Linq;
using System.Threading.Tasks;

namespace Nethereum.WebSocketsStreamingTest
{
    public class BlockHeader
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
    }
}

```