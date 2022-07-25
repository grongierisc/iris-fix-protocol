docker-compose up

docker-compose exec -u root iris bash
    service stunnel4 start
    

management portal :

    **QUOTE OPERATION OR FIX SERVICE started ( THEY DO NOT WORK TOGETHER )**

    **FIX SERVICE**
    Nothing to do, just watch the logs and see the market subscription and see the messages on the process 

    **QUOTE REQUEST**
    Type of request : `Grongier.PEX.Message`<br>

    For the `classname` you must enter :
    ```
    msg.QuoteRequest
    ```

    And for the `json`, here is an example of quote request :
    ```
    {
        "symbols":"USD/JPY",
        "comm_type":"2",
        "currency":"USD"
    }
    ```

    **ORDER REQUEST **
    Type of request : `Grongier.PEX.Message`<br>

    For the `classname` you must enter :
    ```
    msg.OrderRequest
    ```

    And for the `json`, here is an example of a simple buy order :
    ```
   {
        "symbol": "EUR/USD",
        "quantity": "10000",
        "price": "100",
        "side": "buy",
        "ord_type": "limit",
        "currency": "EUR",
        "exec_inst": "B",
        "min_qty": "8000"
    }
    ```