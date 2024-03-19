import database
from os import path, getenv
import logging
from dotenv import load_dotenv

# Set Variables
load_dotenv('config.env')
Verbose = getenv('DEBUG')
logger = logging.getLogger('syndra')

def main() -> None:
    '''
    func : main
    args : None
    ret  : None

    purpose:
        This function will check if the database exists and if it doesn't, it will create it.

    args:
        None

    ret:
        None
    '''
    if path.exists("syndra.db"):
        logger.debug("Syndra.db exists! Passing off to create_database func")
        database.create_database.create_database()
    else:
        database.create_database.create_database()
        logger.error("Database doesn't exist, creating database and stopping bot...")
        exit(2)