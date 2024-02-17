from . import tables, create_database, delete_database

__all__ = ["tables", "create_database", "delete_database"]

def create_db() -> None:
    create_database.create_database()

def delete_db() -> None:
    delete_database.delete_database()

def recreate_db() -> None:
    delete_database.delete_database()
    create_database.create_database()
