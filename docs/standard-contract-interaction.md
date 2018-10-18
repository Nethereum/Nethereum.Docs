# Standard Contract Interaction

## ERC20 / EIP20

The snippet below demonstrates deployment and interaction with a standard ERC20 / EIP20 contract.  

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

#### Using a service
The service provides a one-stop shop for interaction with a contract.  Something similar to the proxy which a web reference provides for a web service.  

Methods are provided for initial deployment and for querying contract state and invoking transactions.

There are code generators to generate services for other bespoke contracts.  The code generators read the contract ABI (application binary interface) and generate functions to interact with the contract.  Code generation means you don't waste time writing boiler plate code and also helps to prevent mistakes.  [Code Gen Docs](nethereum-code-generation.md)

``` csharp
        public static async Task ERC20_Deploy_And_Interact()
        {
            var account = new ManagedAccount("0x12890d2cce102216644c59daE5baed380d84830c", "password");
            var web3 = new Web3(account);
     
            const ulong totalSupply = 1000000;
            const string newAddress = "0x13f022d72158410433cbd66f5dd8bf6d2d129924";

            var deploymentContract = new EIP20Deployment()
            {
                InitialAmount = totalSupply,
                TokenName = "TestToken",
                TokenSymbol = "TST"
            };

            var tokenService = await StandardTokenService.DeployContractAndGetServiceAsync(web3, deploymentContract);
            
            var transfersEvent = tokenService.GetTransferEvent();

            var totalSupplyDeployed = await tokenService.TotalSupplyQueryAsync();
            Console.WriteLine($"Total Supply Deployed: {totalSupplyDeployed}");
           
            var ownerBalance = await tokenService.GetBalanceOfAsync<BigInteger>(account.Address);
            Console.WriteLine($"Owner Balance: {ownerBalance}");

            var newAddressBalance = await tokenService.GetBalanceOfAsync<BigInteger>(newAddress);
            Console.WriteLine($"New Address Balance: {newAddressBalance}");

            var transferFunction = new TransferFunction
            {
                To = newAddress,
                Value = 1000
            };

            var transferReceipt =
                await tokenService.TransferAndWaitForReceiptAsync(transferFunction);

            if (transferReceipt.Status.Value != 1)
            {
                Console.WriteLine($"Transfer failed - expected Status to equal 1 but was {transferReceipt.Status.Value}.");
                return;
            }

            ownerBalance = await tokenService.GetBalanceOfAsync<BigInteger>(account.Address);
            Console.WriteLine($"Owner Balance: {ownerBalance}");

            newAddressBalance = await tokenService.GetBalanceOfAsync<BigInteger>(newAddress);
            Console.WriteLine($"New Address Balance: {newAddressBalance}");

            var allTransfersFilter =
                await transfersEvent.CreateFilterAsync(new BlockParameter(transferReceipt.BlockNumber));

            var eventLogsAll = await transfersEvent.GetAllChanges<TransferEventDTO>(allTransfersFilter);

            var transferLog = eventLogsAll.First();
            Console.WriteLine($"Tx Index: {transferLog.Log.TransactionIndex.HexValue}");
            Console.WriteLine($"Tx BlockNumber: {transferLog.Log.BlockNumber.HexValue}");
            Console.WriteLine($"Tx Event To: {transferLog.Event.To.ToLower()}");
            Console.WriteLine($"Tx Event Value: {transferLog.Event.Value}");
        }
```

#### Using contract handlers

You can use contract handlers to interact with the contract and bypass the service layer.

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