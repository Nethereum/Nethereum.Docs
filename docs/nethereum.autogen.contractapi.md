# Nethereum.Autogen.ContractApi Nuget Package

## A quick path to Dotnet and Ethereum integration

Nethereum offers a code generator which allows you to generates dotnet classes from the ABI and Bin output of the compilation of Solidity contracts.  This generator has a range of front end options (CLI, windows, web, mobile etc).  The Nethereum.Autogen.ContractApi package incorporates the generator and provides the quickest path to Dotnet and Ethereum integration. Once the package is added to a project, C#, Vb or F# files will be generated during pre-build of the target project based on any solidity files (ABI, Bin) present in th0123456e project (or optionally based on a config file). These code files provide a basis for deploying and interacting with smart contracts.

The Nuget package attaches a build targets file to the project, which injects a pre-build task during which the code generation occurs. 

## Prerequisites: 

* [Visual Studio Code (windows/Linux or Mac)](https://code.visualstudio.com/) or Visual Studio.
* Dotnet Core 2.1 must be installed on the machine. The code generator runs on Dotnet Core 2.1, BUT your target project does not need to be a Dotnet core project.  [(Download Dotnet Core)](https://www.microsoft.com/net/download/windows)
* The ABI and bin files from one or more compiled Solidity contracts. [(Solidity contract examples)](http://solidity.readthedocs.io/en/develop/solidity-by-example.html)

## Instructions

### Step 1 - Create the target project:

Create a project In your IDE (Visual Studio or VS Code) - or using the Dotnet CLI.  You can use an existing project if desired.

### Step 2 - Create a folder for your Solidity ABI and Bin files:

Create a sub folder for your Solidity files (ABI, Bin). This is optional - they can be at the root of the project or in any sub folder of the project. By default, the root project and all sub folders will be scanned for ABI files.

If you prefer to have the solidity files in a folder which is not within the project, you will need to create a `Nethereum.Generator.json` file at the root of your project. If this file is present, then only ABI files referenced in that file will be code generated.  See [Config Driven Generation](#config-driven-generation) for more information.

### Step 3 - Put your ABI and bin files in the folder:

Put copies of your ABI and bin files in the sub folder (bin files should have the same name as ABI e.g. StandardContract.ABI, StandardContract.bin).

### Step 4 - Add Nethereum.Web3 nuget package:

Add `Nethereum.Web3` nuget (3.1.2 is the current version at the time of writing).

Nuget Console Command
```
Install-Package Nethereum.Web3
```

### Step 5 - Add Nethereum.Autogen.ContractApi.CSharp package:

Add `Nethereum.Autogen.ContractApi` nuget

Nuget Console Command
```
Install-Package Nethereum.Autogen.ContractApi
```

### Step 6 - Build the project:

Build the project. You should see a folder created in the project for each ABI file. For Dotnet Core projects this will be obvious in the IDE as the files will be visible in the project, for .Net Framework v4.* projects, check the project folder in the file system.

## Disabling code generation

If code generation on every build is not required, it can be disabled.
The code generation can be bypassed by adding the below property to the csproj file. The property is not there by default.  Once code generation is stopped the reference to the Nethereum.ABI.Autogen package can be dropped, but if any generated C# files exist, the reference to Nethereum.Web3 must remain.

``` xml
  <PropertyGroup>
  <!-- Set to false to disable code generation -->
    <NethereumGenerateCode>true</NethereumGenerateCode>
  </PropertyGroup>
```
## Gotchas

* Project Names with unusual characters.  ABI Autogen relies on a convention-based approach to naming. It will generated classes and namespaces based on the project name and solidity ABI file names.  Be aware of the fact that these can create a problem when building. Particularly where the names contain special characters or clash with other parts of your code base. When build issues can arise due to this, and the simplest approach is to rename the project and project folder and perhaps the solidity files. However if more control is required - See [Config Driven Generation](#config-driven-generation).
* For Dotnet Core projects - code generated files will automatically be included as part of the target project.  For Framework v4.* projects, the code generated files will be placed in the project folder but will not automatically be included in the project - they must be manually added to the project after generation.

## Config Driven Generation

Where more control is required over code generation - or where your ABI files are located outside of the project you can switch to a config file based approach.

Create a json file called "Nethereum.Generator.json" in the root of the project. The contents of this file will then control code generation.

Be aware that if a config file is present - ONLY ABI files in the config will be generated, the project will not be scanned for other ABI files.  Each ABI file would require it's own configuration - global configuration across multiple ABI's is not supported. Paths can be project relative or absolute.

``` json
{
	"ABIConfigurations": [
	{
		"ContractName":"StandardContractA",
		"ABI":null,
		"ABIFile":"Ballot.ABI",
		"ByteCode":null,
		"BinFile":"Ballot.bin",
		"BaseNamespace":null,
		"CQSNamespace":null,
		"DTONamespace":null,
		"ServiceNamespace":null,
		"CodeGenLanguage":"CSharp",
		"BaseOutputPath":null}
	]
}
```
### Configuration Info
* ABI - the actual ABI content (optional)
* ABIFile - the path (relative or absolute) to the ABI file (optional)
* Either ABI or ABI File must be specified
* ByteCode - the actual ByteCode (optional)
* BinFile - the path (relative or absolute) to the bin file (optional)
* Both ByteCode and BinFile are optional
* CodeGenLanguages: CSharp,Vb,FSharp (CSharp is default)

## Alternatives for Code Generation

The Nethereum.Autogen.ContractApi.CSharp package uses the Nethereum.Generator.Console under the hood. It is possible to use this in isolation.  

[Nethereum Generator Console](https://github.com/Nethereum/Nethereum.Docs/edit/master/docs/nethereum-code-generation.md)
