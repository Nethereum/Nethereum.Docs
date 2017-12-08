## How to use Nethereum's Console generator

Nethereum offers a code generator that translates Solidity contracts into CS file, allowing interactions with the blockchain from a C# application.

Here's how to do it:

You will need: 

* [vs code (windows/Linux or Mac)](https://code.visualstudio.com/) 
* [Nethereum's Solidity extension](https://github.com/juanfranblanco/vscode-solidity/)
* A solidity contract [( take it from here if you didn't write one yet )](http://solidity.readthedocs.io/en/develop/solidity-by-example.html)

### Step 1:

In vs code, open the command palette with ``` Ctrl+Shift+P ```. then type "solidity" and select "compile current Solidity contract".
![Convert Solidity code to Json](screenshots/how-to-use-console-generator1.gif)

You should now see a newly generated ``` bin ``` folder containing three generated files.

### Step 2:

Select the Json files contained in ``` bin ```, then open the command palette, type solidity and select ``` code generate from compilation output 'YourFile.json'```


![Convert Json file to CS](screenshots/how-to-use-console-generator2.gif)

You're done :)