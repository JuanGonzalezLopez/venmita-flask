import pandas as pd
import pytest
from src.load_data.load_yaml import load_yaml


def test_load_yaml():
    # Replace with the path to your sample YAML file
    data = load_yaml('path/to/your/sample.yml')
    assert isinstance(data, pd.DataFrame)  # or DataFrame, depending on your implementation
    # Add more assertions to validate the structure and content of the data



