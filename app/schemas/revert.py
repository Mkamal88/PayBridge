from pydantic import BaseModel


class RevertRequest(BaseModel):
    request_id: str


class RevertResponse(BaseModel):
    status: str
    amount: int | None = None
    error: str | None = None
    error_code: str | None = None
