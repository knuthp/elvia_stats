import datetime
from typing import Dict

import dateutil.parser as parser
import pytest
from requests_mock import Mocker

from elvia_stats import metervalueapi

ACCESS_TOKEN = "PYTEST_INJECTED"


def test_retrieves_json(meter_value_mock: Mocker):
    data = metervalueapi.get_metervalues(2021)
    assert meter_value_mock.called_once
    assert "meteringpoints" in data
    meteringpoint = data["meteringpoints"][0]
    assert "customerContract" in meteringpoint
    assert "metervalue" in meteringpoint
    assert meteringpoint["metervalue"]["resolutionMinutes"] == 60


def test_stattime_endtime(meter_value_mock: Mocker):
    metervalueapi.get_metervalues(2020)

    # Converts to lowercase, replace '+' with ' '
    qs = meter_value_mock.request_history[0].qs
    assert "starttime" in qs
    assert "endtime" in qs
    assert qs["starttime"][0] == "2020-01-01t00:00:00 01:00"
    assert qs["endtime"][0] == "2020-12-31t23:59:59 01:00"


def test_starttime_endtime_current_year(meter_value_mock: Mocker):
    metervalueapi.get_metervalues(2021)

    # Converts to lowercase, replace '+' with ' '
    qs = meter_value_mock.request_history[0].qs
    assert "starttime" in qs
    assert "endtime" in qs
    assert qs["starttime"][0] == "2021-01-01t00:00:00 01:00"
    end_time = parser.parse(qs["endtime"][0])
    current_time = datetime.datetime.now()
    delta = current_time - end_time
    assert delta.seconds < 5


def test_token(meter_value_mock: Mocker):
    metervalueapi.get_metervalues(2021)
    # Only found headers on protected _request
    request = meter_value_mock.request_history[0]._request
    assert ACCESS_TOKEN in request.headers["Authorization"]


def test_to_pandas(sample_json_data: Dict):
    df = metervalueapi.json_to_pandas(sample_json_data)
    assert df.iloc[0]["startTime"] == "2021-01-01T00:00:00+01:00"
    assert df.iloc[-1]["endTime"] == "2021-01-02T23:00:00+01:00"


def test_datetimefix(sample_json_data: Dict):
    df = metervalueapi.json_to_pandas(sample_json_data)
    df = metervalueapi.fix_datetime(df)

    assert df["startTime"].dtype == "datetime64[ns, Europe/Oslo]"
    assert df["endTime"].dtype == "datetime64[ns, Europe/Oslo]"


@pytest.fixture
def meter_value_mock(requests_mock: Mocker, sample_json_data: Dict):
    requests_mock.get(
        metervalueapi.METER_VALUES_URL,
        json=sample_json_data,
    )
    return requests_mock


@pytest.fixture(autouse=True)
def set_fake_token(monkeypatch):
    monkeypatch.setenv("ELVIA_ACCESS_TOKEN", ACCESS_TOKEN)
