import peewee as pw
import database
from dotenv import load_dotenv
import os

load_dotenv('config.env')

def main() -> None:
    if os.path.exists("syndra.db"):
        print("database exists! continuing...")
        database.create_database.create_database()
    else:
        database.create_database.create_database()
        print("database does not exist! Stopping Bot and starting recovery script...")
        exit(2)