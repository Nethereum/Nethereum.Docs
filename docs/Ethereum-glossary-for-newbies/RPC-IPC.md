---
title: "What is RPC / IPC?"
author: "Gaël Blanchemain"
date: "July 27, 2017"
export_on_save:
  markdown: true
---
##  What is RPC / IPC?

####  tl;dr
Both RPC / IPC are procedures used for any processes to interact with an Ethereum node. 
They are necessary for any Dapp to communicate with public/private Ethereum networks.

###  Detailed explanation
**IPC** or "_Inter-process Communications_" generally works on your local computer. In the Ethereum space, IPC normally involves geth creating a IPC pipe (which is represented by the file $HOME/.ethereum/geth.ipc) on your computer's local filesystem.

Other processes on the same computer can then use the IPC file to create bi-directional communications with geth.

**RPC** or "_Remote Procedure Calls_" generally works across different computers. In the Ethereum space, RPC normally refers to the RPC endpoint localhost:8545 or 127.0.0.1:8545 or 192.168.1.123:8545.

If you use localhost:8545 or 127.0.0.1:8545 for your RPC endpoint, ONLY other processes on the local computer can communicate via this RPC endpoint, as localhost and 127.0.0.1 is only accessible from the local computer.

If you use a non-local IP address like 192.168.1.123, any other computer on your network can access this RPC endpoint.

If your internet connection forwards traffic from your internet IP address to your computer's IP address 192.168.1.123 then any computer from the internet can access your RPC endpoint by connecting to {your internet IP address}:8545.

Credits  to [BokkyPooBah](https://ethereum.stackexchange.com/users/1268/bokkypoobah) for the technical part of this explanation: https://ethereum.stackexchange.com/questions/10681/what-are-ipc-and-rpc