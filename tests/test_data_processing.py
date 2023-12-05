import pytest
from src.utils.data_processing import data_harmonize_integrate
import pandas as pd
test_data_processing = data_harmonize_integrate()

sample_json_data = pd.DataFrame({'...'})  # Fill with sample data
sample_yaml_data = pd.DataFrame({'...'})  # Fill with sample data
sample_csv_data_transaction = pd.DataFrame({'...'})  # Fill with sample data
sample_xml_data = pd.DataFrame({'...'})  # Fill with sample data
sample_csv_data_promotion = pd.DataFrame({'...'})  # Fill with sample data


def test_harmonize_people_data():
    result = test_data_processing.harmonize_people_data(sample_json_data, sample_yaml_data)
    assert isinstance(result, pd.DataFrame)

def test_integrate_transactions():
    result = test_data_processing.integrate_transactions(sample_xml_data, sample_json_data)
    assert isinstance(result, pd.DataFrame)


def test_integrate_transfers():
    result = test_data_processing.integrate_transfers(sample_csv_data_transaction, sample_json_data)
    assert isinstance(result, pd.DataFrame)


def test_integrate_promotions():
    result = test_data_processing.integrate_promotions(sample_csv_data_promotion, sample_json_data)
    assert isinstance(result, pd.DataFrame)
