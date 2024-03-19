from os import getenv
from dotenv import load_dotenv
import logging

# Set Variables
logger = logging.getLogger('syndra')
Verbose = getenv('DEBUG')
ds_KEY = getenv('TOKEN')
load_dotenv('config.env')

def main() -> None:
    '''
    func : main
    args : None
    ret  : None

    purpose:
        This function will check if the environment variables are set correctly.

    args:
        None

    ret:
        None

    raises:
        ValueError : If the DISCORD_TOKEN is not set, empty, too short, or too long.
    '''
    if getenv("DEBUG") == "True":
        logger.info("Checking ENV setup")
    token = getenv("TOKEN")
    if token is None:
        raise ValueError("DISCORD_TOKEN is not set")
    if not token:
        raise ValueError("DISCORD_TOKEN is empty")
    if len(token) < 10:
        raise ValueError("DISCORD_TOKEN is too short")
    if len(token) > 100:
        raise ValueError("DISCORD_TOKEN is too long")
    if getenv("DEBUG"):
        logger.info("DISCORD_TOKEN is set correctly")

# Path: src/checks/check_env.py