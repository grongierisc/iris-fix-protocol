from grongier.pex import BusinessOperation

import quickfix
import quickfix43

from msg import OrderRequest,FixResponse,QuoteRequest

__SOH__ = chr(1)

class FixOrderOperation(BusinessOperation):

    def get_adapter_type():
        """
        Get the Application adapter needed for quickfix
        """
        return "Python.OrderAdapter"


    def on_init(self):
        # We create a SessionSettings and get its settings dict
        session_settings = quickfix.SessionSettings()
        settings_dict = session_settings.get()
        
        # We get all the attr that are in self but not in the base BusinessOperation class
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['new_order','genExecID','replace_order','delete_order','generate_message','new_quote']))

        # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
        for attr in config_attr:
            self.log_info(attr + " : " + str(getattr(self,attr)))
            settings_dict.setString(attr,getattr(self, attr))

        
        sessionID = quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID)

        # We set our session with the session IDs and the settings we want for it
        session_settings.set(sessionID,settings_dict)

        # Create our Application and apply our sessions_settings
        storefactory = quickfix.FileStoreFactory(session_settings)
        logfactory = quickfix.FileLogFactory(session_settings)
        
        # Create the initiator inside the adapter
        self.adapter.init_initiator(storefactory,session_settings,logfactory,sessionID,self.Username,self.Password,self.DeliverToCompID,self.SenderSubID)        
            
    def on_tear_down(self):
        self.adapter.stop_initiator()

    def on_message(self, request):
        self.log_info("on_message")
        return 

    def new_order(self,request:OrderRequest):

        if request.side.lower() == "buy":
            side = quickfix.Side_BUY
        else:
            side = quickfix.Side_SELL

        message = quickfix.Message()

        header = message.getHeader()
        header.setField(35,"D") #MsgType

        message.setField(55,request.symbol) #Symbol
        message.setField(54, side) #Side
        message.setField(15,request.currency) #Currency
        message.setField(44,request.price) #Price
        message.setField(117, "")#request.quote_id) #QuoteID
        message.setField(18, request.exec_inst) #ExecInst
        message.setField(460, "4") #Product
        message.setField(110, request.min_qty) #MinQty
        message.setField(21, "3") #HandlInst
        message.setField(38, request.quantity) #OrderQty

        message.setField(quickfix.TransactTime()) # 60 TransactTime

        if request.ord_type.lower() == "market":
            message.setField(40, "1") #OrdType Market
        else:
            message.setField(40, "2") #OrdType Limit

        message.setField(58, f"{side} {request.symbol} {request.quantity}@{request.price}") #Text

        appResp = self.adapter.send_msg(message)
        msg = self.generate_message(appResp)
        return msg

    def generate_message(self,message):
        resp = FixResponse()
        resp.msg = message
        if message != "Time Out 2s":
            for pair in message.split("|"):
                if pair != "":
                    tag,value = pair.split("=")
                    setattr(resp, tag, value)
        return resp

class FixQuoteOperation(BusinessOperation):

    def get_adapter_type():
        """
        Get the Application adapter needed for quickfix
        """
        return "Python.QuoteAdapter"


    def on_init(self):
        # We create a SessionSettings and get its settings dict
        session_settings = quickfix.SessionSettings()
        settings_dict = session_settings.get()
        
        # We get all the attr that are in self but not in the base BusinessOperation class
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['generate_message','new_quote']))

        # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
        for attr in config_attr:
            self.log_info(attr + " : " + str(getattr(self,attr)))
            settings_dict.setString(attr,getattr(self, attr))

        
        sessionID = quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID)

        # We set our session with the session IDs and the settings we want for it
        session_settings.set(sessionID,settings_dict)

        # Create our Application and apply our sessions_settings
        storefactory = quickfix.FileStoreFactory(session_settings)
        logfactory = quickfix.FileLogFactory(session_settings)
        
        # Create the initiator inside the adapter
        self.adapter.init_initiator(storefactory,session_settings,logfactory,sessionID,self.Username,self.Password,self.DeliverToCompID,self.SenderSubID,self)        
            
    def on_tear_down(self):
        self.adapter.stop_initiator()

    def on_message(self, request):
        self.log_info("on_message")
        return

    def new_quote(self,request:QuoteRequest):

        message = quickfix.Message()
        header = message.getHeader()
        header.setField(35,"R") #MsgType

        group = quickfix43.QuoteRequest().NoRelatedSym()
        group.setField(40,"D") #OrdType
        for symbol in request.symbols.split(";"):
            group.setField(55,symbol) #Symbol
            #group.setField(40,"D") #OrdType
        message.addGroup(group)

        #message.setField(40,"D") #OrdType
        message.setField(167,"FOR") #SecurityType
        message.setField(54,"1") #Side
        message.setField(38,"10000") #OrderQty

        appResp = self.adapter.send_msg(message)
        msg = self.generate_message(appResp)
        return msg


    def generate_message(self,message):
        resp = FixResponse()
        resp.msg = message
        if message != "Time Out 2s":
            for pair in message.split("|"):
                if pair != "":
                    tag,value = pair.split("=")
                    setattr(resp, tag, value)
        return resp