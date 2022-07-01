from grongier.pex import OutboundAdapter
from grongier.pex import InboundAdapter

print(set(dir(InboundAdapter)).difference(set(dir(OutboundAdapter))))