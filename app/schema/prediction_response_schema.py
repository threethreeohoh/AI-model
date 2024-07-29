from pydantic import BaseModel
from typing import List
class PredictionResponseDto(BaseModel):
    obs_name : str
    predicted_date : str
    raining_status : bool

class PredictionsResponseDto(BaseModel):
    data: List[PredictionResponseDto]