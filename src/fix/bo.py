from grongier.pex import BusinessOperation

import quickfix
import quickfix43

from msg import Request,FixResponse,QuoteRequest

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
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['new_request','genExecID','replace_order','delete_order','generate_message','new_quote']))

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
        self.adapter.init_initiator(storefactory,session_settings,logfactory,sessionID,self)        
            
    def on_tear_down(self):
        self.adapter.stop_initiator()

    def on_message(self, request):
        self.log_info("on_message")
        return 

    def new_request(self,request:Request):
        message = quickfix.Message()
        header = message.getHeader()
        try:
            for tag,value in request.__dict__.items():
                if tag[0] == "H":
                    header.setField(int(tag[1:]),value)
                else:
                    message.setField(int(tag),value)

            appResp = self.adapter.send_msg(message)
            msg = self.generate_message(appResp)
            return msg
        except Exception as e:
            self.log_info(str(e))

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
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['generate_message','new_request']))

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
        self.adapter.init_initiator(storefactory,session_settings,logfactory,sessionID,self)        
            
    def on_tear_down(self):
        self.adapter.stop_initiator()

    def on_message(self, request):
        self.log_info("on_message")
        return

    def new_request(self,request:Request):
        message = quickfix.Message()
        header = message.getHeader()
        try:
            for tag,value in request.__dict__.items():
                if tag[0] == "H":
                    header.setField(int(tag[1:]),value)
                else:
                    message.setField(int(tag),value)
            
            # Uncomment if acceptor can manage quote request
            #appResp = self.adapter.send_msg(message)
            #msg = self.generate_message(appResp)
            #return msg

            # To delete if acceptor can manage quote request
            temp = FixResponse()
            temp.msg = "Temp"
            setattr(temp,"117","1")
            return temp

        except Exception as e:
            self.log_info(str(e))


    def generate_message(self,message):
        resp = FixResponse()
        resp.msg = message
        if message != "Time Out 2s":
            for pair in message.split("|"):
                if pair != "":
                    tag,value = pair.split("=")
                    setattr(resp, tag, value)
        return resp