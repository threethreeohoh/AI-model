from pydantic import BaseModel

class PredictionRequestDto(BaseModel):
    obs_code : int
 