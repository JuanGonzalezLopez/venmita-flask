from sqlalchemy.orm import sessionmaker
from models import Person, Transfer, Transaction, Promotion


from src.load_data.load_json import load_json
from src.load_data.load_yaml import load_yaml
from src.load_data.load_csv import load_csv
from src.load_data.load_xml import load_xml
from src.utils.data_processing import data_harmonize_integrate
from sqlalchemy import create_engine
import os
import pandas as pd
from config.config import Config
from config.logger import setup_logger

logger = setup_logger()

def get_engine():
    config = Config()
    database_url = config.DATABASE_URL
    return create_engine(database_url)



def insert_people_data(session, people_data):
    try:

        for _, row in people_data.iterrows():
            person = Person(
                id=row['id'],
                firstName=row['firstName'],
                surname=row['surname'],
                email=row['email'],
                city=row['city'],
                country=row.get('country', None),  # Country might be None in some records
                telephone=row['telephone']
            )
            session.merge(person)

        session.commit()
        logger.info("People data inserted successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error while inserting people data: {e}")
        raise






def insert_transfers_data(session, transfers_data, people_data):
    try:
        people_ids = set(people_data['id'])

        for _, row in transfers_data.iterrows():
            # Split sender and recipient names

            if row['sender'] in people_ids and row['recipient'] in people_ids:
                transfer = Transfer(
                    sender_id=row['sender'],
                    recipient_id=row['recipient'],
                    amount=row['amount'],
                    date=pd.to_datetime(row['date'])
                )
                session.add(transfer)
        session.commit()

        logger.info("Transfer data inserted successfully.")
    except Exception as e:
        session.rollback()

        logger.error(f"Error while inserting transfer data: {e}")
        raise


def insert_transactions_data(session, transactions_data, people_data):
    try:
        # print(people_data.columns)

        # existing_ids = {t.id for t in session.query(Transaction.id).all()}  # Get existing transaction IDs

        for index, row in transactions_data.iterrows():
            # if index in existing_ids:  # Skip if ID already exists
            #     continue
            # print("-----")
            # print(index)
            # print(row)
            # print("-----")



            person = people_data[
                (people_data['firstName'] == row['firstName']) &
                (people_data['surname'] == row['surname'])
                ]

            # print(person['id'],type(person['id']))
            # print(person.empty)
            if not person.empty:
                transaction = Transaction(
                    # id=int(index),
                    buyer_id=int(person.head(1)['id'].item()),
                    item=row['item'],
                    price=row['price'],
                    store=row['store'],
                    transaction_date=pd.to_datetime(row['transactionDate'])
                )
                # print(transaction)

            session.add(transaction)
        session.commit()

        logger.info("transaction data inserted successfully.")
    except Exception as e:
        logger.error(f"Error while inserting transaction data: {e}")
        raise


def insert_promotions_data(session, integrated_promotions_data):
    try:
        for _, row in integrated_promotions_data.iterrows():

            # person_id: pd.Series = row['person_id']
            # if person_id is None or not (person_id > -1):
            #     logger.warning(f"Skipping promotion due to missing person_id: {row}")
            #     continue  # Skip promotions with missing person_id
            # Check if person_id is valid
            promotion = Promotion(
                client_email=row['client_email'],
                telephone=row['telephone'],
                promotion=row['promotion'],
                responded=row['responded'] == 'Yes',
                person_id=int(row['person_id']) if row['person_id'] is not None else None
            )

            # print(promotion)
            session.add(promotion)


        session.commit()
        logger.info("Promotion data inserted successfully.")
    except Exception as e:
        # session.rollback()
        logger.error(f"Error while inserting promotion data: {e}")
        raise






def export_data_to_csv(session):


    people = pd.read_sql(session.query(Person).statement, session.bind)
    promotions = pd.read_sql(session.query(Promotion).statement, session.bind)
    transfers = pd.read_sql(session.query(Transfer).statement, session.bind)
    transactions = pd.read_sql(session.query(Transaction).statement, session.bind)

    # Export to CSV
    people.to_csv('output/people.csv', index=False)
    promotions.to_csv('output/promotions.csv', index=False)
    transfers.to_csv('output/transfers.csv', index=False)
    transactions.to_csv('output/transactions.csv', index=False)

def export_data_to_excel(session):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('/output/final_data.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    pd.read_sql(session.query(Person).statement, session.bind).to_excel(writer, sheet_name='People', index=False)
    pd.read_sql(session.query(Promotion).statement, session.bind).to_excel(writer, sheet_name='Promotions', index=False)
    pd.read_sql(session.query(Transfer).statement, session.bind).to_excel(writer, sheet_name='Transfers', index=False)
    pd.read_sql(session.query(Transaction).statement, session.bind).to_excel(writer, sheet_name='Transactions', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def print_head_of_tables(session):
    people = pd.read_sql(session.query(Person).statement, session.bind)
    promotions = pd.read_sql(session.query(Promotion).statement, session.bind)
    transfers = pd.read_sql(session.query(Transfer).statement, session.bind)
    transactions = pd.read_sql(session.query(Transaction).statement, session.bind)

    print("People Table:")
    print(people.head())
    print("\nPromotions Table:")
    print(promotions.head())
    print("\nTransfers Table:")
    print(transfers.head())
    print("\nTransactions Table:")
    print(transactions.head())


def load_and_process_data():
    json_data = load_json('data/people.json')
    yaml_data = load_yaml('data/people.yml')
    csv_transfers_data = load_csv('data/transfers.csv')
    xml_transactions_data = load_xml('data/transactions.xml')
    csv_promotions_data = load_csv('data/promotions.csv')

    data_processing = data_harmonize_integrate()
    people_data = data_processing.harmonize_people_data(json_data, yaml_data)
    integrated_transfers = data_processing.integrate_transfers(csv_transfers_data, people_data)
    integrated_transactions = data_processing.integrate_transactions(xml_transactions_data, people_data)
    integrated_promotions = data_processing.integrate_promotions(csv_promotions_data, people_data)

    return people_data, integrated_transfers, integrated_transactions, integrated_promotions



def insert_all_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        people_data, integrated_transfers, integrated_transactions, integrated_promotions = load_and_process_data()

        insert_people_data(session, people_data)

        insert_transfers_data(session, integrated_transfers, people_data)

        insert_transactions_data(session, integrated_transactions, people_data)
        insert_promotions_data(session, integrated_promotions)
        session.commit()
        logger.info("All data inserted successfully.")




    except Exception as e:
        session.rollback()
        logger.error(f"Error while inserting data: {e}")
        raise
    finally:
        print_head_of_tables(session)
        export_data_to_csv(session)
        session.close()





if __name__ == "__main__":
    try:
        engine = get_engine()
        insert_all_data(engine)
    except Exception as e:
        logger.error(f"Error in data insertion process: {e}")


