import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from asyncio import sleep
import subprocess
import os
import shutil
import re
import glob
from a3modupdater import update_mods,updateServer
import json
import urllib.request
import requests
import shutil
import time
import psutil
from steam import game_servers as gs
from a3lib import open_pbo,create_pbo
from urllib.error import URLError, HTTPError


tmp_name = ""
tmp_time = ""
name = ""
times = ""

with open('login.json') as jsonfile:
    login = json.load(jsonfile)
DiscordManageRoleId = login['DiscordManageRoleId']
DiscordServerRestartRoleId = login['DiscordServerRestartRoleId']
A3serverPath = login['A3serverPath']
A3ServerConfigName = login['A3ServerConfigName']
def GetCurrentTime():
    dt = datetime.utcnow()
    dt += timedelta(hours=3)
    return dt

def TimeFormat(timedelta):
    time = timedelta.total_seconds()
    hours = time // 3600
    time = time - (hours * 3600)
    minutes = time // 60
    seconds = time - (minutes * 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

def filesize(file):
    size = os.path.getsize(file)
    if size < 1000:
        size = str(size) + 'K'
    else:
        size = str(round((size/(1024*1024)),1)) + 'M'
    return size
    
async def GetInfoServer():
    try:
        global ServerAdress
        data = gs.a2s_info((ServerAdress,2303), timeout = 4)
    except:
        return None
    if data is not None:
        return data
    return None

async def SetMS(arg):
    if os.access(A3serverPath + "\\mpmissions\\" + arg + ".pbo", os.R_OK):
        with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
            newcfg = dict()
            i = 0
            for line in config.readlines():
                if re.search(r"template", line):
                    newcfg[i] = '\t\ttemplate = "' + arg + '";\n'
                else:
                    newcfg[i] = line
                i += 1
            with open(A3serverPath + "\\" + A3ServerConfigName, "w") as config:
                for k, v in newcfg.items():
                    config.write(v)
        return True
    else:
        return False

async def SaveAttachment(ctx,Save=False):
    path = os.getcwd() + '\\tmp\\'
    if Save:
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory tmp failed")
            return False
        else:
            for attach in ctx.message.attachments:
                await attach.save(path + attach.filename)
                return attach
    else:
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        for attach in ctx.message.attachments:
            await attach.save(f"" + A3serverPath + "\\mpmissions\\" + attach.filename)
            return attach

async def ProcessMsUploaded():
    path = os.getcwd() + '\\tmp\\'
    if os.path.isdir(path):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            f.extend(filenames)
            break
        for file in f:
            if '.pbo' in file:
                shutil.move(path + file, A3serverPath + "\\mpmissions\\" + file)
                await SetMS(file.replace('.pbo', ''))
                print("Mission changed")
                break
                
async def ProcessZeusUpdate():
    path = A3serverPath+'\\mpmissions\\'
    try:
        if os.path.isdir(path):
            for name in os.listdir(path):
                if os.path.isdir(path+name):
                    name = name
                    break
            os.remove(path+name+'.pbo')
            create_pbo(path+name,delete_path = True)
    except Exception as e:
        print(f"Ошибка: {e}")

async def ServerRestart(updateMods = False,update_server = False):
    global ArmaCmdPid, SavedServerInfo
    try:
        for proc in psutil.process_iter():
            if proc.name().lower() == "arma3server_x64.exe" or proc.name().lower() == "cmd.exe":
                subprocess.call("taskkill /F /T /PID %i" % proc.pid)
        await ProcessMsUploaded()
        await ProcessZeusUpdate()
        if updateMods:
            update_mods()
            await sleep(6)
        if update_server:
            updateServer()
        process = subprocess.Popen([A3serverPath + '\\START_arma3server.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        await sleep(5)
        response = await GetInfoServer()
        if response:
            SavedServerInfo = response
        return True
    except Exception as e:
        print("Ошибка рестарта сервера: " + str(e))
        return False

async def cheak():
    first = 0
    global tmp_name
    global tmp_time
    global times
    global name
    if tmp_name == "":
        first = 1
        with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
            for line in config:
                if "template =" in line:
                    tmp_name = line.split('"')[1]
                    break

    if tmp_name != "" and tmp_time == "":
        tmp_time = os.path.getmtime(A3serverPath + "\\mpmissions\\" + tmp_name + ".pbo")
    with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
        for line in config:
            if "template =" in line:
                name = line.split('"')[1]
                break
    times = os.path.getmtime(A3serverPath + "\\mpmissions\\" + name + ".pbo")
    if times != tmp_time or name != tmp_name:
        tmp_time = times
        tmp_name = name
        open_pbo(A3serverPath + "\\mpmissions\\" + tmp_name + ".pbo")
        return await read_zeus(A3serverPath + "\\mpmissions\\" + tmp_name)
    if first == 1:
        open_pbo(A3serverPath + "\\mpmissions\\" + tmp_name + ".pbo")
        first = 0
        return await read_zeus(A3serverPath + "\\mpmissions\\" + tmp_name)
    else:
        return None

async def read_zeus(path):
    with open(path+'\scripts\curator.sqf',encoding="utf8") as file:
        w = file.readlines()
    zeus_dict = {}
    count = []
    for line in w:
        if "];" in line:
            if len(count) > 0:
                zeus_dict[line2] = count
            break
        if '//' in line and '// ' not in line:
            if len(count) > 0:
                zeus_dict[line2] = count
                count = []
            line2 = line.replace('\t', "").replace('\n', "").replace("//", "")
        if '"' in line or '// ' in line:
            line = line.replace('\t', "").replace('\n',"").replace(' ', "").replace("/", "").replace(",", "")
            uslit = line.split('"')
            steamId = uslit[1]
            niceName = uslit[2]
            if niceName == "":
                niceName = "Нет имени"
            count.append(f"{steamId} - {niceName}\n")
    shutil.rmtree(path)
    return zeus_dict

async def MsZeusUpdate():
    path = A3serverPath + "\\mpmissions\\"
    for file in os.listdir(path):
        if os.path.isdir(path+file):
            direct = file
    os.remove(path+direct+".pbo")
    create_pbo(path+direct,delete_path = True)

async def msselect():
    with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
        for line in config:
            if "template =" in line:
                file = line
                break
    file = file.replace(" ","").replace("template","").replace("=","").replace(";\n","").replace('"',"").replace("\t","")
    return file

    
    
