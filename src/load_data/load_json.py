import pandas as pd
import json


def load_json(file_path):
    with open(file_path, 'r') as file:
        # Load the JSON file
        data = json.load(file)['people']
        if 'people' in data:
        # Assuming the data is a list of dictionaries
            if isinstance(data['people'], list):
                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(data[0],dtype=str)
            else:
                # If the structure is different, adjust accordingly
                df = pd.DataFrame(data,dtype=str)
        else:
            df = pd.DataFrame(data)

        return df
