from app.domain.portfolio import Portfolio
from app.domain.user import User

def test_create_portfolio(db):
    user = User(first_name="Test", last_name="User", username="testuser", password="pass", balance=1000)
    db.add(user)
    db.commit()

    portfolio = Portfolio(name="Tech", balance=500, user_id=user.id)
    db.add(portfolio)
    db.commit()

    saved = db.query(Portfolio).filter_by(name="Tech").first()
    assert saved is not None
    assert saved.user_id == user.id
    assert saved.balance == 500

def test_portfolio_repr(db):
    p = Portfolio(name="test", description="d", balance=1000, user_id=1)
    assert "test" in repr(p)
