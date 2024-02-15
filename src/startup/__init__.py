print("imported startup package")

from os import getenv
from dotenv import load_dotenv
from startup import dclient

def main():
    load_dotenv()

    print("Loaded .env file")

    discord_token = getenv("DISCORD_TOKEN")
    
    dclient.run_client(discord_token)