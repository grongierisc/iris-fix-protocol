from grongier.pex import BusinessProcess
from msg import Request,MarketResponse
from obj import MessageField,HeaderField,GroupField

class FixBusinessProcess(BusinessProcess):

    def on_request(self,request):
        return request

    def on_order_request(self,request:Request):
        """
        Logic of the project.
        When you get a request, depending on the msg_type ( and/or other field/tags) you process it differently
        """
        try:
            msg_type = getattr(request.header_field,"35")

            if msg_type == "D":
                msg_field = MessageField()

                setattr(msg_field,"55",getattr(request.message_field,"55"))
                setattr(msg_field,"13","2")
                setattr(msg_field,"40",getattr(request.message_field,"40"))

                quote_req = Request(msg_field)
            
                quote_resp = self.send_request_sync("Python.FixQuote",quote_req)

                if quote_resp.msg != "Time Out 5s":
                    setattr(request.message_field,"117",getattr(quote_resp,"117"))
                    order_resp = self.send_request_sync("Python.FixOrder",request)
                    return order_resp
                else:
                    return quote_resp

            elif msg_type == "R":
                quote_resp = self.send_request_sync("Python.FixQuote",request)
                return quote_resp

        except Exception as e:
            self.log_info(str(e))

    def on_market_response(self,request:MarketResponse):
        self.log_info(str(request))

        
