from pydantic import BaseModel


class ZoneResponse(BaseModel):
    id: int
    name: str
    type: str
    coordinates: list[list[float]]
    description: str
    period: str
