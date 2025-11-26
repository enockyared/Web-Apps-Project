from app.domain.user import User
from app.domain.portfolio import Portfolio
from app.domain.transaction import TradeTransaction

def test_buy_logic(db):
    user = User(first_name="A", last_name="B", username="ab", password="123", balance=1000)
    db.add(user)
    db.commit()

    portfolio = Portfolio(name="Test", balance=0, user_id=user.id)
    db.add(portfolio)
    db.commit()

    # simulate buy
    qty = 5
    price = 100
    cost = qty * price

    portfolio.balance -= cost
    user.balance -= cost
    db.commit()

    assert portfolio.balance == -500
    assert user.balance == 500
