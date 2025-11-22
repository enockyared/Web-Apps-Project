from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.config import Base

class TradeTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    security_symbol = Column(String(10), nullable=False)
    transaction_type = Column(String(10), nullable=False) 
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    portfolio = relationship("Portfolio")
    
    def __init__(self, user_id, portfolio_id, security_symbol, quantity, price, transaction_type):
        self.user_id = user_id
        self.portfolio_id = portfolio_id
        self.security_symbol = security_symbol
        self.quantity = quantity
        self.price = price
        self.transaction_type = transaction_type