from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    status: str
    transaction_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
