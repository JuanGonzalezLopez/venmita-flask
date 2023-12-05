import pandas as pd

def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.

    :param file_path: Path to the CSV file.
    :return: DataFrame containing the CSV data.
    """
    df = pd.read_csv(file_path)
    return df

# Example Usage:
# csv_data = load_csv('path_to_transfers.csv')
