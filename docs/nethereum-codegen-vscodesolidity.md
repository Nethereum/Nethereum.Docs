# Code generation using the Visual Studio Code extension

Prerequisites: 

* [Visual Studio Code (windows/Linux or Mac)](https://code.visualstudio.com/) 
* [Solidity vscode extension](https://marketplace.visualstudio.com/items?itemName=JuanBlanco.solidity).
* A solidity smart contract [(like any of these)](http://solidity.readthedocs.io/en/develop/solidity-by-example.html)

## Automatic code generation and the Nethereum Code generation settings file
The simplest way is to automatically code generate your api, for this you need to create a file called "nethereum-gen.settings" at the root of your project, with the following contents.

This file can be also auto-generated for you if you press F1 and type 'Solidity Create 'nethereum-gen.settings'

```json
{
    "projectName": "Solidity.Samples",
    "namespace": "Solidity.Samples",
    "lang":0,
    "autoCodeGen":true,
    "projectPath": "../SoliditySamples"
}
```
"lang" indicates what language to generate the code, 0 = CSharp, 1 = Vb.Net and 3 = FSharp

The "projectName" and "namespace" settings will be also used for the manual code generation.

Use the "projectPath" to set the relative path of your .Net project, this allows to work in a "solution" mode so you can work as an both in Visual Studio Code and Visual Studio (Fat) with your .Net project, or two windows of vscode.

## Single smart contract manual code generation

## Step 1:

In visual studio code, open the command palette with ``` Ctrl+Shift+P ```. then type "solidity" and select "compile current Solidity contract".
![Convert Solidity code to Json](screenshots/how-to-use-console-generator1.gif)

You should now see a newly generated ``` bin ``` folder containing three generated files.

## Step 2 Single contract:

Select the Json files contained in ``` bin ```, then open the command palette, type solidity and select ``` Solidity: Code generate CSharp from compilation output "contract.json"```

If you work in Vb.Net or FSharp chose those instead.

![Convert Json file to CS](screenshots/code-generation-single-contract.gif)

## Step 3 Multiple contracts:

Open the command palette, type solidity and select ``` Solidity: Code generate CSharp project from all compiled files```

If you work in Vb.Net or FSharp chose those instead.

![Convert Json file to CS](screenshots/code-generation-mutltiple.contracts.gif)
