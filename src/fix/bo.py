from grongier.pex import BusinessOperation

import quickfix
import quickfix43

from msg import Request,Response

import xml.etree.ElementTree as ET

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
        if self.DataDictionary:
            self.tree = ET.parse(self.DataDictionary)
        else:
            self.tree = None
        
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
            if request.header_field:
                for tag,value in request.header_field.__dict__.items():
                    header.setField(int(tag),value)
                    if tag == "35":
                        msgtype = value

            if request.message_field:
                for tag,value in request.message_field.__dict__.items():
                    message.setField(int(tag),value)
                    
            if request.group_field:
                if msgtype != None:
                    root = self.tree.getroot()
                    msg_name = root.find(f"messages/message[@msgtype='{msgtype}']").get('name')
                    for group_tag, list_group_tag in request.group_field.__dict__.items():
                        group_name = root.find(f"fields/field[@number='{group_tag}']").get('name')

                        group = getattr(getattr(quickfix43,msg_name)(),group_name)()

                        tag_list = list(list_group_tag.keys())
                        values_list = list(map(lambda x: x.split(";"),list_group_tag.values()))

                        size_values = len(values_list[0])
                        size_tag = len(tag_list)
                        for i in range(size_values):
                            for j in range(size_tag):
                                    group.setField(int(tag_list[j]),values_list[j][i])                                
                            message.addGroup(group)

            appResp = self.adapter.send_msg(message)
            msg = self.generate_message(appResp)
            return msg
        except Exception as e:
            self.log_info(str(e))

    def generate_message(self,message):
        resp = Response()
        resp.msg = message if type(message) == str else message.toString().replace(__SOH__, "|")
        if message != "Time Out 5s":
            for pair in resp.msg.split("|"):
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
        config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['generate_message','new_request','get_info','adapter_attr']))

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

        if self.DataDictionary:
            self.tree = ET.parse(self.DataDictionary)
        else:
            self.tree = None

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
        msgtype = None
        try:
            if request.header_field:
                for tag,value in request.header_field.__dict__.items():
                    header.setField(int(tag),value)
                    if tag == "35":
                        msgtype = value

            if request.message_field:
                for tag,value in request.message_field.__dict__.items():
                    message.setField(int(tag),value)
                    
            if request.group_field:
                if msgtype != None:
                    root = self.tree.getroot()
                    msg_name = root.find(f"messages/message[@msgtype='{msgtype}']").get('name')
                    for group_tag, list_group_tag in request.group_field.__dict__.items():
                        group_name = root.find(f"fields/field[@number='{group_tag}']").get('name')

                        #group = quickfix43.QuoteRequest().NoRelatedSym()
                        group = getattr(getattr(quickfix43,msg_name)(),group_name)()

                        tag_list = list(list_group_tag.keys())
                        values_list = list(map(lambda x: x.split(";"),list_group_tag.values()))

                        size_values = len(values_list[0])
                        size_tag = len(tag_list)
                        for i in range(size_values):
                            for j in range(size_tag):
                                    group.setField(int(tag_list[j]),values_list[j][i])                                
                            message.addGroup(group)

            # appResp = self.adapter.send_msg(message)
            # msg = self.generate_message(appResp)
            # return msg

            # To delete if acceptor can manage quote request
            temp = Response()
            temp.msg = "Temp"
            setattr(temp,"117","1")
            return temp

        except Exception as e:
            self.log_info(str(e))

    def get_info(self):
        return self.adapter_attr

    def generate_message(self,message,book=None):
        resp = Response()
        if book != None:
            resp.book = book
        resp.msg = message if isinstance(message, str) else message.toString().replace(__SOH__, "|")
        if resp.msg != "Time Out 5s":
            for pair in resp.msg.split("|"):
                if pair != "":
                    tag,value = pair.split("=")
                    setattr(resp, tag, value)
        return resp