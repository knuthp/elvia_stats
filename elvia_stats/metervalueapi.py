import datetime
import os
from typing import Dict

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.environ["ELVIA_ACCESS_TOKEN"]
session = requests.session()
session.headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
METER_VALUES_URL = "https://elvia.azure-api.net/customer/metervalues/api/v1/metervalues"


def get_metervalues(year: int) -> Dict:
    """Get Eliva usage data for customer using ELVIA_ACCESS_TOKEN environment

    ELIVA_ACCESS_TOKEN enviroment is used for authentication and identification.

    Params:
        year: the year to get data for.

    Returns:
        power consumption for a year or until now

    Raises:
        Requests exceptios forwarded
    """
    # https://elvia.portal.azure-api.net/docs/services/metervalueapi/operations/get-api-v1-metervalues?
    startTime = f"{year}-01-01T00:00:00+01:00"
    current_year = 2021
    if year != current_year:
        endTime = f"{year}-12-31T23:59:59+01:00"
    else:
        endTime = datetime.datetime.now().isoformat()
    resp = session.get(f"{METER_VALUES_URL}?startTime={startTime}&endTime={endTime}")
    resp.raise_for_status()

    return resp.json()


def json_to_pandas(json_data: dict) -> pd.DataFrame:
    """Convert json dict to pandas Dataframe

    Params:
        dict: json as dict returned from metervalueapi

    Returns>
        Dataframe with usage per hour
    """
    return pd.json_normalize(
        json_data["meteringpoints"][0], record_path=["metervalue", "timeSeries"]
    )


def fix_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Fixes so startTime and endTime is tz aware datetime.

    Experience trouble that pd.to_datetime() did not work.
    We have a special step going via Norwegian tz.
    """
    df["startTimeStr"] = df["startTime"]
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )
    df["endTime"] = pd.to_datetime(df["endTime"], utc=True).dt.tz_convert("Europe/Oslo")
    return df
