from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..services.payment_service import PaymentService
from ..schemas.payment_schema import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

def get_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db)

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(
    payment_data: PaymentCreate,
    service: PaymentService = Depends(get_service)
):
    """
    Process a payment for a booking.
    """
    return service.process_payment(payment_data)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_service)
):
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
