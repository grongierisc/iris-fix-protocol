from grongier.pex import BusinessService
from msg import HeartBeatRequest

class HeartBeatService(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_process_input(self, request):
        self.send_request_sync("Python.FixBusinessOperation",HeartBeatRequest())