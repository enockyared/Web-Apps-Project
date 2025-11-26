from sqlalchemy import Column, Integer, String, Float
from app.database.config import Base

class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, nullable=False)
    issuer = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    available_qty = Column(Integer, nullable=False)

    def __init__(self, symbol, issuer, price, available_qty):
        self.symbol = symbol
        self.issuer = issuer
        self.price = price
        self.available_qty = available_qty

    def __repr__(self):
        return f"{self.symbol} ({self.issuer}) - ${self.price:.2f} | Available: {self.available_qty}"