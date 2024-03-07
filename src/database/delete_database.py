import peewee as pw
import os

def delete_database() -> None:
    # Delete the database
    if os.path.exists('syndra.db'):
        print("DB already exists, attempting to remove.")
        try:
            os.remove('syndra.db')
        except FileNotFoundError:
            print("File not found... Continuing anyway...")
            pass
        except Exception as e:
            print(f"An error occurred: {e}\n\nContinuing anyway...")
            pass
    else:
        print("DB does not exist... continuing.")
        return

    debug_enabled = True

    # DEBUG - Checks if DB still exists after being deleted. 
    if debug_enabled == False:
        return

    if os.path.exists('syndra.db'):
        print("DB still present... Calling error and stopping code.")
        exit(3)
    else:
        print("All seems good, continuing...")