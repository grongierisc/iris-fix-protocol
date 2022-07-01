from grongier.pex import OutboundAdapter

class ApplicationAdapter(OutboundAdapter):
    """
    This adapter is used to hold the quickfix application & more
    name : Python.ApplicationAdapter
    """

    def on_init(self):
        pass

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
