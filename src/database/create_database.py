from sqlalchemy import create_engine, exc
from sqlalchemy_utils import database_exists, create_database


from config.config import Config
from models import Base
from config.logger import setup_logger
import sys

logger = setup_logger()


def create_database_if_not_exists(database_url):
    try:
        engine = create_engine(database_url)

        if not database_exists(engine.url):
            logger.info("Creating database.")
            create_database(engine.url)
        else:
            logger.info("Database already exists.")

        return engine
    except exc.SQLAlchemyError as e:
        logger.error(f"Database creation failed: {e}")
        sys.exit(1)

def create_tables(engine):
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created.")
    except exc.SQLAlchemyError as e:
        logger.error(f"Table creation failed: {e}")
        sys.exit(1)

def main():
    config = Config()
    database_url = config.DATABASE_URL

    engine = create_database_if_not_exists(database_url)
    create_tables(engine)

if __name__ == "__main__":
    main()