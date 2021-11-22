from typing import Dict

import numpy as np
import pandas as pd
import pytest

from elvia_stats import metervalueapi, models


def test_extract_properties(default_data: pd.DataFrame):
    df = models.extract_properties(default_data)
    assert "hour" in df.columns
    assert "weekday" in df.columns
    assert "month" in df.columns
    np.testing.assert_array_equal(df["hour"].unique(), np.array(range(0, 24)))
    np.testing.assert_array_equal(df["weekday"].unique(), np.array([4, 5]))
    np.testing.assert_array_equal(df["month"].unique(), np.array([1]))


def test_elvia_night_day(default_data: pd.DataFrame):
    df = models.extract_properties(default_data)
    df = models.apply_elvia_night_day(df)

    assert "elvia_night_day_period" in df
    assert "elvia_night_day_cost_nok_per_kwh" in df
    assert df.iloc[0]["elvia_night_day_period"] == "winter_night"
    assert df.iloc[0]["elvia_night_day_cost_nok_per_kwh"] == 0.2890
    assert df.iloc[10]["elvia_night_day_period"] == "winter_day"
    assert df.iloc[10]["elvia_night_day_cost_nok_per_kwh"] == 0.7170


@pytest.fixture
def default_data(sample_json_data: Dict) -> pd.DataFrame:
    df = metervalueapi.json_to_pandas(sample_json_data)
    return metervalueapi.fix_datetime(df)
