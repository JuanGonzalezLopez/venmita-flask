import pandas as pd
import yaml

import pandas as pd
import yaml


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        # Load the YAML file
        data = yaml.safe_load(file)

        # Assuming the data is a list of dictionaries under a key like 'people'
        if 'people' in data:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(data['people'])
        else:
            # If the structure is different, adjust accordingly
            df = pd.DataFrame(data)

        return df

# Example Usage:
# yaml_data = load_yaml('path_to_people.yml')
