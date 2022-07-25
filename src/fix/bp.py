from grongier.pex import BusinessProcess
from msg import Request,MarketResponse

class FixBusinessProcess(BusinessProcess):

    def on_request(self,request):
        if isinstance(request,Request):
            try:
                quote_req = Request()
                setattr(quote_req,"55",getattr(request,"55"))
                setattr(quote_req,"13","2")
                setattr(quote_req,"40",getattr(request,"40"))
            
                quote_resp = self.send_request_sync("Python.FixQuote",quote_req)

                if quote_resp.msg != "Time Out 5s":
                    setattr(request,"117",getattr(quote_resp,"117"))
                    order_resp = self.send_request_sync("Python.FixOrder",request)
                    return order_resp
                else:
                    return quote_resp
            except Exception as e:
                self.log_info(str(e))
        
        elif isinstance(request,MarketResponse):
            self.log_info(str(request))
            pass

        else:
            return request

        
