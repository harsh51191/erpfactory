import json
from dataclasses import asdict
from .mock import MockERP, PR
from .policy import Grant
from .graph import Edge, impact

def main():
    grant = Grant("synthetic", frozenset({"pr.read", "pr.update"}), True)
    erp = MockERP([PR("SYN-1", 100, "2027-01-15")])
    before = erp.read(grant, "SYN-1")
    erp.update_quantity(grant, "SYN-1", 120, before.version, "demo-1")
    after = erp.read(grant, "SYN-1")
    assert after.quantity == 120 and before.delivery_date == after.delivery_date
    print(json.dumps({"environment":"synthetic", "before":asdict(before),
        "after":asdict(after), "impact":impact("PR", [Edge("PR","approval","may-trigger","synthetic fixture"), Edge("approval","PO","may-affect","synthetic fixture")])}, indent=2))

if __name__ == "__main__":
    main()
