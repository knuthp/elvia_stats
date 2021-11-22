import pytest
from pathlib import Path
import json

@pytest.fixture
def sample_json_data():
    json_str = Path("tests/metervalue_sample.json").read_text()
    return json.loads(json_str)
