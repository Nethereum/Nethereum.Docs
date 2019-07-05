# Introduction to Unity in Nethereum

Nethereum supports the Unity .Net net351, net461 and netstandard frameworks. 

The Nethereum.Unity library is a Nethereum specific Unity library and api which provides support for UnityWebRequest to interact with Ethereum using RPC over Http. The Nethereum.Unity library is the only library that supports using IEnumerator and yield when working with Coroutines in Unity.

If wanted to work using async / await and Tasks in net461 / netstandard it is also possible in the same way as "vanilla" Nethereum as long as your environment does not require to use UnityWebRequest instead of HttpRequest. (Webgl requires to use UnityWebRequest)

Nethereum provides also AoT libraries for both net351 and net461 framework builds.

All the "dlls" can be downloaded from the Nethereum github releases https://github.com/Nethereum/Nethereum/releases.

## Example projects

The following projects provides examples on how to structure the projects and how to interact with Ethereum

### Flappy Eth

The flappy eth game sample, is the Unity3d "flappy" sample transformed to interact with Ethereum, Infura and Metamask using Nethereum as a webgl dapp game.

The source code of the main integration components can be found here: https://github.com/Nethereum/Nethereum.Flappy

You can also play the game here: http://flappyeth.nethereum.com/

![Flappy Eth](screenshots/flappy.png)

### Simple Unity3d sample

This simple Unity3d sample provides examples on how to interact with Ethereum, transfer ether and interact with smart contracts

There are two options the Net461, including Unity.UI interaction 
https://github.com/Nethereum/Unity3dSimpleSampleNet461, and the net351 https://github.com/Nethereum/Unity3dSimpleSample
![Desktop](screenshots/desktop.PNG "Desktop")
![Webgl](screenshots/webgl.png "Webgl")


