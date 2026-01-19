import uuid
from sqlalchemy.orm import Session
from ..database.models import Payment
from ..schemas.payment_schema import PaymentCreate

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def process_payment(self, payment_data: PaymentCreate):
        # Mock payment processing logic
        # In real life, integrate with Stripe/PayPal here.
        
        transaction_id = str(uuid.uuid4())
        
        new_payment = Payment(
            booking_id=payment_data.booking_id,
            amount=payment_data.amount,
            status="SUCCESS",
            transaction_id=transaction_id
        )
        self.db.add(new_payment)
        self.db.commit()
        self.db.refresh(new_payment)
        return new_payment

    def get_payment(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
