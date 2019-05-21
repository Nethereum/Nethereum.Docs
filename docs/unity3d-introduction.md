# Introduction to Unity in Nethereum

Nethereum supports Unity3d for both net351 and net461 / netstandard frameworks. 

Nethereum provides support for Unity3d UnityWebRequest and yield mechanism for Tasks. A complete separate api of RPC Requests has been created to support this.

If wanted to work using Tasks using async / await in net461 / netstandard it is also possible in the same way as "vanilla" Nethereum as long as your environment (like webgl) requires to use UnityWebRequest.

Nethereum provides also an AoT for both net351 and net461 builds.

All the "dlls" can be downloaded from the Nethereum github releases https://github.com/Nethereum/Nethereum/releases.

## Example projects

The following projects provides examples on how to structure the projects and how to interact with Ethereum

### Flappy Eth

The flappy eth game sample, is the Unity3d "flappy" sample transformed to interact with Ethereum, Infura and Metamask using Nethereum as a webgl dapp game.

The source code of the main integration components can be found here: https://github.com/Nethereum/Nethereum.Flappy

You can also play the game here: http://flappyeth.nethereum.com/

![Flappy Eth](screenshots/flappy.png)

### Simple Unity3d sample

This simple Unity3d sample provides examples on how to transfer ether and interact with smart contracts

https://github.com/Nethereum/Unity3dSimpleSample

