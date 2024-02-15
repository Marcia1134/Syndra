import discord

class Client(discord.Client):
    def __init__(self):
        print("Discord API Client")

def run_client(token):
    print("Running Discord API Client")
    try:
        Client.run(token)
    except Exception as e:
        print(e)
        return e

# Path: src/startup/__init__.py