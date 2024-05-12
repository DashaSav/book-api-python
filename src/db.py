import logging
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

load_dotenv()

db_client: AsyncIOMotorClient | None = None


def get_db() -> AsyncIOMotorDatabase:
    db_name = os.environ.get('MONGODB_DATABASE')

    if db_client is None:
        connect_and_init_db()

    return db_client.get_database(db_name) # type: ignore


def get_collection(db: AsyncIOMotorDatabase, collection: str) -> AsyncIOMotorCollection:
    return db.get_collection(collection)


def connect_and_init_db():
    global db_client

    try:
        db_client = AsyncIOMotorClient(os.environ.get('MONGODB_URL'))
        logging.info('Connected to mongo.')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise


def close_db_connect():
    global db_client

    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')
