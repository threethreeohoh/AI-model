import requests
from datetime import datetime, timedelta, date
import joblib
import pandas as pd
import numpy as np
import unicodedata
import os
from fastapi import HTTPException

from ..core.config import settings
from ..schema.prediction_response_schema import PredictionResponseDto, PredictionsResponseDto
from ..project_enum.obs_enum import ObsEnum

# Woo
def get_classification(request):
    # find obs
    selected_obs = find_obs(request=request)
    # update df to recent data
    df_up_to_date = weather_recent(obs=selected_obs)
    # Preprocessing
    num_cols = df_up_to_date.drop(columns=['baseDate']).columns
    temp_df = df_up_to_date[num_cols].apply(pd.to_numeric, errors='coerce')
    df_interpolated = temp_df.interpolate(method='linear', axis=0)
    df_interpolated['baseDate'] = df_up_to_date['baseDate']
    preprocessed_data = data_preprocessing(df_interpolated)

    # Prediction
    # Prediction: today, tomorrow, the day after tomorrow, two days after tomorrow
    prediction_days = -4
    # baseDate: responseDto
    predictions_list = []
    print("here?")
    model = joblib.load(unicodedata.normalize("NFC",selected_obs['path_to_model']))
    while (prediction_days < 0):
        current_row = preprocessed_data.iloc[prediction_days]
        current_row_date = current_row.at['baseDate']
        current_row_df = current_row.to_frame().T.drop(columns=["baseDate", "dailyRainfall"])
        current_row_prediction = model.predict(current_row_df)[0]
        if (current_row_prediction == 1) :
            # raining
            predictions_list.append(PredictionResponseDto(
                obs_name=selected_obs['observatoryName'],
                predicted_date=current_row_date,
                raining_status=True
            ))
        else :
            # not raining
            predictions_list.append(PredictionResponseDto(
                obs_name=selected_obs['observatoryName'],
                predicted_date=current_row_date,
                raining_status=False,
            ))
        prediction_days += 1
    # add try catch
    return {"data": predictions_list}
    
# Supporting Methods
# finding observatory based on given request
# Raise Error if obs_code is not valid
def find_obs(request):
    print("find_obs")
    obs_codes = [int(obs.value['obs_code']) for obs in ObsEnum]
    if (request.obs_code not in obs_codes):
        raise HTTPException(status_code=404, detail="Given code not valid")
    for obs in ObsEnum:
        obs_info = obs.value
        if int(obs_info['obs_code']) == request.obs_code:
            return obs_info

# Updating recent weather data
# Raise Error if server can't update recent data
def weather_recent(obs):
    print("weather_recent")
    obs_name = obs['observatoryName']
    obs_last_update = obs['last_update']
    up_to = datetime.now().date()+timedelta(days=3)
    df_up_to_date = pd.DataFrame(columns=obs['include'])
    while (obs_last_update <= up_to):
        project_key = settings.project_key
        year_month_day = obs_last_update.strftime("%Y%m%d")
        url = f'https://open.jejudatahub.net/api/proxy/1aD5taat1attaa51Db1511b51ab9Da19/{project_key}?searchDate={year_month_day}&observatoryName={obs_name}'
        response = requests.get(url=url)
        if response.status_code == 200:
            try:
                print(f"Status 200 JSON for {year_month_day}")
                response_json = response.json()
                df_up_to_date = pd.concat([df_up_to_date, json_parsing_200(response_json, obs, year_month_day)], ignore_index=True)
            except ValueError as e:
                print(f"Error decoding JSON for {year_month_day}: {e}")
                print(response.text)
        else:
            return None
        obs_last_update+=timedelta(days=1)
    return df_up_to_date

# Parsing
def json_parsing_200(data, obs, base_date):
    given_data =data['data']
    if (len(given_data) != 0):
        given_data = given_data[0]
        df = pd.DataFrame()
        for column in obs['include']:
            df[column] = [given_data.get(column)]
        return df
    else:
        df = pd.DataFrame()
        for column in obs['include']:
            df[column] = [np.nan]
        df['baseDate'] = [base_date]
        return df

# Preprocessing
def data_preprocessing(df):
    print("preprocessing")
    data = df.sort_values('baseDate')
    prev_day_1 = data.shift(1).drop(columns=['baseDate'])
    prev_day_2 = data.shift(2).drop(columns=['baseDate'])
    prev_day_3 = data.shift(3).drop(columns=['baseDate'])


    combined_data = pd.concat([data['baseDate'], data['dailyRainfall'],prev_day_1.add_suffix('_prev1'), prev_day_2.add_suffix('_prev2'), prev_day_3.add_suffix('_prev3')], axis=1)
    combined_data = combined_data.dropna()
    combined_data = combined_data.reset_index(drop=True)

    return combined_data