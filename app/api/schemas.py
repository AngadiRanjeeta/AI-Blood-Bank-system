from pydantic import BaseModel, Field

class FindBestRequest(BaseModel):
    bg: str = Field(..., examples=["A+"])
    urgency: str = Field("high", examples=["critical", "high", "medium", "low"])
    lat: float
    lon: float