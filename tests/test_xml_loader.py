import pytest
from src.load_data.load_xml import load_xml
import pandas as pd
def test_load_xml():
    # Replace with the path to your sample XML file
    data = load_xml('path/to/your/sample.xml')
    assert isinstance(data, pd.DataFrame)  # or DataFrame, depending on your implementation
    # Add more assertions to validate the structure and content of the data

