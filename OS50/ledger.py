"""Virtual OS50 trade ledger. This module NEVER connects to a broker."""
from dataclasses import dataclass, field
from decimal import Decimal


def D(value):
    return Decimal(str(value))


DIVISIONS = ("Trend", "Momentum", "Breakout", "Volatility", "Risk")


@dataclass
class PaperLedger:
    cash: Decimal = D("50")
    qty: Decimal = D("0")
    entry_spent: Decimal = D("0")
    realized_net: Decimal = D("0")
    reserves: dict = field(default_factory=lambda: {name: D("0") for name in DIVISIONS})
    commission: Decimal = D("0.008")
    slippage: Decimal = D("0.001")
    n_born: int = 0

    def reserve_total(self):
        return sum(self.reserves.values(), D("0"))

    def equity(self, price):
        """Conservative marked-liquidation equity (estimated exit costs included)."""
        px = D(price)
        if px <= 0:
            raise ValueError("Price must be positive")
        position_proceeds = self.qty * px * (D("1") - self.slippage) * (D("1") - self.commission)
        return self.cash + self.reserve_total() + position_proceeds

    def buy(self, amount, price):
        amount, price = D(amount), D(price)
        if amount <= 0 or price <= 0 or self.qty != 0 or amount > self.cash:
            raise ValueError("Invalid order size, price, or existing position")
        fee = amount * self.commission
        effective_price = price * (D("1") + self.slippage)
        self.qty = (amount - fee) / effective_price
        self.cash -= amount
        self.entry_spent = amount

    def sell(self, price):
        price = D(price)
        if price <= 0 or self.qty <= 0:
            raise ValueError("No position or invalid price")
        gross = self.qty * price * (D("1") - self.slippage)
        proceeds = gross * (D("1") - self.commission)
        trade_net = proceeds - self.entry_spent
        self.cash += proceeds
        self.qty = D("0")
        self.entry_spent = D("0")
        self.realized_net += trade_net
        self.allocate_children()
        return trade_net

    def allocate_children(self):
        # Ledger transfer ONLY. A losing trade reduces realized_net,
        # so losses must be recovered before creating any new child reserve.
        while self.realized_net - self.reserve_total() >= D("1") and self.cash >= D("1"):
            name = DIVISIONS[self.n_born % len(DIVISIONS)]
            self.reserves[name] += D("1")
            self.cash -= D("1")
            self.n_born += 1

    def deposit_virtual(self, amount):
        amount = D(amount)
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.cash += amount

    def withdraw_virtual(self, amount):
        amount = D(amount)
        if amount <= 0 or amount > self.cash:
            raise ValueError("Cannot withdraw more than unreserved cash")
        self.cash -= amount

    def reconcile_when_flat(self, net_external_flows=D("0")):
        if self.qty:
            raise ValueError("Cannot use flat reconciliation with an open position")
        return self.cash + self.reserve_total() - (D("50") + D(net_external_flows) + self.realized_net)
