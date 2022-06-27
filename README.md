# IRIS-fix-protocol
Implementation of the fix protocol using an IRIS python container for the initiator and a regular python container for the acceptor.

# Requirements
- QuickFix will be installed automatically when building ( takes 10 to 20 minutes to build )
- If you use VSCode, you should have seen some pop up in the right corner, if you press `open in container` all the needed extensions will be installed but this step is not necessary.

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
## Using the demo

You must first start the demo, using the green `Start` button.

Then, by clicking on the operation `Python.FixBusinessOperation` and selecting in the right tab `action`, you can `test` the demo.

In this `test` window, select :<br>
Type of request : Ens.Request<br>

Then call test request.

Now you can click on `Visual Trace` to see in details what happened.


**Note that** only one session can be used by Python.FixBusinessOperation, if you want to modify the parameters of this session, go to `settings` in the right tab, then in the `Python` part, then in the `%settings` part.
See the difference between the `Python.FixBusinessOperation` and the `Python.FixBusinessOperation2`.<br>
Here you can enter any settings for your session like for the Operation2 : <br>
```
DataDictionary=/src
UseDataDictionary=N
BeginString=FIX.4.0
```

This will modify the session id in itself, as the BeginString will be different, it will also change the path for the DataDictionary to /src and ask not to use the dictionary.

To create multiple sessions and them being active at the same time, you can add a new operation with the + near the Operation column.
In Operation Class select `Python.FixBusinessOperation` and in the Operation Name `Python.FixBusinessOperation3` for example.