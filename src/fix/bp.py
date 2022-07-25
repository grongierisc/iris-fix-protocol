from grongier.pex import BusinessProcess
from msg import OrderRequest,QuoteRequest,MarketResponse

class FixBusinessProcess(BusinessProcess):

    def on_request(self,request):
        if isinstance(request,OrderRequest):
            quote_req = QuoteRequest(request.symbol,2,request.ord_type)
            quote_resp = self.send_request_sync("Python.FixQuote",quote_req)
            if quote_resp.msg != "Time Out 2s":
                request.quote_id = getattr(quote_resp,117)
                order_resp = self.send_request_sync("Python.FixOrder")
                return order_resp
            else:
                return quote_resp
        
        elif isinstance(request,MarketResponse):
            #self.log_info(request)
            pass

        else:
            return request

        
