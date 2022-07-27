from grongier.pex import OutboundAdapter,InboundAdapter
from msg import MarketResponse
from utils import Book
import quickfix
import quickfix43

import time
from datetime import datetime

__SOH__ = chr(1)


class OrderAdapter(quickfix.Application,OutboundAdapter):
    """
    This adapter is used to hold the quickfix application & more
    name : Python.OrderAdapter
    """

    def on_keepalive(self):
        pass

    def init_initiator(self,storefactory,session_settings,logfactory,sessionID,host):
        try:
            self.lastMsg = None
            self.execID = 0
            self.quoteID = 0
            self.sessionID = sessionID
            self.username = host.Username if hasattr(host,"Username") else ""
            self.password = host.Password if hasattr(host, "Password") else ""
            self.delivertocompID = host.DelivertocompID if hasattr(host, "DelivertocompID") else ""
            self.sendersubID = host.SendersubID if hasattr(host, "SendersubID") else ""
            self.initiator = quickfix.SocketInitiator(self, storefactory, session_settings, logfactory)
            self.initiator.start()
        except (quickfix.ConfigError, quickfix.RuntimeError) as e:
            if hasattr(self,'initiator'):
                self.initiator.stop()
            raise e

    def stop_initiator(self):
        self.initator.stop()

    def send_msg(self,message):
        self.lastMsg = "Time Out 5s"

        header = message.getHeader()
        message.setField(11, self.genExecID()) #ClOrdID
        message.setField(60, str(datetime.now().strftime("%Y%m%d-%H:%M:%S"))) #TransactTime

        quickfix.Session.sendToTarget(message,self.sessionID)        

        start = time.perf_counter()
        # Once a message was sent to the server, we wait 5 seconds for a response or we time out
        while time.perf_counter() - start < 5 and self.lastMsg == "Time Out 5s" :
            pass
        return self.lastMsg

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        self.log_info("FixOrder onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self.log_info("FixOrder Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        self.log_info("FixOrder Session (%s) logout !" % sessionID.toString())
        return
        
    def toAdmin(self, message, sessionID):
        # If logon message, add to the header the connection info
        if message.getHeader().getField(35) == "A" and self.username != "" and self.password != "":
            message.getHeader().setField(553, self.username)
            message.getHeader().setField(554, self.password)
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AdminOrder) S >> %s" % msg)
        return
        
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AdminOrder) R << %s" % msg)

        msgtype = quickfix.MsgType()
        message.getHeader().getField(msgtype)

        # If we receive from admin an error or a reject, we send it as a response
        if msgtype.getValue() == "3" or msgtype.getValue() == "2":
            self.lastMsg = message
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AppOrder) S >> %s" % msg)
        return
        
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AppOrder) R << %s" % msg)
        # if we receive a message from app we send it as a response
        self.lastMsg = message
        return


