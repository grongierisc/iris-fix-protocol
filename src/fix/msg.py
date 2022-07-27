from dataclasses import dataclass
from grongier.pex import Message

from obj import MessageField,HeaderField,GroupField

@dataclass
class Request(Message):
    header_field:HeaderField = None
    message_field:MessageField = None
    group_field:GroupField = None

@dataclass
class Response(Message):
    header_field:HeaderField = None
    message_field:MessageField = None
    group_field:GroupField = None
    msg:str = None

@dataclass
class MarketResponse(Message):
    pass