from grongier.pex import BusinessOperation

import time

import quickfix
import quickfix43

from msg import NewOrderRequest,ReplaceOrderRequest,DeleteOrderRequest

__SOH__ = chr(1)

class FixBusinessOperation(quickfix.Application,BusinessOperation):
    def on_init(self):
        try:
            # We create a SessionSettings and get it's settings dict
            session_settings = quickfix.SessionSettings()
            settings_dict = session_settings.get()
            
            # We get all the attr that are in self but not in the base BusinessOperation class
            config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['this','new_order','genExecID','replace_order','delete_order','onMessage'])).difference(set(dir(quickfix.Application)))

            # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
            for attr in config_attr:
                self.log_info(attr + str(getattr(self,attr)))
                settings_dict.setString(attr,getattr(self, attr))

            self.sessionID = quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID)

            # We set our session with the session IDs and the settings we want for it
            session_settings.set(self.sessionID,settings_dict)

            # Create our Application and apply our sessions_settings
            storefactory = quickfix.FileStoreFactory(session_settings)
            logfactory = quickfix.FileLogFactory(session_settings)
            self.initiator = quickfix.SocketInitiator(self, storefactory, session_settings, logfactory)

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

    def new_order(self,request:NewOrderRequest):
        
        time.sleep(2)

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
        time.sleep(2)
        return 
        
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

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

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
        #self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID=None):
        msg = message.toString().replace(__SOH__, "|")
        self.log_info("onMessage >< %s" % msg)

if __name__ == '__main__':
    bo = FixBusinessOperation()
    bo.BeginString='FIX.4.3'
    bo.SenderCompID='CLIENT'
    bo.TargetCompID='SERVER'
    bo.HeartBtInt='5'
    bo.SocketConnectPort='3000'
    bo.SocketConnectHost='acceptor'
    bo.DataDictionary='/irisdev/app/src/fix/spec/FIX43.xml'
    bo.FileStorePath='/irisdev/app/src/fix/Sessions/'
    bo.ConnectionType='initiator'
    bo.FileLogPath='./Logs/'
    bo.StartTime='00:00:00'
    bo.EndTime='00:00:00'
    bo.ReconnectInterval='60'
    bo.LogoutTimeout='30'
    bo.LogonTimeout='30'
    bo.ResetOnLogon='Y'
    bo.ResetOnLogout='Y'
    bo.ResetOnDisconnect='Y'
    bo.SendRedundantResendRequests='Y'
    bo.SocketNodelay='N'
    bo.ValidateUserDefinedFields='N'
    bo.ValidateFieldsOutOfOrder='N'
    bo.on_init()

    nostop = True
    while nostop:
        #bo.artificial_heart_beat(HeartBeatRequest())
        nb = input("0 stop, 1 to new order buy, 2 to delete order, ")
        if nb == "1":
            msg = NewOrderRequest()
            msg.order_type = "limit"
            msg.symbol = "MSFT"
            msg.price = "100"
            msg.quantity = "10000"
            msg.side = "buy"
            bo.new_order(msg)
        elif nb == "2":
            msg = DeleteOrderRequest()
            msg.order_type = "limit"
            msg.side = "buy"
            msg.symbol = "MSFT"
            msg.orig_client_order_id = "00001"
            bo.delete_order(msg)
        else:
            nostop = not nostop
    