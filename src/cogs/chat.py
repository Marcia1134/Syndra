import discord
from discord import app_commands
from discord.ext import commands
import logging
import google.generativeai as genai

# Set Variables
genai.configure(api_key="AIzaSyC3_bO3DVAJ0rWCzy68D2UWB1TpNZ9q1BE")
model = genai.GenerativeModel('gemini-pro')
logger = logging.getLogger('syndra')

class ChatCommand(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot

    # Look for a message in a spesific channel using the event
    @commands.Cog.listener()
    async def on_message(self, message : discord.Message) -> None:
        '''
        func : on_message
        args : message : discord.Message
        ret  : None

        purpose:
            Listens to messages from the chatchannel and responds with a message from the generative model.
        
        args:
            message : discord.Message : The message object from the discord.py library.

        ret:
            None
        '''
        
        # if the message is from the bot ignore
        if message.author == self.bot.user:
            return
        # if message content starts with ! ingore
        if message.content.startswith("!"):
            return
        if message.content.startswith('src/'):
            # get filepath user will say src/ and then the file path and the file path will end wiht !
            # get the file path and then open the file and send the content
            file_path = message.content.split('!')[0]
            with open(file_path, 'r') as file:
                content = file.read()
                logger.info(f"Syndra read the file: {file_path}")
        else:
            content = None        


        channel_ids = [1199375811489321070, 1219587983439691786]
        if message.channel.id in channel_ids:

            # Prompt
            rubber_duck_prompt = f"You are a very good python developer working mainly in discord.py and you work in user expirence with discord, you tutor and help anyone you come across with code and things. You follow the rubber duck method, when someone tells you something, you reflect that idea back onto them in a way that says the pros and cons of the idea, and if nessary, proposes fixes or improvements. Please keep in mind you should try to keep your responses on the shorter side to not overload the 2000 character limit on discord. Try not to repeat yourself too much as well! generate something outside of what you see in messgae history. You are chatting with {message.author.name}, who said {message.content}, \n"

            # If the user mentioned a file, add the content to the prompt
            if content:
                rubber_duck_prompt += "\n\n\n Here is the content of the file the user mentioned: \n```\n" + content + "\n```"

            # If the user mentioned a message, add the content to the prompt
            if message.reply:
                rubber_duck_prompt += "\n\n\n Here is the content of the message the user mentioned: \n```\n" + message.reply.content + "\n```"

            try:
                response = model.generate_content(rubber_duck_prompt)
            except Exception as e:
                logger.error(f"{e}")
                message.reply("There seems to be an issue with your prompt, syndra couldn't respond. Please try again with a different prompt.")
                return

            # If the response is too long, split it into multiple messages
            if len(response.text) > 2000:
                for i in range(0, round(len(response.text)/2000)):
                    await message.reply(response.text[i:i+2000])
            else:
                await message.reply(response.text)

async def setup(bot : commands.Bot) -> None:
    await bot.add_cog(ChatCommand(bot))
