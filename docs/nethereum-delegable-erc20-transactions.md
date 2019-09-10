# Delegable ERC20 Transactions

All token transfers on the Ethereum network requires gas as fee for writing to the blockchain, thereby requiring some amount of ether to be loaded into an Ethereum address before any token transactions could take place. This creates a confusing UI (having to hold two assets on an address) and a higher barrier to entry (having to buy ethers first, which means having to go through the whole 9 yards of registering on an exchange, going through KYC, etc) even before using the Ethereum network.

A common mechanism which can be implemented on wallets to circumvent the gas requirement on the user end is to require the user to sign a message consisting of the parameters of the transfer, send this message to a relayer, and let the relayer deploy the message to the token contract, which consist of specific functions to perform ercrecover and execute the balance increment/decrement.

Contract Implementation at: https://github.com/Nethereum/DelegateTestToken-Deployer/blob/master/contract/DelegateTestToken.sol, namely, the delegableToken contract which provides the functionality validate and execute signed token transfers.

As for the server side, we use the DelegatedSignerService as an abstract class which encompasses the generic parameters that a signed transaction should have:
* Owner - Owner (address) of the transaction.
* Fee - Fee amount charged by the relayer.
* DelegatedNonce - The nonce of Owner, to prevent replay attacks.
* Sig - This is a keccak256 hash of relevant parameters, acts as a checksum to ensure the parameters are correct and the signing account is the Owner.
* FeeAccount - The account where fees are to be sent to.

A TokenDelegatedSignerService class which inherits the DelegatedSignerService introduces the additional parameters - To (address) and Value (to transfer) to pass the parameters which are necessary for an ERC20 token transfer.

For the client end, the private key is necessary for the transaction to be signed to identify the holder of the tokens, also to ensure that all parameters are as originated from the client.

PS: This could be extended by creating a smart contract wallet that manages token transfers (possibly using CREATE2 opcode so a wallet address is pre-allocated), which takes the command to transfer tokens by means of a signed transaction. This way, the token contract does not need to natively support the signed transfer functionality, allowing support for a wider array of tokens.


# Implementation Sample: DelegateTestToken-Deployer

This test allows access to an ERC20 deployed on address 0x1a073cbe88718403c3e521494e1d0d263252ecb3, with a signed transfer function which allows function call delegation to a third party to pay for gas.

For the context of this sample, the fee defaults to 1% of the total token transferred, which will be added on top intended transferred amount.

![alt text](https://pictr.com/images/2018/07/14/tauU1.md.png)

Requires:
1. **Private key of token holder (Token Deployed At)**
   >The token holder itself. The private key is meant to sign the transaction, to be ran on the client end without ever needing the private key to be transmitted out of the client device. Once the transaction is signed by the holder, it is being delegated to the deploying address for deployment.
   
   >In this sample, the token holder is 0x794398c00aE32e62B4f3b90Fe050D32D55A59878, and its private key is embedded in the test executable (12ed9149b9202ccf46e7bdd856788cfc4e4c5b598ee445653f6bbccc7899ce84). This address holds tokens from 0x1a073cbe88718403c3e521494e1d0d263252ecb3, but has no ethers to pay for gas.
   
   > Example tx: https://rinkeby.etherscan.io/tx/0x5e5051062f0df5b1cb6ca95a1d09d6f86543bb5cab72dd4d1b1773e5dffc51bf


2. **To address (where the tokens should be sent to).**
   >The token receiving address.


3. **Amount (number of tokens to send).**
   >Number of tokens to send. Numeric.


4. **Deployer Private Key**
   >Private keys to the deploying address. This address will execute the signed transfer, and will require to hold some ethers to pay for gas. Just use any account with some Rinkeby ethers.
   
   >In return for the incurred gas cost, 1% of the transferred token sum is calculated and sent to the deploying address, which acts as a deployment fee. This is specified within the test executable. With enough traction, a form of deployer marketplace is possible.

