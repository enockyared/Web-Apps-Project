from app.domain.transaction import TradeTransaction
from datetime import datetime

def test_transaction_logging(db):
    transaction = TradeTransaction(
        type="BUY",
        symbol="AAPL",
        quantity=5,
        price=100.0,
        total=500.0,
        user_id=1,
        portfolio_id=1
    )

    db.add(transaction)
    db.commit()

    saved = db.query(TradeTransaction).first()
    assert saved.type == "BUY"
    assert saved.total == 500.0
    assert saved.symbol == "AAPL"
def test_transaction_repr(db):
    tx = TradeTransaction(type="BUY", symbol="AAPL", quantity=1, price=100, total=100, user_id=1, portfolio_id=1)
    assert tx.total == 100
