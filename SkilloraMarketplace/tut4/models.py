from dataclasses import dataclass, field

@dataclass
class Order:
    id: str
    customer_id: str
    address: str
    items: list
    status: str = "pending"
    total: float = 0.0
    version: int = 1
    secret_internal_note: str = field(default="internal", repr=False)

    def as_json(self):
        return {
            "id": self.id,
            "customerId": self.customer_id,
            "address": self.address,
            "items": self.items,
            "status": self.status,
            "total": self.total,
            "version": self.version
        }
