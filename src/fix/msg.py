from dataclasses import dataclass
from grongier.pex import Message

@dataclass
class NewOrderRequest(Message):
    symbol:str = None
    quantity:str = None
    price:str = None
    side:str = None
    order_type:str = None