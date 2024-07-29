from fastapi import APIRouter

from ..schema.prediction_request_schema import PredictionRequestDto
from ..schema.prediction_response_schema import PredictionsResponseDto, PredictionResponseDto
from ..crud.classification_crud import get_classification
from ..crud.prediction_crud import get_amount

router = APIRouter()

@router.post("/predict/classify", response_model=PredictionsResponseDto)
def read_classifications(request: PredictionRequestDto):
    return get_classification(request = request)


@router.post("/predict/amount", response_model=PredictionResponseDto)
def read_prediction(request: PredictionRequestDto):
    return get_amount(request = request)