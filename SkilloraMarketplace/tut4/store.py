from tut4.models import Order

# Simple in-memory storage
ORDERS = {}
IDEMPOTENCY = {}

def create(order: Order):
    ORDERS[order.id] = order

def get(order_id: str):
    return ORDERS.get(order_id)

def all():
    return list(ORDERS.values())
