from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))  
    balance = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to User
    user = relationship("User", back_populates="portfolios")
    investments = relationship("Investment", back_populates="portfolio")

    def __init__(self, name, description, balance, user_id):
        self.name = name
        self.description = description
        self.balance = balance
        self.user_id = user_id

    def __repr__(self):
        return f"Portfolio({self.name}, Balance: ${self.balance:.2f})"