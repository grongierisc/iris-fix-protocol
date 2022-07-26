from dataclasses import dataclass
from grongier.pex import Message

from obj import MessageField,HeaderField,GroupField

@dataclass
class Request(Message):
    message_field:MessageField = None
    header_field:HeaderField = None
    group_field:GroupField = None

@dataclass
class Response(Message):
    pass

@dataclass
class MarketResponse(Message):
    pass