import json
import asyncio
import discord
import os
import pbo_features as pbo
import database_interaction as db
from discord import app_commands

with open('login.json') as jsonfile:
    login = json.load(jsonfile)
DiscordManageRoleId = login['DiscordManageRoleId']
DiscordServerRestartRoleId = login['DiscordServerRestartRoleId']
A3serverPath = login['A3serverPath']
A3ServerConfigName = login['A3ServerConfigName']


async def can_use_command(ctx, restart=False):
    if DiscordManageRoleId in [y.id for y in ctx.author.roles]:
        return 1
    if restart and DiscordServerRestartRoleId in [y.id for y in ctx.author.roles]:
        return 2
    return 0


intents = discord.Intents.all()
bot = app_commands.Bot(command_prefix=login["prefix"], intents=intents)
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=login['DiscordServerId']))
    print("Ready!")


@tree.command(name="add_zeus", description="Добавить зевса в миссию")
async def add_zeus(interaction,
                   steamid64: int = app_commands.Param(description="SteamID64 человека которого нужно добавить"),
                   user: discord.Member = app_commands.Param(description="Упомяните человека")):
    if can_use_command(interaction) == 1 and not db.check_if_exists_zeus(steamid64):
        if await db.add_zeus(steamid64, user):
            print("Добавил зевса в базу данных")
        await interaction.response.send_message(await pbo.add_zeus(steamid64, user))


@tree.command(name="del_zeus", description="Забрать зевс")
async def del_zeus(interaction,
                   steamid64: int = app_commands.Param(description="SteamID64 человека которого нужно удалить")):
    if can_use_command(interaction) == 1 and db.check_if_exists_zeus(steamid64):
        if await db.delete_zeus(steamid64):
            print("Удалил зевса из базы данных")
        await interaction.response.send_message(await pbo.del_zeus(steamid64))


@tree.command(name="zeus_list", description="Вывести список зевсов")
async def del_zeus(interaction):
    await interaction.response.send_message(await db.get_zeuses())


@tree.command(name="ban", description="Забанить игрока по стимайди")
async def ban_user_by_id(interaction,
                         steamid64: int = app_commands.Param(description="SteamID64 человека которого нужно забанить"),
                         reason: str = app_commands.Param(description="Причина бана"),
                         duration: int = app_commands.Param(description="Длительность, если навсегда - 0")
                         ):
    if login['BanRoleID'] in interaction.author.roles:
        await db.ban_player(steamid64, reason, duration)



async def main():
    async with bot:
        await bot.start(login['login'])


asyncio.run(main())
