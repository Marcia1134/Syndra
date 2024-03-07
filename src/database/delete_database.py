import peewee as pw
import os

def delete_database() -> None:
    # Delete the database
    if os.path.exists('syndra.db'):
        try:
            os.remove('syndra.db')
        except FileNotFoundError:
            print("File not found... Continuing anyway...")
            pass
        except Exception as e:
            print(f"An error occurred: {e}\n\nContinuing anyway...")
            pass

    debug_enabled = True

    # DEBUG
    if debug_enabled == False:
        return

    if os.path.exists('syndra.db'):
        print("DB still present... Calling error and stopping code.")
        exit(3)
    else:
        print("All seems good, continuing...")