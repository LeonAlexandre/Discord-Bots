# bot.py template code
import os

import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')
    print(f'Bot is connected to {client.guilds}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    alex_quotes = [
        'PRESS DOWN B',
        'It\s life',
        'I haven\'t had an erection in three years'
    ]
    if message.content == '!Alex':
        response = random.choice(alex_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException


client.run(TOKEN)