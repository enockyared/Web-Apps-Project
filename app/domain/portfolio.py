from app.domain.investment import Investment

class Portfolio:
    def __init__(self, id: int, name: str, description: str, balance: float = 0.0):
        self.id = id
        self.name = name
        self.description = description
        self.balance = balance
        self.holdings: list[Investment] = []

    def add_investment(self, investment: Investment):
        self.holdings.append(investment)

    def remove_investment(self, ticker: str):
        self.holdings = [i for i in self.holdings if i.ticker != ticker]

    def __repr__(self):
        return f"Portfolio({self.id}: {self.name}, Balance: ${self.balance:.2f})"
