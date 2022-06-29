from dataclasses import dataclass
from grongier.pex import Message

@dataclass
class NewOrderRequest(Message):
    symbol:str = None
    quantity:str = None
    price:str = None
    side:str = None
    order_type:str = None

@dataclass
class ReplaceOrderRequest(Message):
    symbol:str = None
    quantity:str = None
    price:str = None
    side:str = None
    orig_client_order_id:str = None

@dataclass
class DeleteOrderRequest(Message):
    symbol:str = None
    side:str = None
    orig_client_order_id:str = None
