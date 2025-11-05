class User:
    def __init__(self, first_name: str, last_name: str, username: str, password: str, balance: float):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.balance = balance

    def __repr__(self):
        return f"User({self.username}, Balance: ${self.balance:.2f})"
