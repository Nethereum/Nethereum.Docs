---
title: "What is an Ethereum Event?"
author: "Gaël Blanchemain"
date: "October 11, 2017"
export_on_save:
  markdown: true
---
## What is an Ethereum Event?

In the Ethereum environment, functions don't return anything. In order to compensate for that limitation,  Solidity offers a way to log state changes which is called Event.

Events are functions that store a change on a log, they are often used to trigger UI functions.

In the example below, an event called 'Multiplied' is first declared (line 18) then assigned (line 26);
```javascript
15	 contract test {
16
17	    int _multiplier;
18	    event Multiplied(int indexed a, address indexed sender, int result );
…
26	       Multiplied(a, msg.sender, r);
27	       return r;
28	    }
29	 }
```