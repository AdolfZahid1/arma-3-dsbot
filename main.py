import json
import asyncio
import discord
import os
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
with open('login.json') as jsonfile:
    login = json.load(jsonfile)

bot = commands.Bot(command_prefix=login["prefix"], intents=intents)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
async def main():
    async with bot:
        await load_extensions()
        await bot.start(login['login'])

asyncio.run(main())
