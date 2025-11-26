from app.domain.user import User

def test_create_user(db):
    user = User(first_name="Enock", last_name="Yared", username="eyared", password="pass", balance=500)
    db.add(user)
    db.commit()

    saved = db.query(User).filter_by(username="eyared").first()
    assert saved is not None
    assert saved.username == "eyared"
    assert saved.balance == 500

def test_user_repr(db):
    user = User(first_name="A", last_name="B", username="ab", password="123", balance=100)
    assert "ab" in repr(user)
