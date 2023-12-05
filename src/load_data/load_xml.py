import pandas as pd
import xml.etree.ElementTree as ET


def load_xml(file_path):
    """
    Load an XML file into a Pandas DataFrame.

    :param file_path: Path to the XML file.
    :return: DataFrame containing the XML data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize an empty list to hold the parsed data
    data = []

    # Iterate through each element in the XML file
    for elem in root:
        record = {}
        # Alternative implementation: record = {child.tag: child.text for child in elem}
        # This is a more readable approach:
        for child in elem:
            record[child.tag] = child.text
        data.append(record)
    return pd.DataFrame(data).reset_index(names="trans_id")

# Example Usage:
# xml_data = load_xml('path_to_transactions.xml')
