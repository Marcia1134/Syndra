import peewee as pw
from database import tables, create_database

def delete_database() -> None:
    db = pw.SqliteDatabase(database='syndra.db')
    db.connect()

    # Drop all tables
    db.drop_tables([tables.Server], safe=True, cascade=True)

    # Create all tables
    create_database.create_database()