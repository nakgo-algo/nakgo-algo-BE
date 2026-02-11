from pydantic import BaseModel, Field


class FishAnalyzeRequest(BaseModel):
    image: str
    fileType: str


class FishRegulationInfo(BaseModel):
    minLength: int
    bannedMonths: list[int]
    description: str


class FishAnalyzeResponse(BaseModel):
    species: str
    confidence: float
    regulation: FishRegulationInfo


class FishSpeciesItem(BaseModel):
    name: str
    minLength: int
    bannedMonths: list[int]
    category: str


class FishCheckRequest(BaseModel):
    species: str
    length: float = Field(gt=0)


class FishCheckResponse(BaseModel):
    species: str
    inputLength: float
    minLength: int
    isUnderSize: bool
    isBannedPeriod: bool
    message: str
