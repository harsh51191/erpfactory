from dataclasses import dataclass, replace
from .policy import Grant, authorize

@dataclass(frozen=True)
class PR:
    id: str
    quantity: int
    delivery_date: str
    version: int = 1
    status: str = "open"

class MockERP:
    def __init__(self, records: list[PR]):
        self.records = {r.id: r for r in records}
        self.receipts = {}
    def read(self, grant: Grant, key: str) -> PR:
        authorize(grant, "synthetic", "pr.read")
        return self.records[key]
    def update_quantity(self, grant: Grant, key: str, qty: int,
                        expected_version: int, token: str) -> PR:
        authorize(grant, "synthetic", "pr.update")
        if not token or type(qty) is not int or qty <= 0:
            raise ValueError("Invalid request")
        request = (key, qty, expected_version)
        if token in self.receipts:
            previous, result = self.receipts[token]
            if previous != request:
                raise ValueError("Idempotency conflict")
            return result
        old = self.records[key]
        if old.status != "open" or old.version != expected_version:
            raise ValueError("Closed or stale PR")
        updated = replace(old, quantity=qty, version=old.version + 1)
        self.records[key] = updated
        self.receipts[token] = (request, updated)
        return updated
