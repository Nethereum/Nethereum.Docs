
A Smart Contract’s ABI is specified as a JSON array of function descriptions events. A **function description** is a JSON object with fields type, name, inputs, outputs, constant, and payable. An **event description** object has fields type, name, inputs, and anonymous.

In Ethereum, the ABI is used to encode contract calls for the EVM and to read data out of transactions. The purpose of an ABI is to define the functions in the contract that can be invoked and describe how each function will accept arguments and return its result.

Nethereum provides a `abiEncode` class with methods to serialize/deserialize data to and from the ABI format.

Note!!!
    You can execute samples pertaining to ABI encoding in Nethereum's playground
    using the following links: 
    - [ABI Encoding: Encoding using ABI Values, Parameters and Default values ](http://playground.nethereum.com/csharp/id/1015)
    - [ABI Encoding Packed: Encoding using ABI Values ](http://playground.nethereum.com/csharp/id/1016)
    - [ABI Encoding Packed: Encoding using parameters ](http://playground.nethereum.com/csharp/id/1017)
    - [ABI Encoding Packed: Encoding using default values](http://playground.nethereum.com/csharp/id/1018) 

## GetSha3ABIParamsEncodedPacked

```csharp
using System;
using System.Text;
using Nethereum.Hex.HexConvertors.Extensions;
using System.Threading.Tasks;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Util;
using Nethereum.ABI;

		public class TestParamsInput
		{
				[Parameter("string", 1)] public string First { get; set; }
				[Parameter("int8", 2)] public int Second { get; set; }
				[Parameter("address", 3)] public string Third { get; set; }
		}

    static void Main(string[] args)
    {
				var abiEncode = new ABIEncode();
				var result = abiEncode.GetSha3ABIParamsEncodedPacked(new TestParamsInput()
						{First = "Hello!%", Second = -23, Third = "0x85F43D8a49eeB85d32Cf465507DD71d507100C1d"});
				Console.WriteLine("Result: " + result.ToHex(true));

    }
```

## GetABIEncoded

```csharp
using System.Text;
using System.Threading.Tasks;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Util;
using Nethereum.ABI;

public class AbiEncode_AbiValue_Parameters_Default
{
	public class TestParamsInput
	{
			[Parameter("string", 1)]
			public string First { get; set; }
			[Parameter("int256", 2)]
			public int Second { get; set; }
			[Parameter("string", 3)]
			public string Third { get; set; }
	}

    static void Main(string[] args)
    {
            
		var abiEncode = new ABIEncode();
		var result = abiEncode.GetABIEncoded(new ABIValue("string", "hello"), new ABIValue("int", 69),
						new ABIValue("string", "world")).ToHex();

		Console.WriteLine("Encoded hello, 69 and world using ABIValue: " + result);


		result = abiEncode.GetABIEncoded("1", "2", "3").ToHex();

		Console.WriteLine("Encoded 1, 2, 3 strings using  default convertor: " + result);

    }
}
```

## GetABIParamsEncoded

```csharp
using System;
using System.Text;
using Nethereum.Hex.HexConvertors.Extensions;
using System.Threading.Tasks;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Util;
using Nethereum.ABI;

public class AbiEncode_AbiValue_Parameters_Default
{
	public class TestParamsInput
	{
			[Parameter("string", 1)]
			public string First { get; set; }
			[Parameter("int256", 2)]
			public int Second { get; set; }
			[Parameter("string", 3)]
			public string Third { get; set; }
	}

    static void Main(string[] args)
    {
            
		var abiEncode = new ABIEncode();
		var result = abiEncode.GetABIEncoded(new ABIValue("string", "hello"), new ABIValue("int", 69),
						new ABIValue("string", "world")).ToHex();

		Console.WriteLine("Encoded hello, 69 and world using ABIValue: " + result);

		result = abiEncode.GetABIParamsEncoded(new TestParamsInput(){First = "hello", Second = 69, Third = "world"}).ToHex();
		
		Console.WriteLine("Encoded hello, 69 and world using Parameter attributes: " + result);
    }
}
```

## GetSha3ABIEncodedPacked

```csharp
using System;
using System.Text;
using Nethereum.Hex.HexConvertors.Extensions;
using System.Threading.Tasks;
using Nethereum.ABI.FunctionEncoding.Attributes;
using Nethereum.Util;
using Nethereum.ABI;

public class AbiEncodePacked_UsingDefaultValues
{
    static void Main(string[] args)
    {
					var abiEncode = new ABIEncode();
            var result = abiEncode.GetSha3ABIEncodedPacked(234564535,
                "0xfff23243".HexToByteArray(), true, -10);
						Console.WriteLine("Encoded 234564535, 0xfff23243, true and -10:" + result.ToHex());

            var result2 = abiEncode.GetSha3ABIEncodedPacked("Hello!%");
						Console.WriteLine("Encoded Hello!%:" + result2.ToHex());
          
            var result3 = abiEncode.GetSha3ABIEncodedPacked(234);
            Console.WriteLine("Encoded 234:" + result2.ToHex());
    }
}
```
