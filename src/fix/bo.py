from grongier.pex import BusinessOperation

import quickfix
import quickfix43

from msg import Request,Response
from obj import HeaderField,MessageField,GroupField

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
                if msgtype != None and self.tree != None:
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

    def generate_message(self,message,book=None):
        if type(message) == str:   
            resp = Response()
            resp.msg = message
        else:
            hdr_field = HeaderField()
            msg_field = MessageField()
            grp_field = GroupField()
            base_msg = message.toString().replace(__SOH__, "|")
            root = ET.fromstring(message.toXML())

            for field in root.findall(f"header/field"):
                setattr(hdr_field,field.get('number'),field.text)

            for field in root.findall("body/field"):
                setattr(msg_field,field.get('number'),field.text)

            ctn = 0
            for group in root.findall("body/group"):
                temp = {}
                for field in group.findall("field"):
                    temp[field.get('number')] = field.text
                setattr(grp_field,f"grp{ctn}",temp)
                ctn+=1
                
            resp = Response(hdr_field,msg_field,grp_field,base_msg)
        if book:
            resp.book = book
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
                if msgtype != None and self.tree != None:
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

            appResp = self.adapter.send_msg(message)
            msg = self.generate_message(appResp)
            return msg

        except Exception as e:
            self.log_info(str(e))

    def get_info(self):
        return self.adapter_attr


    def generate_message(self,message,book=None):
        if type(message) == str:   
            resp = Response()
            resp.msg = message
        else:
            hdr_field = HeaderField()
            msg_field = MessageField()
            grp_field = GroupField()
            base_msg = message.toString().replace(__SOH__, "|")
            root = ET.fromstring(message.toXML())

            for field in root.findall(f"header/field"):
                setattr(hdr_field,field.get('number'),field.text)

            for field in root.findall("body/field"):
                setattr(msg_field,field.get('number'),field.text)

            ctn = 0
            for group in root.findall("body/group"):
                temp = {}
                for field in group.findall("field"):
                    temp[field.get('number')] = field.text
                setattr(grp_field,f"grp{ctn}",temp)
                ctn+=1
                
            resp = Response(hdr_field,msg_field,grp_field,base_msg)
        if book:
            resp.book = book
        return resp