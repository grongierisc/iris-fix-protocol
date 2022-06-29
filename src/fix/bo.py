
from grongier.pex import BusinessOperation
from datetime import datetime
import quickfix
__SOH__ = chr(1)

class FixBusinessOperation(BusinessOperation):
    def on_init(self):
        try:
            # We create a SessionSettings and get it's settings dict
            session_settings = quickfix.SessionSettings()
            settings_dict = session_settings.get()
            
            # We get all the attr that are in self but not in the base BusinessOperation class
            config_attr = set(dir(self)).difference(set(dir(BusinessOperation))).difference(set(['new_order']))

            # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
            for attr in config_attr:
                settings_dict.setString(attr,getattr(self, attr))

            # We set our session with the session IDs and the settings we want for it
            session_settings.set(quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID),settings_dict)

            # Create our Application and apply our sessions_settings
            self.application = Application()
            storefactory = quickfix.FileStoreFactory(session_settings)
            logfactory = quickfix.FileLogFactory(session_settings)
            self.initiator = quickfix.SocketInitiator(self.application, storefactory, session_settings, logfactory)

            # Start the initiator
            self.initiator.start()


        except (quickfix.ConfigError, quickfix.RuntimeError) as e:
            if hasattr(self,'initiator'):
                self.initiator.stop()
            raise e
            

    def on_tear_down(self):
        self.initiator.stop()

    def on_message(self, request):
        pass
    
    def new_order(self,request:NewOrderRequest):
        self.application.put_new_order(request)
        
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

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def new_order(self,request:NewOrderRequest):
        sender_comp_id, target_comp_id, symbol, quantity, price, side, order_type = ""

        if side.lower() == "buy":
            side = quickfix.Side_BUY
        else:
            side = quickfix.Side_SELL

        message = quickfix.Message()
        header = message.getHeader()
        header.setField(quickfix.BeginString("FIX.4.2"))
        header.setField(quickfix.SenderCompID(sender_comp_id))
        header.setField(quickfix.TargetCompID(target_comp_id))
        header.setField(quickfix.MsgType("D"))
        #ord_id = get_order_id(sender_comp_id, symbol)
        message.setField(quickfix.ClOrdID(ord_id))
        message.setField(quickfix.Symbol(symbol))
        message.setField(quickfix.Side(side))
        message.setField(quickfix.Price(float(price)))
        if order_type.lower() == "market":
            message.setField(quickfix.OrdType(quickfix.OrdType_MARKET))
        else:
            message.setField(quickfix.OrdType(quickfix.OrdType_LIMIT))
        message.setField(quickfix.HandlInst(quickfix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        message.setField(quickfix.TransactTime())
        message.setField(quickfix.OrderQty(float(quantity)))
        message.setField(quickfix.Text(f"{side} {symbol} {quantity}@{price}"))

        return message

    def put_new_order(self):
        """Request sample new order single"""
        message = quickfix.Message()
        header = message.getHeader()

        header.setField(quickfix.MsgType(quickfix.MsgType_NewOrderSingle)) #39 = D 

        message.setField(quickfix.ClOrdID(self.genExecID())) #11 = Unique Sequence Number
        message.setField(quickfix.Side(quickfix.Side_BUY)) #43 = 1 BUY 
        message.setField(quickfix.Symbol("MSFT")) #55 = MSFT
        message.setField(quickfix.OrderQty(10000)) #38 = 1000
        message.setField(quickfix.Price(100))
        message.setField(quickfix.OrdType(quickfix.OrdType_LIMIT)) #40=2 Limit Order 
        message.setField(quickfix.HandlInst(quickfix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
        message.setField(quickfix.TimeInForce('0'))
        message.setField(quickfix.Text("NewOrderSingle"))
        trstime = quickfix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)

        quickfix.Session.sendToTarget(message, self.sessionID)
