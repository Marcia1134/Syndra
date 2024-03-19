# Main File

import logging
from rich.logging import RichHandler
import checks
import bot
import ease
from discord.utils import setup_logging

# Logging configuration
logger = setup_logging(level=logging.INFO)
logger = logging.getLogger('syndra')


if __name__ == '__main__':
    logger.info("Starting the Syndra Application! If you have any issues, please report them to the developers.")
    
    ease.print_line()

    with open('ASCII.txt', 'r') as file:
        print(file.read())

    ease.print_line()

    checks.env()
    checks.db()
    bot.main()

# Path: src/main.py