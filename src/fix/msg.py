from dataclasses import dataclass
from grongier.pex import Message

@dataclass
class Request(Message):
    pass

@dataclass
class QuoteRequest(Message):
    pass

@dataclass
class FixResponse(Message):
    pass

@dataclass
class MarketResponse(Message):
    pass