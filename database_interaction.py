import json
import psycopg2.extras
import re
import logging
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

with open('login.json') as jsonfile:
    login = json.load(jsonfile)
passw = login['dbpassword']
database_name = login['database_name']
user = login['dbuser']
host = login['dbhost']
port = "5432"


async def create_conn():
    conn = await asyncio.get_event_loop().run_in_executor(None, psycopg2.connect, database=database_name, user=user,
                                                          password=passw, host=host, port=port)
    logging.info("connected to Postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn, cur


async def check_if_exists_zeus(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        query = "SELECT COUNT(1) FROM Zeuses WHERE steamid = %s"
        values = steamid
        await cur.execute(query, values)
        await conn.commit()
        result = await cur.fetchone()
        if result:
            return True
        return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def check_if_exists_ban(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        query = "SELECT COUNT(1) FROM bans WHERE steamid = %s"
        values = steamid
        await cur.execute(query, values)
        await conn.commit()
        result = await cur.fetchone()
        if result:
            return True
        return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def check_if_exists_infistar(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        query = "SELECT COUNT(1) FROM infistar WHERE steamid = %s"
        values = steamid
        await cur.execute(query, values)
        await conn.commit()
        result = await cur.fetchone()
        if result:
            return True
        return False
    except psycopg2.InterfaceError as e:
        logging.warning()
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def add_zeus(steamid, member) -> bool:
    conn, cur = await create_conn()
    try:
        if not await check_if_exists_zeus(steamid):
            query = "INSERT INTO Zeuses (steamid, member) VALUES (%s, %s)"
            values = (steamid, member)
            await cur.execute(query, values)
            await conn.commit()
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def delete_zeus(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        if await check_if_exists_zeus(steamid):
            query = "DELETE FROM zeuses WHERE steamid = %s"
            values = steamid
            await cur.execute(query, values)
            await conn.commit()
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def get_zeuses():
    conn, cur = await create_conn()
    try:
        query = "SELECT steamid, member FROM Zeuses"
        await cur.execute(query)
        result = await cur.fetchall()
        formatted_result = ""
        async for row in result:
            formatted_result += f"{row['steamid']} - <@!{row['member']}>\n"
        return formatted_result
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def add_infistar(steamid, member, rank) -> bool:
    conn, cur = await create_conn()
    try:
        if not await check_if_exists_infistar(steamid):
            query = "INSERT INTO infistar (steamid, member, rank) VALUES (%s,%s,%s)"
            values = (steamid, member, rank)
            await cur.execute(query, values)
            await conn.commit()
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning()
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def delete_infistar(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        if await check_if_exists_infistar(steamid):
            query = "DELETE FROM infistar WHERE steamid = %s"
            values = steamid
            await cur.execute(query, values)
            await conn.commit()
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def ban_player(steamid, reason, time) -> bool:
    conn, cur = await create_conn()
    try:
        if not await check_if_exists_ban(steamid):
            value, unit = time.split()
            # Create a relativedelta object using the user input
            if unit == 'd':
                duration = relativedelta(days=value)
            elif unit == 'm':
                duration = relativedelta(months=value)
            elif unit == 'y':
                duration = relativedelta(years=value)
            else:
                print('Invalid unit')

            # Add the duration to the current datetime
            if value == 0:

                end_time = 0
            elif value < 0:
                print("Длительность указана неверно")
                return False
            else:
                end_time = datetime.now() + duration

            query = "INSERT INTO bans (steamid, reason, duration) VALUES (%s,%s,%s)"
            values = (steamid, reason, end_time)
            await cur.execute(query, values)
            await conn.commit()
            print(f"Добавил {steamid} бан в базу данных")
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def unban_player(steamid) -> bool:
    conn, cur = await create_conn()
    try:
        if await check_if_exists_ban(steamid):
            query = "DELETE FROM bans WHERE steamid = %s"
            values = steamid
            await cur.execute(query, values)
            await conn.commit()
            print(f"Удалил бан {steamid} из базы данных")
            return True
        else:
            return False
    except psycopg2.InterfaceError as e:
        logging.warning(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()


async def get_bans():
    conn, cur = await create_conn()
    print("Вызвана функция списка бана")
    try:
        query = "SELECT steamid, reason, duration FROM bans"
        print("Делаю запрос в бд")
        await cur.execute(query)
        result = await cur.fetchall()
        if result:
            print("Получил ответ")
        tasks = []
        formatted_result = ""
        for row in result:
            task = asyncio.create_task(format_ban_entry(row))
            tasks.append(task)
        formatted_result = await asyncio.gather(*tasks)
        return "\n".join(formatted_result)
    except psycopg2.InterfaceError as e:
        print(e)
    finally:
        if conn:
            await conn.close()
            await cur.close()
async def format_ban_entry(row):
    return f"{row['steamid']} - <@!{row['reason']}> - duration:{row['duration']}"