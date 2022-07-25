from dataclasses import dataclass
from grongier.pex import Message

@dataclass
class OrderRequest(Message):
    symbol:str = None
    quantity:str = None
    price:str = None
    side:str = None
    ord_type:str = None
    currency:str = None
    exec_inst:str = None
    time_in_force:str = None
    min_qty:str = None
    quote_id:str = None

@dataclass
class QuoteRequest(Message):
    symbols:str = None
    comm_type:str = None
    ord_type:str = None

@dataclass
class FixResponse(Message):
    pass

@dataclass
class MarketResponse(Message):
    pass