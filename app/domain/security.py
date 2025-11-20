class Security:
    def __init__(self, ticker: str, issuer: str, price: float, available_quantity: int):
        self.ticker = ticker
        self.issuer = issuer
        self.price = price
        self.available_quantity = available_quantity

    def __repr__(self):
        return f"{self.ticker} ({self.issuer}) - ${self.price:.2f} | Available: {self.available_quantity}"
