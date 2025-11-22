from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    security_symbol = Column(String(10), nullable=False)  
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)

    portfolio = relationship("Portfolio", back_populates="investments")

    def __init__(self, portfolio_id, security_symbol, quantity, purchase_price):
        self.portfolio_id = portfolio_id
        self.security_symbol = security_symbol
        self.quantity = quantity
        self.purchase_price = purchase_price

    def __repr__(self):
        return f"{self.security_symbol} - Qty: {self.quantity} @ ${self.purchase_price:.2f}"