class QuoteAdapter(quickfix.Application,OutboundAdapter):

    def on_init(self):
        adapter_attr = {}
        for attr in set(dir(self)).difference(set(dir(OutboundAdapter))).difference(set(['OnMessage','subscription','unsubscription'])):
            adapter_attr[attr] = getattr(self,attr)
        self.business_host_python.adapter_attr = adapter_attr

    def on_keepalive(self):
        pass

    def init_initiator(self,storefactory,session_settings,logfactory,sessionID,host):
        try:
            self.host = host
            self.execID = 0
            self.quoteID = 0
            self.sessionID = sessionID
            self.username = host.Username if hasattr(host,"Username") else ""
            self.password = host.Password if hasattr(host, "Password") else ""
            self.delivertocompID = host.DelivertocompID if hasattr(host, "DelivertocompID") else ""
            self.sendersubID = host.SendersubID if hasattr(host, "SendersubID") else ""
            self.marketList = []
            self.initiator = quickfix.SocketInitiator(self, storefactory, session_settings, logfactory)
            self.initiator.start()

        except (quickfix.ConfigError, quickfix.RuntimeError) as e:
            if hasattr(self,'initiator'):
                self.unsubscription()
                self.initiator.stop()
            raise e

    def stop_initiator(self):
        try:
            self.unsubscription()
        except Exception as e:
            self.log_info(str(e))
        self.unsubscription()
        self.initator.stop()

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def genQuoteID(self):
        self.quoteID += 1
        return str(self.quoteID).zfill(5)

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        self.log_info("FixQuote onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self.log_info("FixQuote Successful Logon to session '%s'." % sessionID.toString())
        try:
            self.subscription()
        except Exception as e:
            self.log_info(str(e))
        return

    def onLogout(self, sessionID):
        self.log_info("FixQuote Session (%s) logout !" % sessionID.toString())
        return
        
    def toAdmin(self, message, sessionID):
        # If logon message, add to the header the connection info
        if message.getHeader().getField(35) == "A" and self.username != "" and self.password != "":
            message.getHeader().setField(553, self.username)
            message.getHeader().setField(554, self.password)
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AdminQuote) S >> %s" % msg)
        return
        
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AdminQuote) R << %s" % msg)

        msgtype = quickfix.MsgType()
        message.getHeader().getField(msgtype)

        # If we receive from admin an error or a reject, we send it as a response
        if msgtype.getValue() == "3" or msgtype.getValue() == "2":
            self.lastMsg = message
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AppQuote) S >> %s" % msg)
        return
        
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(AppQuote) R << %s" % msg)
        # If we receive a message from app, we have to process it
        try:
            self.onMessage(message)
        except Exception as e:
            self.log_info(str(e))
        return

    def send_msg(self,message):
        self.lastMsg = "Time Out 5s"

        message.setField(131, self.genQuoteID()) #QuoteReqID

        quickfix.Session.sendToTarget(message,self.sessionID)
        
        start = time.perf_counter()
        # Once a message was sent to the server, we wait 5 seconds for a response or we time out
        while time.perf_counter() - start < 5 and self.lastMsg == "Time Out 5s" :
            pass
        return self.lastMsg


    def onMessage(self, message):
        msgtype = quickfix.MsgType()
        message.getHeader().getField(msgtype)

        # if the message received for the app is a market response
        if msgtype.getValue() == "W":
            symbol = quickfix.Symbol()
            message.getField(symbol)
            _bids = []
            _asks = []
            _trades = []

            instrument = symbol.getValue()

            entry_type = quickfix.MDEntryType()
            entry_px = quickfix.MDEntryPx()
            entry_size = quickfix.MDEntrySize()
            entries = quickfix.NoMDEntries()

            message.getField(entries)

            group = quickfix43.MarketDataSnapshotFullRefresh().NoMDEntries()

            for i in range(entries.getValue()):
                message.getGroup(i + 1, group)
                group.getField(entry_type)
                group.getField(entry_px)
                group.getField(entry_size)

                if entry_type.getValue() == "0":
                    _bids.append((entry_px.getValue(), entry_size.getValue()))
                elif entry_type.getValue() == "1":
                    _asks.append((entry_px.getValue(), entry_size.getValue()))
                elif entry_type.getValue() == "2":
                    _trades.append((entry_px.getValue(), entry_size.getValue()))

            book = Book(instrument, _bids, _asks, _trades)
            try:
                # Send a "good looking" message to the FixBusinessProcess to show it in the log
                self.host.send_request_async("Python.FixBusinessProcess",self.host.generate_message(message,book))
            except Exception as e:
                self.log_info(str(e))
        else:
            self.lastMsg = message
                
    def subscription(self):
        adapter_attr = self.host.get_info()
        if adapter_attr["subscribe"] == "True":

            message = quickfix43.MarketDataRequest()
            header = message.getHeader()

            header.setField(262, str(self.genExecID())) #MDReqID

            # Subscription snapshot + updates
            message.setField(
                quickfix.SubscriptionRequestType(
                    quickfix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES
                )
            )
    
            message.setField(264, adapter_attr["MarketDepth"]) #MarketDepth

            group = quickfix43.MarketDataRequest().NoMDEntryTypes()

            for md_type in adapter_attr["md_types"].split(";"):
                group.setField(269, md_type) #269 MDEntryType
                message.addGroup(group)

            message.setField(265, adapter_attr["MDUpdateType"]) #MDUpdateType

            if self.delivertocompID != "":
                header.setField(128, self.delivertocompID) #DeliverToCompID
            if self.sendersubID != "":
                header.setField(50, self.sendersubID) #SenderSubID

            message.setField(167, adapter_attr["SecurityType"]) #SecurityType

            group = quickfix43.MarketDataRequest().NoRelatedSym()


            for symbol,product in zip(adapter_attr["symbols"].split(";"),adapter_attr["products"].split(";")):
                group.setField(55, symbol) #Symbol
                group.setField(460, product) #Product
                message.addGroup(group)

            msg = message.toString().replace(__SOH__, "|")
            self.log_info(f"Market subscription : {msg}")
            self.host.send_request_async("Python.FixBusinessProcess",self.host.generate_message(message))
            quickfix.Session.sendToTarget(message, self.sessionID)

    def unsubscription(self):
        adapter_attr = self.host.get_info()
        message = quickfix43.MarketDataRequest()
        header = message.getHeader()

        header.setField(262, str(self.genExecID())) #MDReqID

        # Unsubscription snapshot + updates
        message.setField(
            quickfix.SubscriptionRequestType(
                quickfix.SubscriptionRequestType_DISABLE_PREVIOUS_SNAPSHOT_PLUS_UPDATE_REQUEST
            )
        )
 
        message.setField(264, adapter_attr["MarketDepth"]) #MarketDepth

        group = quickfix43.MarketDataRequest().NoMDEntryTypes()

        for md_type in adapter_attr["md_types"].split(";"):
            group.setField(269, md_type) #269 MDEntryType
            message.addGroup(group)

        message.setField(265, adapter_attr["MDUpdateType"]) #MDUpdateType

        if self.delivertocompID != "":
            header.setField(128, self.delivertocompID) #DeliverToCompID
        if self.sendersubID != "":
            header.setField(50, self.sendersubID) #SenderSubID

        message.setField(167, adapter_attr["SecurityType"]) #SecurityType

        group = quickfix43.MarketDataRequest().NoRelatedSym()


        for symbol,product in zip(adapter_attr["symbols"].split(";"),adapter_attr["products"].split(";")):
            group.setField(55, symbol) #Symbol
            group.setField(460, product) #Product
            message.addGroup(group)

        msg = message.toString().replace(__SOH__, "|")
        self.log_info(f"Market subscription : {msg}")
           
        quickfix.Session.sendToTarget(message, self.sessionID)