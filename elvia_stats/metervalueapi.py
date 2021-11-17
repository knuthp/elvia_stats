import os

import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.environ["ELVIA_ACCESS_TOKEN"]
session = requests.session()
session.headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"


def get_metervalues(year: int):
    # https://elvia.portal.azure-api.net/docs/services/metervalueapi/operations/get-api-v1-metervalues?
    url = "https://elvia.azure-api.net/customer/metervalues/api/v1/metervalues"
    startTime = "2021-01-01T01:00:00+02:00"
    endTime = "2021-11-17T00:21:00+02:00"
    resp = session.get(f"{url}?startTime={startTime}&endTime={endTime}")
    resp.raise_for_status()

    return resp.json()
