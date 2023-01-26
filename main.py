import json
import asyncio
import discord
import os
import pbo_features as pbo
import database_interaction as db
from discord import app_commands
from discord.ext import commands

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
bot = commands.Bot(command_prefix=login["prefix"], intents=intents)


# tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Ready!")


# = commands.param(description="SteamID64 человека которого нужно добавить"

@bot.tree.command(name="add_zeus", description="Добавить зевса в миссию")
@app_commands.describe(steamid64="СтимАйди жертвы", user="Упомяните человека")
@app_commands.checks.has_any_role(login['DiscordManageRoleId'])
async def add_zeus(interaction, steamid64: int, user: discord.Member):
    if can_use_command(interaction) == 1 and not db.check_if_exists_zeus(steamid64):
        if await db.add_zeus(steamid64, user):
            print("Добавил зевса в базу данных ")
            print(f"{interaction.author.name} добавил зевса {steamid64}")
            await interaction.response.send_message(await pbo.add_zeus(steamid64, user))


@bot.tree.command(name="del_zeus", description="Забрать зевс")
@app_commands.describe(steamid64="SteamID64 человека которого нужно удалить")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.checks.has_any_role(login['DiscordManageRoleId'])
async def del_zeus(interaction, steamid64: int):
    if can_use_command(interaction) == 1 and db.check_if_exists_zeus(steamid64):
        if await db.delete_zeus(steamid64):
            print("Удалил зевса из базы данных")
            print(f"{interaction.author.name} удалил зевса {steamid64}")
            await interaction.response.send_message(await pbo.del_zeus(steamid64))


@bot.tree.command(name="zeus_list", description="Вывести список зевсов")
async def get_zeus(interaction):
    await interaction.response.send_message(await db.get_zeuses())


@bot.tree.command(name="ban", description="Забанить игрока по стимайди")
@app_commands.checks.has_any_role(login['BanRoleID'])
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(steamid64="SteamID64 человека которого нужно забанить", reason="Причина бана",duration= "Длительность в формате d,m,y, если навсегда - 0" )
async def ban_user_by_id(interaction,steamid64: int,reason: str,duration: str):
        if await db.ban_player(steamid64, reason, duration):
            await interaction.response.send_message(await pbo.ban_user(steamid64, reason, duration))
            print(f"{interaction.author.name} забанил игрока {steamid64}")



@bot.tree.command(name="unban", description="Разбанить игрока по стимайди")
@app_commands.describe(steamid64 = "SteamID64 человека которого требуется разбанить")
@app_commands.checks.has_any_role(login['BanRoleID'])
@app_commands.checks.has_permissions(administrator=True)
async def unban_user_by_id(interaction, steamid64: int):
    if await db.unban_player(steamid64):
        print(f"{interaction.author.name} разбанил игрока {steamid64}")
        await interaction.respones.send_message(await pbo.unban_user(steamid64))


@bot.tree.command(name="ban_list", description="Список банов")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.checks.has_any_role(login['BanRoleID'])
async def ban_list(interaction):
    await interaction.response.send_message(await db.get_bans())


async def main():
    async with bot:
        await bot.start(login['login'])


asyncio.run(main())
