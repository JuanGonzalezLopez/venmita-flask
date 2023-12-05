import pandas as pd
import pytest
from src.load_data.load_json import load_json


def test_load_json():
    # Replace with the path to your sample JSON file
    data = load_json('path/to/your/sample.json')
    assert isinstance(data, pd.DataFrame)  # or DataFrame, depending on your implementation
    # Add more assertions to validate the structure and content of the data



