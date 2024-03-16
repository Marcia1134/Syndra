import peewee as pw
from database.tables import *

def create_database() -> None:
    
    db = pw.SqliteDatabase(database='syndra.db')
    db.connect()

    print("Creating tables...")
    db.create_tables([Server, Currency, Wallet, RolePay, Commands, CommandConfig])

    db.close()