from pydantic import BaseModel


class TransactionResponse(BaseModel):
    transaction_id: int
