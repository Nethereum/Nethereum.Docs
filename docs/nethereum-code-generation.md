# Nethereum Code Generation

Nethereum offers a code generator which allows you to generate .Net classes (C#, Vb.Net and F#) from the compilation output of smart contracts (ABI and Bin).

The core and first code generators output the .Net contract definitions and services to simplify and speed up the development to interact with Ethereum smart contracts using Nethereum. Our roadmap is to be able to generate User interfaces, view models and cloud services.

Nethereum provides different tooling based on the same code generation.

* Web based code generation: 
 
 	The Web based code generation [http://codegen.nethereum.com](http://codegen.nethereum.com/) is a simple online tool, to code generate a smart contract definition without the need to install any tools. Just input your Abi, Bytecode, Smart contract name and Namespace. [Source code](https://github.com/Nethereum/Nethereum.CodeGen.Blazor)

* VsCode Solidity extension integrated code generation: 
	
	The [vs code solidity extension](https://marketplace.visualstudio.com/items?itemName=JuanBlanco.solidity) can code generate your contract defintions automatically after compilation of a smart contract, and for any existing smart contract or all in the current solidity project workspace. [More info..](nethereum-codegen-vscodesolidity.md)
	
* Nethereum Autogen Nuget
	The [Nethereum.Autogen.ContractApi](https://www.nuget.org/packages/Nethereum.Autogen.ContractApi/) is a nuget package that automatically generates your code when building your project, just save your contract abi and bin files at the root of your project.
	[More info..](nethereum.autogen.contractapi.md)
	
* Nethereum Generator Console: https://www.nuget.org/packages/Nethereum.Generator.Console/
	You can install the Nethereum cli globally by simply typing ```dotnet tool install -g Nethereum.Generator.Console```. 
	[More info..](nethereum-codegen-console.md)


To integrate the generators in your own solution using the Netheruem nugets and npm packages.

* Nuget packages: https://www.nuget.org/packages/Nethereum.Generators/
* Npm packages: https://www.npmjs.com/package/nethereum-codegen


### Interacting with the generated code

The code below uses the generated code to deploy a standard contract to a test chain and invoke its Transfer function.
(To run the code you need to ensure you have a test chain/node running and that you provide valid account addresses and passwords)

``` csharp
using System;
using System.Numerics;
using System.Threading.Tasks;
using MyStandardContractProject.StandardContract.CQS;
using MyStandardContractProject.StandardContract.Service;
using Nethereum.Hex.HexTypes;
using Nethereum.Web3;
using Nethereum.Web3.Accounts;
using Nethereum.Web3.Accounts.Managed;

namespace MyStandardContractProject
{
    public class Sample
    {
        public async Task DeployAndCall()
        {
            var account = new ManagedAccount("0x12890d2cce102216644c59dae5baed380d84830c", "password");
            var web3 = new Web3(account, "http://localhost:8545");

            var deployment = new StandardContractDeployment
            {
                InitialAmount = new HexBigInteger(100),
                TokenName = "Test",
                DecimalUnits = 0,
                TokenSymbol = "T"
            };

            var svc =
                await StandardContractService.DeployContractAndGetServiceAsync(web3, deployment);

            var receipt = await svc.TransferRequestAndWaitForReceiptAsync(new TransferFunction
            {
                To = "0x13f022d72158410433cbd66f5dd8bf6d2d129924",
                Value = new BigInteger(1)
            });

            if (receipt.Status.Value == 0)
                throw new Exception("Failure - status should equal 1");
        }
    }
}
```
