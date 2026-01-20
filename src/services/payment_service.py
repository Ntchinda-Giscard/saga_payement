import uuid
from sqlalchemy.orm import Session
from ..database.models import Payment
from ..schemas.payment_schema import PaymentCreate

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    # Updated process_payment signature in payment_routes.py needs to pass token/user_id if we want verification
    def process_payment(self, payment_data: PaymentCreate, token: str = None, user_id: int = None):
        # 1. Verify Booking exists and belongs to user (optional strictly, but good practice)
        from ..clients.user_client import UserClient
        user_client = UserClient()
        
        # We need the token to verify the booking ownership if we enforce it.
        # The user_client.get_booking uses the token.
        booking = None
        if token:
            booking = user_client.get_booking(payment_data.booking_id, token)
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found or access denied")
            if user_id and booking.get('user_id') != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to pay for this booking")

        # 2. Process Payment (Mock)
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
        
        # 3. Confirm Booking
        user_client.confirm_booking(payment_data.booking_id)

        # 4. Send Notification
        from ..clients.notification_client import NotificationClient
        try:
            notif_client = NotificationClient()
            notif_client.send_notification(
                user_id=user_id if user_id else 0, # Fallback
                message=f"Payment Successful for Booking {payment_data.booking_id}. Transaction ID: {transaction_id}",
                notification_type="EMAIL"
            )
        except:
            pass # Don't fail payment if notification fails
            
        return new_payment

    def get_payment(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
