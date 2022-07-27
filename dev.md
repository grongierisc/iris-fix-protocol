docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker-compose up

docker-compose up -d --build acceptor

    

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
        "header_field":
            {
                "35":"R"
            },
        "group_field":
            {
                "146":
                {
                    "40":"1;2",
                    "55":"EUR/USD;USD/CZK"
                }
            }
        }
    ```

    **ORDER REQUEST **
    Type of request : `Grongier.PEX.Message`<br>

    For the `classname` you must enter :
    ```
    msg.Request
    ```

    And for the `json`, here is an example of a simple buy order :
    ```
    {
    "header_field":
        {
            "35":"D"
        },
    "message_field":
        {
            "55": "EUR/USD",
            "40": "1",
            "44": "100",
            "38": "10000",
            "54": "1",
            "21": "1"
        }
    }
    ```