from prettytable import PrettyTable


class Book:
    def __init__(self, symbol, bids, asks, trades):
        self.symbol = symbol
        self.bids = bids
        self.asks = asks
        self.trades = trades

    def __str__(self):
        res = ""
        table = PrettyTable()

        if len(self.asks) > len(self.bids):
            diff = len(self.asks) - len(self.bids)
            while diff:
                self.bids.append(("Empty", "Empty"))
                diff -= 1
        elif len(self.bids) > len(self.asks):
            diff = len(self.bids) - len(self.asks)
            while diff:
                self.asks.append(("Empty", "Empty"))
                diff -= 1

        table.add_column("bid_prc, bid_qty", self.bids)
        table.add_column("ask_prc, ask_qty", self.asks)

        res += f"Symbol: {self.symbol}\n"
        res += table.get_string() + "\n"

        for trade in self.trades:
            res += f"Trade {self.symbol}, {trade[1]}@{trade[0]}.\n"

        return res
