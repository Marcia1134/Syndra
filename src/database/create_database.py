import peewee as pw
from database.tables import *
import logging

# Set Variables
logger = logging.getLogger('syndra')

def create_database() -> None:
    '''
    func : create_database
    args : None
    ret  : None

    purpose:
        This function will create the database.

    args:
        None

    ret:
        None
    '''
    # Connect to the database
    db = pw.SqliteDatabase(database='syndra.db')
    db.connect()

    # Create the tables
    db.create_tables([Server, Currency, Wallet, RolePay, Commands, CommandConfig, RoleCommandConfig])
    logger.info("Database tables created!")

    # Close the database
    db.close()