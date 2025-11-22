from sqlalchemy import Column, Integer, String, Float
from app.database.config import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    balance = Column(Float)

    portfolios = relationship("Portfolio", back_populates="user")
    transactions = relationship("TradeTransaction", back_populates="user")

    def __init__(self, first_name, last_name, username, password, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.balance = balance

    def __repr__(self):
        return f"User({self.username}, Balance: ${self.balance:.2f})"
