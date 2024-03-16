import database
import os

def main() -> None:
    if os.path.exists("syndra.db"):
        print("database exists! continuing...")
        database.create_database.create_database()
    else:
        database.create_database.create_database()
        print("database does not exist! Stopping Bot!!!")
        exit(2)