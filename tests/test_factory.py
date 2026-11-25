import unittest
from erpfactory.policy import Grant, authorize
from erpfactory.mock import MockERP, PR
from erpfactory.graph import Edge, impact

class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.g = Grant("synthetic", frozenset({"pr.read", "pr.update"}), True)
        self.erp = MockERP([PR("a", 100, "2027-01-15"), PR("b", 20, "2027-02-01", status="closed")])
    def test_update_preserves_date_and_other_record(self):
        other = self.erp.read(self.g,"b")
        a = self.erp.update_quantity(self.g,"a",120,1,"t")
        self.assertEqual((a.quantity,a.delivery_date,a.version),(120,"2027-01-15",2))
        self.assertEqual(other,self.erp.read(self.g,"b"))
    def test_idempotency(self):
        a=self.erp.update_quantity(self.g,"a",120,1,"t")
        self.assertEqual(a,self.erp.update_quantity(self.g,"a",120,1,"t"))
        with self.assertRaises(ValueError):
            self.erp.update_quantity(self.g,"a",121,1,"t")
    def test_stale_closed_invalid(self):
        self.erp.update_quantity(self.g,"a",120,1,"t")
        for key, qty, version in [("a",130,1),("b",50,1),("a",-1,2)]:
            with self.assertRaises(ValueError):
                self.erp.update_quantity(self.g,key,qty,version,"new")
    def test_production_denied(self):
        with self.assertRaises(PermissionError):
            authorize(Grant("prod",frozenset({"pr.update"}),True),"prod","pr.update")
    def test_unapproved_denied(self):
        with self.assertRaises(PermissionError):
            self.erp.update_quantity(Grant("synthetic",frozenset({"pr.update"})), "a",120,1,"t")
    def test_read_only_denied(self):
        with self.assertRaises(PermissionError):
            self.erp.update_quantity(Grant("synthetic",frozenset({"pr.read"}),True),"a",120,1,"t")
    def test_transitive_cycle(self):
        r=impact("PR",[Edge("PR","approval","trigger","fixture"),Edge("approval","PO","dependency","fixture"),Edge("PO","PR","cycle","fixture")])
        self.assertEqual(r["affected"],["PO","approval"])
        self.assertTrue(r["requires_review"])
    def test_missing_evidence(self):
        with self.assertRaises(ValueError):
            impact("PR",[Edge("PR","PO","dependency","")])

if __name__ == "__main__":
    unittest.main()
