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
@app_commands.describe(steamid64="SteamID64 человека которого нужно забанить", reason="Причина бана",
                       duration="Длительность в формате d,m,y, если навсегда - 0")
async def ban_user_by_id(interaction, steamid64: int, reason: str, duration: str):
    if await db.ban_player(steamid64, reason, duration):
        await interaction.response.send_message(await pbo.ban_user(steamid64, reason, duration))
        print(f"{interaction.author.name} забанил игрока {steamid64}")


@bot.tree.command(name="unban", description="Разбанить игрока по стимайди")
@app_commands.describe(steamid64="SteamID64 человека которого требуется разбанить")
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


@bot.tree.command(name="stop_server", description="Остановить сервер")
@app_commands.checks.has_role(login['DiscordManageRoleId'])
async def stop(interaction):
    try:
        for proc in psutil.process_iter():
            if proc.name().lower() == "arma3server_x64.exe" or proc.name().lower() == "cmd.exe":
                subprocess.call("taskkill /F /T /PID %i" % proc.pid)
        await asyncio.sleep(5)
        await interaction.response.send_message("Сервер ушел на покой.")
    except Ane as e:
        print(e)
        await interaction.response.send_message("Не могу выключить")


@bot.tree.command(name="stop_server", description="Остановить сервер")
@app_commands.checks.has_role(login['DiscordManageRoleId'])
async def stop(interaction):
    try:
        global ArmaCmdPid
        process = subprocess.Popen([A3serverPath + '\\START_arma3server.bat'],
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
        ArmaCmdPid = process.pid
        await asyncio.sleep(5)
        await interaction.response.send_message("Сервер запускается.")
    except Any as e:
        print(e)
        await interaction.response.send_message("Не могу включить")


@bot.tree.command(name="restart", description="Перезапустить сервер")
@option(
    "update_mods",
    description="Обновить моды?",
    choices=['False', 'True'],
    default=False
)
@option(
    "update_server",
    description="Обновить сервер?",
    choices=['False', 'True'],
    default=False
)
@app_commands.checks.has_role(login['DiscordManageRoleId'])
async def restart(interaction, update_mods: bool, update_server: bool):
    global RestartTimer, RestartTimerStarted
    if not update_mods:
        RestartTimerStarted = GetCurrentTime().timestamp()
        await interaction.response.send_message(
            "Server will be restarted at " + datetime.fromtimestamp(RestartTimerStarted + 0).strftime(
                '%d.%m.%y | %X'))
    else:
        message = interaction.response.send_message("Сервер ушёл на рестарт.")
        if update_mods:
            rs = await ServerRestart(updateMods=True)
        if update_server:
            rs = await ServerRestart(update_server=True)
        else:
            rs = await ServerRestart()
        if rs:
            await sleep(5)
            await message.edit(content="Сервер вернулся после рестарта.")
        else:
            await message.edit(content="Рестарт не прошел.")

@bot.tree.command(name="msdownload", description="Скачать миссию")
@app_commands.checks.has_role(login['DiscordManageRoleId'])
async def msdownload(interaction):
    ms_file = A3serverPath + "\\mpmissions\\" + await msselect() + ".pbo"
    file = discord.File(ms_file)
    await interaction.response.send_message(file=file, content="Держи нынешнюю миссию.")

@bot.tree.command(name="msupload", description="Загрузить миссию")
@option(
    "restart",
    description="Перезапустить сервер после загрузки миссии?",
    choices=['False', 'True'],
    default=False
)
@app_commands.checks.has_role(login['DiscordManageRoleId'])
async def msupload(interaction, restart: bool):
    if interaction.message.attachments:
        if restart:
            message = await interaction.response.send_message("Сервер ушёл подумать.")
            for proc in psutil.process_iter():
                if proc.name().lower() == "arma3server_x64.exe" or proc.name().lower() == "cmd.exe":
                    subprocess.call("taskkill /F /T /PID %i" % proc.pid)
            attach = await SaveAttachment(interaction)
            await setms(ctx, attach.filename.replace('.pbo', ''))
            await message.edit(content="Миссия успешно установлена.")
            await asyncio.sleep(5)
            await start(interaction)
        else:
            attach = await SaveAttachment(interaction, Save=True)
            await interaction.response.send_message(
                content=("Миссия будет загружена на сервер после рестарта." if attach else "Сохранение не вышло."))
    else:
        await interaction.response.send_message("Миссию то добавь")

async def BotStatus():
    global SavedServerInfo
    while True:
        try:
            response = await GetInfoServer()
            SavedServerInfo = response
            if response:
                players = response.get('players')
                maxplayers = response.get('max_players')
                await bot.change_presence(
                    activity=discord.Game(name=BotStatusGame + str(players) + "/" + str(maxplayers)))
            else:
                await bot.change_presence(activity=discord.Game(name="Сервер на стадии перезагрузки"))
        except Exception as e:
            print(e)
        await asyncio.sleep(60)

async def main():
    async with bot:
        await bot.start(login['login'])


asyncio.run(main())
