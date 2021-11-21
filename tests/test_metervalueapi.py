import datetime
import json
from pathlib import Path

import dateutil.parser as parser
import pytest
from requests_mock import Mocker

from elvia_stats import metervalueapi


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


def test_stattime_endtime_current_year(meter_value_mock: Mocker):
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


@pytest.fixture
def meter_value_mock(requests_mock: Mocker):
    json_str = Path("tests/metervalue_sample.json").read_text()
    requests_mock.get(
        metervalueapi.METER_VALUES_URL,
        json=json.loads(json_str),
    )
    return requests_mock
