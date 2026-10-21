import unittest
from decimal import Decimal
from ledger import PaperLedger, D, DIVISIONS


class PaperLedgerTests(unittest.TestCase):
    def test_buy_fees_and_sell_reconciliation(self):
        x = PaperLedger()
        x.buy(20, 100)
        self.assertLess(x.equity(100), D("50"))
        profit = x.sell(102)
        self.assertLess(profit, D("0.4"))
        self.assertEqual(x.reconcile_when_flat(), D("0"))

    def test_losses_reduce_real_capital(self):
        x = PaperLedger()
        x.buy(20, 100)
        loss = x.sell(99)
        self.assertLess(loss, 0)
        self.assertLess(x.equity(99), D("50"))
        self.assertEqual(x.n_born, 0)
        self.assertEqual(x.reconcile_when_flat(), D("0"))

    def test_children_transfer_not_multiply_money(self):
        x = PaperLedger()
        x.buy(20, 100)
        x.sell(120)
        self.assertGreaterEqual(x.n_born, 1)
        self.assertEqual(x.reserve_total(), D(x.n_born))
        self.assertEqual(x.reconcile_when_flat(), D("0"))
        self.assertLess(x.cash, D("50") + x.realized_net)

    def test_five_child_divisions_round_robin(self):
        x = PaperLedger()
        x.buy(20, 100)
        x.sell(150)
        self.assertGreaterEqual(x.n_born, 5)
        self.assertEqual(x.reserves["Trend"], D("2"))
        self.assertEqual(x.reserves["Momentum"], D("2"))
        self.assertEqual(x.reserves["Breakout"], D("2"))
        self.assertEqual(x.reserves["Volatility"], D("2"))
        self.assertEqual(x.reserves["Risk"], D("1"))

    def test_loss_must_be_recovered_before_another_birth(self):
        x = PaperLedger()
        x.buy(20, 100)
        x.sell(120)
        before = x.n_born
        x.buy(20, 100)
        x.sell(90)
        self.assertEqual(x.n_born, before)
        self.assertEqual(x.reconcile_when_flat(), D("0"))

    def test_reject_overspend_and_double_entry(self):
        x = PaperLedger()
        with self.assertRaises(ValueError):
            x.buy(100, 100)
        x.buy(10, 100)
        with self.assertRaises(ValueError):
            x.buy(10, 100)

    def test_virtual_external_flows_keep_reserves_separate(self):
        x = PaperLedger()
        x.deposit_virtual(5)
        x.withdraw_virtual(2)
        self.assertEqual(x.reconcile_when_flat(D("3")), D("0"))
        with self.assertRaises(ValueError):
            x.withdraw_virtual(1000)


if __name__ == "__main__":
    unittest.main()
