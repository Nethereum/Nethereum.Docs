# Getting Started with Nethereum

This is a quick start sample for new and existing .Net developers with minimal dependencies.

This will take you through the steps of connecting to Infura and retrieve the balance of an account from the mainnet (live Ethereum). 

Infura provides a set of public nodes removing the need to have a local or maintained client fully synchronised with the main Ethereum network.

## 1. Install .Net

Nethereum works with .Net Core or .Net Framework (from 4.5.1 upwards).  You'll need to have the .Net SDK installed.  For new starters we recommend .Net core.  Mac or Linux users will also need .Net Core.  

Not sure which .Net SDK to download? - choose .Net Core 2.1.

[Download .Net SDK](https://www.microsoft.com/net/download)

## 2. Create your app

Create a project using the .Net CLI (below) OR create a project in Visual Studio.
``` sh
dotnet new console -o NethereumSample
cd NethereumSample
```

## 3. Add package reference to Nethereum.Web3

``` sh
dotnet add package Nethereum.Web3
```

## 4. Open your IDE (VS Code, Visual Studio etc)

Visual Studio Code or Visual Studio are both good choices for .Net development.  Other good IDE's are also available (Jet Brains Rider etc).

Open the Program.cs file in the editor.

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
            var task = Task.Run(async () =>
            {
                var web3 = new Web3("https://mainnet.infura.io");

                var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
                Console.WriteLine($"Balance in Wei: {balance.Value}");

                var etherAmount = Web3.Convert.FromWei(balance.Value);
                Console.WriteLine($"Balance in Ether: {etherAmount}");

                Console.ReadLine();
            });

            task.Wait();
        }
    }
}
```

First, we need to add our required namespaces for Nethereum:

``` c#
using Nethereum.Web3;
```

The next step is to create an instance of Web3, with the infura url for mainnet.

``` c#
var web3 = new Web3("https://mainnet.infura.io");
```

Using the Eth API we can execute the GetBalance request asynchronously, for our selected account. In this scenario I have chosen the Ethereum Foundation account. “0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae”

``` c#
var balance = await web3.Eth.GetBalance.SendRequestAsync("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae");
```

The amount returned is in Wei, the lowest unit of value. We can convert this to Ether using the Convertion utility:

``` c#
var etherAmount = Web3.Convert.FromWei(balance.Value);
```

