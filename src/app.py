from flask import Flask, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Person, Transfer, Transaction, Promotion
import os
from config.logger import setup_logger
from config.generatingOutput import generate_er_diagram


app = Flask(__name__)
logger = setup_logger()
from config.config import Config

def get_engine():
    config = Config()
    database_url = config.DATABASE_URL
    return create_engine(database_url)

def query_to_dict(query):
    return [item.to_dict() for item in query]

@app.route('/people', methods=['GET'])
def get_people():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        people = session.query(Person).all()
        return jsonify(query_to_dict(people))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    finally:
        session.close()

@app.route('/transfers', methods=['GET'])
def get_transfers():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        transfers = session.query(Transfer).all()
        return jsonify(query_to_dict(transfers))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    finally:
        session.close()

@app.route('/transactions', methods=['GET'])
def get_transactions():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        transactions = session.query(Transaction).all()
        return jsonify(query_to_dict(transactions))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    finally:
        session.close()

@app.route('/promotions', methods=['GET'])
def get_promotions():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        promotions = session.query(Promotion).all()
        return jsonify(query_to_dict(promotions))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    finally:
        session.close()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})


# generate_er_diagram()

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)