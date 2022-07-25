# IRIS-fix-protocol
Implementation of the fix protocol using an IRIS python container for the initiator and a regular python container for the acceptor.

The Financial Information eXchange (FIX®) Protocol has revolutionized the trading environment, proving fundamental in facilitating many of the electronic trading trends that have emerged over the past decade.

FIX has become the language of the global financial markets used extensively by buy and sell-side firms, trading platforms and even regulators to communicate trade information.

This demo has for objective to simulate a FIX client, allowing the user to create multiple sessions connected to a server ( fix acceptor ) and send buy or sell requests.

# Requirements and information
- [QuickFix](https://quickfixengine.org/c/) will be installed automatically when building ( takes 10 to 20 minutes to build once )
- If you use VSCode, you should have seen some pop up in the right corner, if you press `open in container` all the needed extensions will be installed but this step is not necessary.

See [this website](https://new.quickfixn.org/c/documentation/) for the general documentation.<br>

See [this website](https://www.onixs.biz/fix-dictionary/4.3/fields_by_tag.html#) for the tags documentation.<br>

See [this website](https://www.onixs.biz/fix-dictionary/4.3/msgs_by_msg_type.html) for the Message Types.<br>


# The demo
## Starting the demo
To start the demo you have to use docker-compose in the `iris-fix-protocol` folder:
```
docker-compose up --build
```

The first time you do this it will take some time to install QuickFix.

## Closing the demo
```
docker-compose down
```
By only closing the demo you can up it again and it will take only a few seconds since the image is already built.

## Opening the demo

If you are **NOT** inside the IRIS container connect to the demo using :
```
http://localhost:52795/csp/irisapp/EnsPortal.ProductionConfig.zen?PRODUCTION=INFORMATION.QuickFixProduction
```
The `Username` is `SuperUser` and the `Password` is `SYS`

Else,
```
http://127.0.0.1:52773/csp/irisapp/EnsPortal.ProductionConfig.zen?PRODUCTION=INFORMATION.QuickFixProduction
```
## Using the client demo : Initiator

### Settings and Sessions

**Note that** only one session can be used by Python.FixBusinessOperation, if you want to modify the parameters of this session, click on the `Python.FixBusinessOperation` then go to `settings` in the right tab, then in the `Python` part, then in the `%settings` part.
Here, you can enter or modify any parameters ( don't forget to press `apply` once your are done ).<br>
Here's the default configuration :
```
BeginString=FIX.4.3
SenderCompID=CLIENT
TargetCompID=SERVER
HeartBtInt=30
SocketConnectPort=3000
SocketConnectHost=acceptor
DataDictionary=/irisdev/app/src/fix/spec/FIX43.xml
FileStorePath=/irisdev/app/src/fix/Sessions/
ConnectionType=initiator
FileLogPath=./Logs/
StartTime=00:00:00
EndTime=00:00:00
ReconnectInterval=10
LogoutTimeout=5
LogonTimeout=30
ResetOnLogon=Y
ResetOnLogout=Y
ResetOnDisconnect=Y
SendRedundantResendRequests=Y
SocketNodelay=N
ValidateUserDefinedFields=N
ValidateFieldsOutOfOrder=N
```
Now, on start/restart, the new configuration will apply and the new session will be created.


To create multiple sessions and them being active at the same time, you can add a new operation with the + near the Operation column.
In Operation Class select `Python.FixBusinessOperation` and in the Operation Name `Python.FixBusinessOperation3` for example, now you need to enter the configuration you want for your session.<br>
It can be the same as the default configuration seen earlier or any other valid configuration.<br>
See this [website (in the 'Getting started' / 'Configuration' tab)](https://new.quickfixn.org/c/documentation/) for more information.

### Send a quote
**New Quote**
Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.QuoteRequest
```

 And for the `json`, here is an example of quote request :
```
{
    "symbols":"MSFT",
    "comm_type":"2",
    "ord_type":"market"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs of the initiator.


### Send an order

You must first start the demo, using the green `Start` button or `Stop` and `Start` it again to apply your config changes.

Then, by clicking on the operation `Python.FixBusinessOperation` of your choice, and selecting in the right tab `action`, you can `test` the demo.

In this `test` window, select :<br>


**New Order Buy**
Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.OrderRequest
```

 And for the `json`, here is an example of a simple buy order :
```
{
    "symbol":"MSFT",
    "quantity":"10000",
    "price":"100",
    "side":"buy",
    "ord_type":"limit",
    "currency":"EUR/USD",
    "exec_inst":"B",
    "time_in_force":"1",
    "min_qty":"8000"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs of the initiator.

<br><br>

**New Order Sell**
Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.OrderRequest
```

By using "side":"sell" we can send make a simple sell order :
```
{
    "symbol":"MSFT",
    "quantity":"10000",
    "price":"100",
    "side":"sell",
    "ord_type":"limit"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs of the initiator.

<br><br>


**Existing Order Replace** WIP
For this you will need to have send an order request buy or sell.
By entering the original client order id of the request and it's symbol, you can replace it.

Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.ReplaceOrderRequest
```
```
{
    "symbol":"MSFT",
    "quantity":"1000",
    "price":"1000",
    "side":"buy",
    "orig_client_order_id":"00001"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs of the initiator.

**Existing Order Delete** WIP
For this you will need to have send an order request buy or sell.
By entering the original client order id of the request and it's symbol, you can delete it.

Type of request : `Grongier.PEX.Message`<br>

For the `classname` you must enter :
```
msg.DeleteOrderRequest
```
```
{
    "symbol":"MSFT",
    "side":"buy",
    "orig_client_order_id":"00001"
}
```
Now you can click on `Visual Trace` to see in details what happened and see the logs of the initiator.

## Using the server demo : Acceptor

### Logs

The acceptor is isolated in another container, to access it's logs you must go to the source folder `iris-fix-protocol` then in the `acceptor/Logs` folder.
Here you can see the logs for each session.

### New acceptor session

If you are familiar with the FIX protocol, you now that creating a session on the client side without adding it to the server side will lead to an error, which is logical as security and reliability are key words for the FIX protocol.

To add a new session to the acceptor you must go to `acceptor/server.cfg` and add at the end of the file the sessions you wish to add.

Now you can enter in the terminal :
```sh
docker-compose up -d --build acceptor
```

**Note that this will close the acceptor and restart it so it may lead to issues regarding sent requests and stored data**

