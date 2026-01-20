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

from fastapi.security import OAuth2PasswordBearer
from fastapi import Header

# OAuth scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/users/login")

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def process_payment(
    payment_data: PaymentCreate,
    service: PaymentService = Depends(get_service),
    token: str = Depends(oauth2_scheme)
):
    """
    Process a payment for a booking. Requires valid Auth Token.
    """
    # Decode token to get user_id (using our auth module in PaymentService)
    from ..auth import get_current_user_id
    user_id = get_current_user_id(token)
    
    return service.process_payment(payment_data, token, user_id)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_service)
):
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
