from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .session import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="SUCCESS")
    transaction_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
