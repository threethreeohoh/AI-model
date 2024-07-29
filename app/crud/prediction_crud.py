import requests
from datetime import datetime, timedelta, date
import joblib
import pandas as pd
import numpy as np
import unicodedata
import os
from fastapi import HTTPException

from ..schema.prediction_response_schema import PredictionResponseDto

# Eric
def get_amount(request):
    test = PredictionResponseDto(
        obs_name="test",
        predicted_date="test",
        raining_status=True,
    )
    return test
