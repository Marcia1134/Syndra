from . import tables, create_database, delete_database

__all__ = ["tables", "create_database", "delete_database"]

def create_db() -> None:
    '''
    func : create_db
    args : None
    ret  : None

    purpose:
        This function will create the database.

    args:
        None

    ret:
        None
    '''
    create_database.create_database()

def delete_db() -> None:
    '''
    func : delete_db
    args : None
    ret  : None

    purpose:
        This function will delete the database.

    args:
        None

    ret:
        None
    '''
    delete_database.delete_database()

def recreate_db() -> None:
    '''
    func : recreate_db
    args : None
    ret  : None

    purpose:
        This function will delete the database and then recreate it.

    args:
        None

    ret:
        None
    '''
    delete_database.delete_database()
    create_database.create_database()
