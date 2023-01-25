import psycopg2.extras
import re
import logging
import asyncio

passw = "#nUKb9aCc&9"
database_name = "postgres"
user = "postgres"
host = "localhost"
port = "5432"


async def create_conn():
    conn = await asyncio.get_event_loop().run_in_executor(None, psycopg2.connect,database=database_name, user=user, password=passw, host=host,port=port)
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
            await cur.execute(query,values)
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
        for row in result:
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
            values= (steamid, member, rank)
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
            query = "DELETE FROM infistar steamid = %s"
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

