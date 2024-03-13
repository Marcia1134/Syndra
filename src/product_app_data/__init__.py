from dotenv import load_dotenv
from os import getenv
from product_app_data import create

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

async def create_product_func(interaction):
    await create.create_product(interaction=interaction)