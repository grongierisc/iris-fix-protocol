
from grongier.pex import BusinessOperation
from datetime import datetime
import quickfix
__SOH__ = chr(1)

class FixBusinessOperation(BusinessOperation):
    def on_init(self):
        try:
            # We gather the base information of the session : the ids
            # Note : If a new session is created it needs to be added to the acceptor or nothing will happen ( shouldn't be done automatically or it will break the point of having an acceptor )
            if not hasattr(self,'config_file'):
                self.config_file='/irisdev/app/src/fix/client.cfg'
            if not hasattr(self,"BeginString"):
                self.BeginString = "FIX.4.3"
            if not hasattr(self,"SenderCompID"):
                self.SenderCompID = "CLIENT"
            if not hasattr(self,"TargetCompID"):
                self.TargetCompID = "SERVER"
            
            # We open our base config file and modify it's session to match ours
            list_of_lines = []
            with open(self.config_file, "r") as config_file:
                list_of_lines = config_file.readlines()

                for i in range(len(list_of_lines)):
                    if list_of_lines[i] == "BeginString=FIX.4.3\n":
                        list_of_lines[i] = "BeginString={}\n".format(self.BeginString)
                    elif list_of_lines[i] == "SenderCompID=CLIENT\n":
                        list_of_lines[i] = "SenderCompID={}\n".format(self.SenderCompID)
                    elif list_of_lines[i] == "TargetCompID=SERVER\n":
                        list_of_lines[i] = "TargetCompID={}\n".format(self.TargetCompID)

            tmp_name = "tmp.cfg"
            with open(tmp_name,"w") as tmp_config_file:
                tmp_config_file.writelines(list_of_lines)

            # We get the SessionsSettings ( with the right session )
            settings = quickfix.SessionSettings(tmp_name)

            # We get the mutable object of the settings ( reference and not copy ) using the session ids
            session_settings = settings.get(quickfix.SessionID(self.BeginString,self.SenderCompID,self.TargetCompID))

            # We get all the attr that are in self but not in the base BusinessOperation class and are not the ids
            base_attr = set(dir(BusinessOperation))
            other_attr = set(("config_file","beginString","senderCompID",'targetCompID'))
            config_attr = set(dir(self)).difference(base_attr)
            config_attr = config_attr.difference(other_attr)

            # For every one of them we add them to the settings using the setString method ( replace it if exists, create it if not)
            # See if it works with int like for "ReconnectInterval"
            for attr in config_attr:
                session_settings.setString(attr,getattr(self, attr))

            # Create our Application and apply our settings
            self.application = Application()
            storefactory = quickfix.FileStoreFactory(settings)
            logfactory = quickfix.FileLogFactory(settings)
            self.initiator = quickfix.SocketInitiator(self.application, storefactory, settings, logfactory)

            # Start the initiator
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