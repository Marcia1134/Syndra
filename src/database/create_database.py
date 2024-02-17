import peewee
from database import tables

def create_database() -> None:
    db = peewee.SqliteDatabase(database='syndra.db')
    db.connect()

    db.create_tables([tables.Server])