import requests
from datetime import datetime, timedelta, date
import joblib
import pandas as pd
import numpy as np
import unicodedata
import os
from fastapi import HTTPException
from ..schema.prediction_response_schema import PredictionResponseDto

# Woo
def get_classification(request):
    test_list = []
    test_list.append(PredictionResponseDto(
        obs_name="test",
        predicted_date="test",
        raining_status=True
    ))
    return {"data": test_list}