from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    CANCELLED = "Cancelled"
    REVERTED = "Reverted"


class SalesTransaction(Base):
    __tablename__ = "sales_transactions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    payments = relationship("Payment", back_populates="transaction")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, nullable=False, index=True)
    transaction_id = Column(Integer, ForeignKey("sales_transactions.id"))
    amount = Column(Integer)
    status = Column(Enum(PaymentStatus))
    created_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("SalesTransaction", back_populates="payments")
