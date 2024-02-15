from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

def main() -> None:
    token = getenv("TOKEN")
    if token is None:
        raise ValueError("DISCORD_TOKEN is not set")
        return
    if not token:
        raise ValueError("DISCORD_TOKEN is empty")
        return
    if len(token) < 10:
        raise ValueError("DISCORD_TOKEN is too short")
        return
    if len(token) > 100:
        raise ValueError("DISCORD_TOKEN is too long")
        return
    print("DISCORD_TOKEN is set correctly")

# Path: src/checks/check_env.py