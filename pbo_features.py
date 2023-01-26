import json
import os

with open('login.json') as jsonfile:
    login = json.load(jsonfile)
from a3lib import open_pbo, create_pbo

A3serverPath = login['A3serverPath']
A3ServerConfigName = login['A3ServerConfigName']
path_to_bans = login['path_to_bans']


async def add_zeus(steamid64, user):
    curator_list = list()
    path_acces = 0
    print("Читаю конфиг")
    with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
        for line in config:
            if "template" in line:
                tmp_name = line.replace(" ", "").replace("template", "").replace("=", "").replace(";\n",
                                                                                                  "").replace('"',
                                                                                                              "").replace(
                    "\t", "")
                break
    for file in os.listdir(A3serverPath + "\\mpmissions\\"):
        if file == tmp_name:
            path_access = 1
    if path_access == 0:
        print("Открываю ПБО")
        open_pbo(A3serverPath + "\\mpmissions\\" + tmp_name + ".pbo")
        with open(A3serverPath + "\\mpmissions\\" + tmp_name + '\scripts\curator.sqf', "r", encoding="utf8") as file:
            for line in file:
                curator_list.append(line)
                curator_list.append("\t" + '"' + str(steamid64) + '",    // ' + str(str(user)) + "\n")
                done = True
        with open(A3serverPath + "\\mpmissions\\" + tmp_name + '\scripts\curator.sqf', "w", encoding="utf8") as file:
            for line in curator_list:
                file.write(line)
        if done:
            return f"<@!{user}> будет добавлен после рестарта сервера."
        else:
            print(f'Ошибка при добавлении нового зевса: ')
            return "Человек не был добавлен, повторите попытку, либо обратитесь к тех.админу"


async def del_zeus(steamid64):
    curator_list = list()
    path_acces = 0
    with open(A3serverPath + "\\" + A3ServerConfigName, "r") as config:
        for line in config:
            if "template" in line:
                tmp_name = line.replace(" ", "").replace("template", "").replace("=", "").replace(";\n", "").replace(
                    '"', "").replace("\t", "")
                break
    for file in os.listdir(A3serverPath + "\\mpmissions\\"):
        if file == tmp_name:
            path_access = 1
    if path_access == 0:
        open_pbo(A3serverPath + "\\mpmissions\\" + tmp_name + ".pbo")
    with open(A3serverPath + "\\mpmissions\\" + tmp_name + '\scripts\curator.sqf', "r", encoding="utf8") as file:
        for line in file:
            if str(steamid64) in line:
                pass
            else:
                curator_list.append(line)
    with open(A3serverPath + "\\mpmissions\\" + tmp_name + '\scripts\curator.sqf', "w", encoding="utf8") as file:
        for line in curator_list:
            file.write(line)
    return "Человек будет удалён после рестарта сервера."


async def ban_user(steamid64) -> str:
    try:
        # Открываем файл для чтения
        with open(path_to_bans, 'r') as file:
            # Читаем содержимое файла в список
            lines = file.readlines()

        # Добавляем новое значение в список
        lines.append(str(steamid64) + '\n')

        # Открываем файл для записи
        with open(path_to_bans, 'w') as file:
            # Записываем строки обратно в файл
            for line in lines:
                file.write(line)
        return "Человек будет забанен после рестарта"
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


async def unban_user(steamid64) -> str:
    try:
        # Открываем файл для чтения
        with open(path_to_bans, 'r') as file:
            # Читаем содержимое файла в список
            lines = file.readlines()

        # Удаляем строку с нужным значением
        lines = [line for line in lines if line.strip() != str(steamid64) + '\n']

        # Открываем файл для записи
        with open(path_to_bans, 'w') as file:
            # Записываем строки обратно в файл
            for line in lines:
                file.write(line)
        return "Пользователь будет разбанен после рестарта"
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
