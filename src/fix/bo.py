
from grongier.pex import BusinessOperation
from datetime import datetime
import quickfix
__SOH__ = chr(1)

class FixBusinessOperation(BusinessOperation):
    def on_init(self):
        try:
            if not hasattr(self,'config_file'):
                config_file='/irisdev/app/src/fix/client.cfg'
            settings = quickfix.SessionSettings(config_file)
            self.application = Application()
            storefactory = quickfix.FileStoreFactory(settings)
            logfactory = quickfix.FileLogFactory(settings)
            self.initiator = quickfix.SocketInitiator(self.application, storefactory, settings, logfactory)

            self.initiator.start()
            
        except (quickfix.ConfigError, quickfix.RuntimeError) as e:
            if hasattr(self,'initiator'):
                self.initiator.stop()
            raise e
            

    def on_tear_down(self):
        self.initiator.stop()

    def on_message(self, request):
        self.application.put_new_order()
        
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

if __name__ == '__main__':
    bo = FixBusinessOperation()
    bo.on_init()
    bo.on_message('')