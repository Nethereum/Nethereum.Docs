# Standard Contract Interaction

## ERC20 / EIP20

The snippet below demonstrates deploying and querying a standard ERC20 / EIP20 contract.

### Pre Requisites

The sample requires a pre configured test chain.  Nethereum provides a test chain.  

#### Downloading and running the Nethereum Test Chain
[Clone](https://github.com/Nethereum/Nethereum.git) the Nethereum repo and go to directory (testchain/clique/) OR [download individual files](https://github.com/Nethereum/Nethereum/tree/master/testchain/clique).

The account address and password are hard coded in this sample and are specific to the Nethereum test chain setup.

 - Run startgeth.bat (windows) or startgeth.sh (linux, mac)
 
 ### Running the sample
 - Ensure the test chain is running
 - Create a new project
 - Add Nethereum.StandardTokenEIP20 nuget package  (example uses 3.0.0-rc1)
 - Call the function below

``` csharp
        public static async Task ERC20_Deploy_And_Query()
        {
            var account = new ManagedAccount("0x12890d2cce102216644c59daE5baed380d84830c", "password");
            var web3 = new Web3(account);
            var deploymentHandler =  web3.Eth.GetContractDeploymentHandler<EIP20Deployment>();
            
            var receipt = await deploymentHandler.SendRequestAndWaitForReceiptAsync(new EIP20Deployment()
            {
                DecimalUnits = 18,
                InitialAmount = BigInteger.Parse("10000000000000000000000000"),
                TokenSymbol = "XST",
                TokenName = "XomeStandardToken"
            });

            var contractHandler = web3.Eth.GetContractHandler(receipt.ContractAddress);

            var symbol = await contractHandler.QueryAsync<SymbolFunction, string>();
            var token = await contractHandler.QueryAsync<NameFunction, string>();
            
            Console.WriteLine($"Symbol: {symbol}");
            Console.WriteLine($"Token: {token}");
        }
```