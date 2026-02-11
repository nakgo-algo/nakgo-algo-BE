from pydantic import BaseModel


class RegulationSpeciesItem(BaseModel):
    name: str
    minLength: int
    bannedPeriod: str
    fine: str


class RegulationRegionResponse(BaseModel):
    id: str
    region: str
    species: list[RegulationSpeciesItem]
