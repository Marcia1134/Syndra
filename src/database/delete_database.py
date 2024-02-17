import peewee as pw
import os

def delete_database() -> None:
    # Delete the database
    if os.path.exists('syndra.db'):
        try:
            os.remove('syndra.db')
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}\n\nContinuing anyway...")
            pass