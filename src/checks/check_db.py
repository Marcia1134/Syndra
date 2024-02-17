import peewee as pw
import database
from dotenv import load_dotenv
from os import getenv

load_dotenv('config.env')

def main() -> None:
    db = pw.SqliteDatabase(database='syndra.db')
    db.connect()

    try:
        database.create_db()
    except pw.OperationalError:
        if getenv("DEBUG") == "True":
            if input("Database already exists. Do you want to delete it? [y/n]: ").lower() == "y":
                database.delete_database.delete_database()
                database.create_database.create_database()
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        if getenv("DEBUG") == "True":
            print("Database created successfully")          

    db.close()  
