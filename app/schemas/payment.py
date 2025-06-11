from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime


class PaymentStatus(str, Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    CANCELLED = "Cancelled"
    REVERTED = "Reverted"


class PaymentRequest(BaseModel):
    amount: int
    transaction_id: int


class PaymentResponse(BaseModel):
    request_id: str
    status: PaymentStatus
    amount: int | None = None
    reason: str | None = None


class PaymentOut(BaseModel):
    request_id: str
    amount: int | None = None
    status: PaymentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
