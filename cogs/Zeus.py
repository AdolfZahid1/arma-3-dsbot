import database_interaction
import discord
import logging
from discord.ext import commands

class Guild(commands.Cog):
    """Guild class"""

    def __init__(self, bot):
        """Init function"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Add all server members to database """
        logging.warning('Hello World!')
        #await self.bot.change_presence(activity=discord.Activity(type=TYPE, name=login["default-activity"]))


class Zeuses(commands.Cog):
    @commands.tree.command(name="add_zeus", description="Add zeus to list")
    async def add_zeus(self,interaction):
        await interaction.response.send_message("Hello!")


async def setup(bot):
    """Init"""
    await bot.add_cog(Guild(bot))
    await bot.add_cog(Zeuses(bot))
    await bot.tree.sync(guild=discord.Object(id=645653725213622272))
