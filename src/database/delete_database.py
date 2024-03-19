import peewee as pw
import os
import logging

# Set Variables
logger = logging.getLogger('syndra')

def delete_database() -> None:
    '''
    func : delete_database
    args : None
    ret  : None

    purpose:
        This function will delete the database.

    args:
        None

    ret:   
        None
    '''
    # Delete the database
    if os.path.exists('syndra.db'):
        logger.debug("Database Found... Deleting...")
        try:
            os.remove('syndra.db')
        except FileNotFoundError:
            logger.debug("File not found... Continuing anyway...")
            pass
        except Exception as e:
            logger.debug(f"An error occurred: {e}\n\nContinuing anyway...")
            pass
    else:
        logger.debug("DB does not exist... stopping bot proccess.")
        exit(500)