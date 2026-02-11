from pydantic import BaseModel


class FineResponse(BaseModel):
    id: int
    species: str
    violation: str
    fineAmount: str
    legalBasis: str
