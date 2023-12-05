import pandas as pd
from config.logger import setup_logger

logger = setup_logger()

class data_harmonize_integrate():
    def __init__(self):
        pass

    def harmonize_people_data(self, json_data: pd.DataFrame, yaml_data: pd.DataFrame):
        """
        Harmonizes the data from JSON and YAML files into a single DataFrame.

        Parameters:
        json_data (DataFrame): DataFrame containing data from people.json.
        yaml_data (DataFrame): DataFrame containing data from people.yml.

        Returns:
        DataFrame: Harmonized DataFrame of people data.
        """
        try:
            # Process YAML data
            # Split the 'name' column into 'firstName' and 'surname'
            yaml_data.reset_index(drop=True)
            json_data.reset_index(drop=True)


            yaml_data[['firstName', 'surname']] = yaml_data['name'].str.split(pat=' ', n=1, expand=True)
            # Process city and country fields in YAML data
            city_country = yaml_data['city'].str.split(', ', expand=True)


            yaml_data['city'] = city_country[0]
            yaml_data['country'] = city_country[1] if len(city_country.columns) > 1 else ''
            json_data['id'] = json_data['id'].apply(lambda x: int(x) if pd.notnull(x) else None).astype(int)
            yaml_data['id'] = yaml_data['id'].astype(int)


            # Rename 'phone' column in yaml_data to 'telephone' to match json_data
            yaml_data.rename(columns={'phone': 'telephone'}, inplace=True)



            # Select common columns for concatenation
            common_columns = ['id', 'firstName', 'surname', 'email', 'city', 'country', 'telephone']
            combined_people = pd.concat([json_data[common_columns], yaml_data[common_columns]], ignore_index=True,
                                        sort=False)
            # combined_people = pd.concat([json_data, yaml_data], ignore_index=True, sort=False)
            logger.info("Harmonization of people data completed successfully.")
        except Exception as e:
            logger.error(f"Error in harmonizing people data: {e}")
            raise

        return combined_people

    def integrate_transactions(self, transactions_data, people_data):
        """
        Integrates transaction data with people data.

        Parameters:
        transactions_data (DataFrame): DataFrame containing data from transactions.xml.
        people_data (DataFrame): DataFrame containing harmonized people data.

        Returns:
        DataFrame: DataFrame with integrated transaction data.
        """
        try:
            # Split buyer_name in transactions_data to get the initial of the first name and surname
            transactions_data['firstName_initial'] = transactions_data['buyer_name'].str.extract(r'(\w)\.')[0]
            transactions_data['surname'] = transactions_data['buyer_name'].str.extract(r' (\w+)$')[0]

            # Merge transactions with people data
            # Compare the first letter of firstName in people_data with firstName_initial in transactions_data
            integrated_data = transactions_data.merge(
                people_data,
                left_on=['firstName_initial', 'surname'],
                right_on=[people_data['firstName'].str[0], 'surname'],
                how='left'
            )
            logger.info("Integrating transaction data completed successfully.")
            # integrated_data['id'] = integrated_data['id'].apply(lambda x: int(x) if pd.notnull(x) else None)

        except Exception as e:
            logger.error(f"Error in integrating transaction data: {e}")
            raise

        return integrated_data

    def integrate_transfers(self,transfers_data, people_data):
        """
        Integrates transfer data with people data.

        Parameters:
        transfers_data (DataFrame): DataFrame containing data from transfers.csv.
        people_data (DataFrame): DataFrame containing harmonized people data.

        Returns:
        DataFrame: DataFrame with integrated transfer data.
        """
        try:
            # Assuming sender_id and recipient_id in transfers match id in people data
            transfers_data = transfers_data.rename(columns={'sender_id': 'sender', 'recipient_id': 'recipient'})
            transfers_data['sender'] = transfers_data.apply(lambda row: int(row['sender']), axis=1)
            transfers_data['recipient'] = transfers_data.apply(lambda row: int(row['recipient']), axis=1)
            transfers_data = transfers_data.merge(people_data, left_on='sender', right_on='id', how='left')

            transfers_data = transfers_data.merge(people_data, left_on='recipient', right_on='id', how='left', suffixes=('_sender', '_recipient'))



            logger.info("Integrating transfer data completed successfully.")

        except Exception as e:
            # Log the error (consider using a logging library here)
            logger.error(f"Error in integrating transfer data: {e}")

            print(f"Error in integrating transfers: {e}")
            raise

        return transfers_data

    def integrate_promotions(self, promotions_data: pd.DataFrame, people_data: pd.DataFrame):
        try:
            # Add a new column 'person_id' in promotions_data for the corresponding person's ID
            promotions_data['person_id'] = None

            # Iterate over each promotion record to find the matching person_id
            for index, promo in promotions_data.iterrows():
                client_email = promo['client_email'] if (len(promo['client_email']) > 2) else None
                telephone = promo['telephone'] if (len(promo['telephone']) > 2) else None
                # Find the matching person by email or telephone

                if client_email:
                    person = people_data.loc[people_data['email'] == client_email]

                elif telephone:
                    person = people_data.loc[people_data['telephone'] == telephone]
                else:
                    continue  # Skip if both email and telephone are missing


                # If a matching person is found, assign their ID to the promotion record
                if not person.empty:
                    promotions_data.at[index, 'person_id'] = person.head(1)['id'].item()
                else:
                    continue



        except Exception as e:
            logger.error(f"Error in integrating promotion data: {e}")
            raise

        return promotions_data




