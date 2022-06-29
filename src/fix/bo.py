from grongier.pex import BusinessOperation
from datetime import datetime

import quickfix
import quickfix43

from msg import NewOrderRequest,ReplaceOrderRequest,DeleteOrderRequest

__SOH__ = chr(1)

class FixBusinessOperation(BusinessOperation):
    def on_init(self):
        try:
            # We create a SessionSettings and get it's settings dict
            session_settings = quickfix.SessionSettings()
            settings_dict = session_settings.get()
            
            # We get all the attr that are in self but not in the base BusinessOperation class
            config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['new_order','genExecID','replace_order','delete_order']))

            # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
            for attr in config_attr:
                settings_dict.setString(attr,getattr(self, attr))

            self.sessionID = quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID)

            # We set our session with the session IDs and the settings we want for it
            session_settings.set(self.sessionID,settings_dict)

            # Create our Application and apply our sessions_settings
            self.application = Application()
            storefactory = quickfix.FileStoreFactory(session_settings)
            logfactory = quickfix.FileLogFactory(session_settings)
            self.initiator = quickfix.SocketInitiator(self.application, storefactory, session_settings, logfactory)

            self.execID = 0

            # Start the initiator
            self.initiator.start()


        except (quickfix.ConfigError, quickfix.RuntimeError) as e:
            if hasattr(self,'initiator'):
                self.initiator.stop()
            raise e
            

    def on_tear_down(self):
        self.initiator.stop()

    def on_message(self, request):
        self.log_info("on_message")
        return 

    def genExecID(self):
        self.execID += 1
        self.application.execID += 1
        return str(self.execID).zfill(5)

    
    def new_order(self,request:NewOrderRequest):
        if request.side.lower() == "buy":
            side = quickfix.Side_BUY
        else:
            side = quickfix.Side_SELL

        message = quickfix.Message()
        header = message.getHeader()
        header.setField(quickfix.MsgType("D"))
        message.setField(quickfix.ClOrdID(self.genExecID()))
        message.setField(quickfix.Symbol(request.symbol))
        message.setField(quickfix.Side(side))
        message.setField(quickfix.Price(float(request.price)))
        if request.order_type.lower() == "market":
            message.setField(quickfix.OrdType(quickfix.OrdType_MARKET))
        else:
            message.setField(quickfix.OrdType(quickfix.OrdType_LIMIT))
        message.setField(quickfix.HandlInst(quickfix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        message.setField(quickfix.TransactTime())
        message.setField(quickfix.OrderQty(float(request.quantity)))
        message.setField(quickfix.Text(f"{side} {request.symbol} {request.quantity}@{request.price}"))

        quickfix.Session.sendToTarget(message, self.sessionID)
        
    def replace_order(self,request:ReplaceOrderRequest):
        if request.side.lower() == "buy":
            side = quickfix.Side_BUY
        else:
            side = quickfix.Side_SELL

        message = quickfix43.OrderCancelReplaceRequest()
        message.setField(quickfix.OrigClOrdID(request.orig_client_order_id))
        message.setField(quickfix.ClOrdID(self.genExecID()))
        message.setField(quickfix.Symbol(request.symbol))
        message.setField(quickfix.Side(side))
        message.setField(quickfix.Price(float(request.price)))
        message.setField(quickfix.OrdType(quickfix.OrdType_LIMIT))
        message.setField(quickfix.HandlInst(quickfix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        message.setField(quickfix.TransactTime())
        message.setField(quickfix.OrderQty(float(request.quantity)))
        message.setField(quickfix.Text(f"{request.side} {request.symbol} {request.quantity}@{request.price}"))

        quickfix.Session.sendToTarget(message, self.sessionID)

    def delete_order(self,request:DeleteOrderRequest):
        if request.side.lower() == "buy":
            side = quickfix.Side_BUY
        else:
            side = quickfix.Side_SELL
      
        message = quickfix43.OrderCancelRequest()
        message.setField(quickfix.OrigClOrdID(request.orig_client_order_id))
        message.setField(quickfix.ClOrdID(self.genExecID()))
        message.setField(quickfix.Symbol(request.symbol))
        message.setField(quickfix.Side(side))
        message.setField(quickfix.TransactTime())
        message.setField(quickfix.Text(f"Delete {request.orig_client_order_id}")) 

        quickfix.Session.sendToTarget(message, self.sessionID)


class Application(quickfix.Application,BusinessOperation):
    """FIX Application"""

    execID = 0
    def onCreate(self, sessionID):
        self.sessionID = sessionID
        self.log_info("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        self.log_info("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        self.log_info("Session (%s) logout !" % sessionID.toString())
        return
        
    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(App) S >> %s" % msg)
        return
        
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass
