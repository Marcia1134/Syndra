from dotenv import load_dotenv
from os import getenv
from product_app_data import *

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

