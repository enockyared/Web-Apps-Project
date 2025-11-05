from typing import Optional
from app.domain.user import User
from app.domain.security import Security


users: dict[str, User] = {}
portfolios: dict[str, list] = {}
securities: dict[str, Security] = {}

logged_in_user: Optional[User] = None
next_portfolio_id: int = 1

# 
# ADMIN USER (ENOCK YARED)
# 
admin = User("Enock", "Yared", "eyared", "admin123", 25000.00)
users[admin.username] = admin


securities["AAPL"] = Security("AAPL", "Apple Inc.", 172.45, 10000)
securities["MSFT"] = Security("MSFT", "Microsoft Corp.", 320.10, 8000)
securities["GOOG"] = Security("GOOG", "Alphabet Inc.", 140.80, 12000)


def add_user(user: User) -> None:
    users[user.username] = user

def get_user(username: str) -> Optional[User]:
    return users.get(username)

def set_logged_in_user(user: Optional[User]) -> None:
    global logged_in_user
    logged_in_user = user

def get_next_portfolio_id() -> int:
    global next_portfolio_id
    pid = next_portfolio_id
    next_portfolio_id += 1
    return pid
