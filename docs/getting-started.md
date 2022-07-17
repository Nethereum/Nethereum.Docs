# Getting Started with Nethereum

 This is a quick start sample with minimal dependencies. It is meant to help new and seasoned .Net developers.

This will take you through the steps of connecting to Infura and retrieving the balance of an account from the mainnet (the public Ethereum chain). 

Infura provides a set of public nodes removing the need to have a local or maintained client fully synchronized with the main Ethereum network.

!!! note
    You can find an executable code sample about the same topic on the Nethereum Playground:
    [Query Ether account balance using Infura](http://playground.nethereum.com/csharp/id/1001)


## 1. Install .Net

Nethereum works with .Net Core or .Net Framework (from 4.5.1 upwards). You'll need to have the .Net SDK installed. For new starters we recommend .Net core. Mac or Linux users will also need .Net Core. 

Not sure which .Net SDK to download? - choose .Net Core 3.1.

[Download .Net SDK](https://www.microsoft.com/net/download)

## 2. Create your app

Create a project using the .Net CLI (below) OR create a project in Visual Studio.

``` sh
dotnet new console -o NethereumSample
cd NethereumSample
```

## 3. Add package reference to Nethereum.Web3 and restore (update / download) the project packages.

``` sh
dotnet add package Nethereum.Web3
dotnet restore
```

## 4. Open your IDE (VS Code, Visual Studio etc)

Visual Studio Code or Visual Studio are both good choices for .Net development. Other good IDE's are also available (Jet Brains Rider for instance).
Nethereum's playground can help you get started immediately with no setup, yet, just be aware that it's not a full-fledged IDE http://playground.nethereum.com/

Now, open the Program.cs file in the editor.
If Visual Studio Code prompts you to add additional extensions, click 'Yes'.

## 5. Code to retrieve account balance

Full sample code for Program.cs.  See below for a fuller explanation of each step.
``` c#
using System;
using System.Threading.Tasks;
using Nethereum.Web3;

namespace NethereumSample
{
    class Program
    {
        static void Main(string[] args)
        {
            GetAccountBalance().Wait();
            Console.ReadLine();
        }

        static async Task GetAccountBalance()
        {
var web3 = new Web3("https://mainnet.infura.io/v3/7238211010344719ad14a89db874158c");
            var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
            Console.WriteLine($"Balance in Wei: {balance.Value}");

            var etherAmount = Web3.Convert.FromWei(balance.Value);
            Console.WriteLine($"Balance in Ether: {etherAmount}");
        }
    }
}
```

First, we need to add our required namespaces for Nethereum:

``` c#
using Nethereum.Web3;
```

The next step is to create an instance of Web3, with the infura url for mainnet and your INFURA api key with the format:`https://<network>.infura.io/v3/YOUR-PROJECT-ID`.

For this sample, we’ll use a special API key `7238211010344719ad14a89db874158c`, but for your own project you’ll need to [sign up on INFURA](https://infura.io/register) and generate your own key.

``` c#
var web3 = new Web3("https://mainnet.infura.io/v3/7238211010344719ad14a89db874158c");
```

Using the Eth API we can execute the GetBalance request asynchronously, for our selected account. In this scenario I have chosen the Ethereum Foundation account. “0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae”

``` c#
var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
```

The amount returned is in Wei, the lowest unit of value. We can convert this unit to Ether using the Convertion utility:

``` c#
var etherAmount = Web3.Convert.FromWei(balance.Value);
```

!!! note
    You can find executable code samples to experiment further on the Nethereum Playground, some examples: 
    - [Smart Contracts: Smart Contracts Deployment, Querying, Transactions, Nonces, Estimating Gas, Gas Price](http://playground.nethereum.com/csharp/id/1007)
    - [Chain information: Query Ether account balance using Infura](http://playground.nethereum.com/csharp/id/1001)
    - [Generating mnemonics for HdWallets](http://playground.nethereum.com/csharp/id/1042)
    - [Azure Blockchain Service: Interacting with a Quorum member node](http://playground.nethereum.com/csharp/id/1046)
