from fastapi import APIRouter, HTTPException
from app.schemas.payment import PaymentRequest, PaymentResponse, PaymentStatus, PaymentOut
from app.schemas.transaction import TransactionResponse
from app.schemas.revert import RevertRequest
from app.db.models import Payment, SalesTransaction
from app.db.database import SessionLocal
from uuid import uuid4
from typing import List
from puc_payment_provider import payment as provider_payment
from puc_payment_provider import revert as provider_revert
from datetime import datetime
import json
from fastapi.responses import JSONResponse
from fastapi import Path

router = APIRouter()


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction():
    db = SessionLocal()
    try:
        tx = SalesTransaction(created_at=datetime.utcnow())
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return {"transaction_id": tx.id}
    finally:
        db.close()


@router.post("/payment", response_model=PaymentResponse)
def make_payment(request: PaymentRequest):
    db = SessionLocal()
    request_id = str(uuid4())

    try:
        # Call the simulated provider
        response_json = provider_payment(request.amount, request_id)
        response = json.loads(response_json)

        # Determine status
        status = response.get("status")
        amount = response.get("amount")
        reason = response.get("reason")

        # Save to DB
        payment = Payment(
            request_id=request_id,
            transaction_id=request.transaction_id,
            amount=amount,
            status=status
        )
        db.add(payment)
        db.commit()

        return PaymentResponse(
            request_id=request_id,
            status=status,
            amount=amount,
            reason=reason
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Payment failed: {str(e)}")
    finally:
        db.close()


@router.get("/transactions/{transaction_id}/payments", response_model=List[PaymentOut])
def get_payments_for_transaction(transaction_id: int = Path(..., title="Transaction ID")):
    db = SessionLocal()
    try:
        transaction = db.query(SalesTransaction).filter(SalesTransaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return transaction.payments
    finally:
        db.close()


@router.post("/revert")
def revert_payment(payload: RevertRequest):
    db = SessionLocal()
    try:
        response_json = provider_revert(payload.request_id)
        response = json.loads(response_json)

        # Update status if reverted
        payment = db.query(Payment).filter(Payment.request_id == payload.request_id).first()
        if payment and response.get("status") == "Reverted":
            payment.status = "Reverted"
            db.commit()

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Revert failed: {str(e)}")
    finally:
        db.close()


@router.post("/transactions/{transaction_id}/revert_all")
def revert_all_payments(transaction_id: int):
    db = SessionLocal()
    try:
        transaction = db.query(SalesTransaction).filter(SalesTransaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        results = []
        for payment in transaction.payments:
            if payment.status != "Reverted":
                try:
                    response_json = provider_revert(payment.request_id)
                    response = json.loads(response_json)

                    if response.get("status") == "Reverted":
                        payment.status = "Reverted"
                        db.commit()

                    results.append({
                        "request_id": payment.request_id,
                        "response": response
                    })

                except Exception as e:
                    results.append({
                        "request_id": payment.request_id,
                        "error": str(e)
                    })

        return {"results": results}

    finally:
        db.close()
