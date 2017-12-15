## Installation and configuration of the Ethereum client Parity

[Parity](https://github.com/paritytech/parity/wiki) is an Ethereum client based on the RUST language.

You can download ``` Parity ``` latest stable version from [Github](https://github.com/paritytech/parity/releases/latest)

## Installation

### Windows

Use the [self-installer InstallParity.exe](https://github.com/paritytech/parity/releases/latest)

### Mac

A ``` .pkg ``` [installer for Mac OSX](https://github.com/paritytech/parity/releases/latest) is available.


It is also possible to use [Brew](https://brew.sh/):
```
$ brew update
$ brew upgrade
$ brew tap paritytech/paritytech
$ brew install parity --stable
```

### Linux

On Linux, a ``` .deb ``` package is available for Debian based distribution, [the sources are also available to build.](https://github.com/paritytech/parity/releases/latest)

#### Batch file

```
parity.exe --config node0.toml --tracing=on
```
[Source code](https://github.com/Nethereum/Nethereum.Workbooks/blob/9c7088591006f9677e167722d0d2a84f61bd93cc/testchain/parity%20poa/launch.bat)

[//]: # (CJuan> I couldn't run that script, your help is welcome)

#### Shell script

Ensure to make your script executable: ` chmod +x launch.sh `
```
parity.exe --config node0.toml --tracing=on
```
You can start the script from the directory where it sits: ` ./launch.sh
[Source code](https://github.com/Nethereum/Nethereum.Workbooks/blob/9c7088591006f9677e167722d0d2a84f61bd93cc/testchain/parity%20poa/launch.sh)


### Proof of Authority

The consensus mechanism used in the parity launch scripts is called Proof of Authority (PoA).

PoA consensus is reached by referring to a list of validators (referred to as authorities when they are linked to physical entities).

Since PoA doesn't require any mining, it's an extremely responsive mechanism (little to no delay after submitting a transaction) and it doesn't require manipulation to start mining ("mining" starts immediately).

