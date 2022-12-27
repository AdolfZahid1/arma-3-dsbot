import psycopg2.extras
import re
import logging
import asyncio

passw = "#nUKb9aCc&9"
database_name = "postgres"
user = "postgres"
host = "localhost"
port = "5432"


class PostgresConnection:
    """Describe connections to postgres"""
    connect = psycopg2.connect(database=database_name, user=user, password=passw, host=host,
                               port=port)
    logging.info("connected to Postgres")
    cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


async def check_if_exists_zeus(steamid) -> bool:
    try:
        conn = PostgresConnection.connect
        cur = PostgresConnection.cur
        query = "SELECT COUNT(1) FROM Zeuses WHERE steamid = %s"
        values = steamid
        cur.execute(query, values)
        conn.commit()
        result = cur.fetchone()
        if result:
            return True
        return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        check_if_exists_zeus(steamid)
    finally:
        if conn:
            conn.close()
            cur.close()
        return False


async def check_if_exists_infistar(steamid) -> bool:
    try:
        conn = PostgresConnection.connect
        cur = PostgresConnection.cur
        query = "SELECT COUNT(1) FROM infistar WHERE steamid = %s"
        values = steamid
        cur.execute(query, values)
        conn.commit()
        result = cur.fetchone()
        if result:
            return True
        return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        check_if_exists_infistar(steamid)
    finally:
        if conn:
            cur.close()
            conn.close()
        return False


async def add_zeus(steamid, member) -> bool:
    try:
        if not check_if_exists_zeus(steamid):
            conn = PostgresConnection.connect
            cur = PostgresConnection.cur
            query = "INSERT INTO Zeuses (steamid, member) VALUES (%s, %s)"
            values = (steamid, member)
            cur.execute(query, values)
            conn.commit()
        else:
            return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        add_zeus(steamid, member)
    finally:
        if conn:
            conn.close()
            cur.close()
        return True


async def delete_zeus(steamid) -> bool:
    try:
        if check_if_exists_zeus(steamid):
            conn = PostgresConnection.connect
            cur = PostgresConnection.cur
            query = "DELETE FROM zeuses WHERE steamid = %s"
            values = steamid
            cur.execute(query,values)
            conn.commit()
        else:
            return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        delete_zeus(steamid)
    finally:
        if conn:
            conn.close()
            cur.close()
        return True


async def add_infistar(steamid, member, rank) -> bool:
    try:
        if not check_if_exists_infistar:
            conn = PostgresConnection.connect
            cur = PostgresConnection.cur
            query = "INSERT INTO infistar (steamid, member, rank) VALUES (%s,%s,%s)"
            values= (steamid, member, rank)
            cur.execute(query, values)
            conn.commit()
        else:
            return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        add_infistar(steamid, member, rank)
    finally:
        if conn:
            conn.close()
            cur.close()
        return True


async def delete_infistar(steamid) -> bool:
    try:
        if check_if_exists_infistar:
            conn = PostgresConnection.connect
            cur = PostgresConnection.cur
            query = "DELETE FROM infistar steamid = %s"
            values = steamid
            cur.execute(query, values)
            conn.commit()
        else:
            return False
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        delete_zeus(steamid)
    finally:
        if conn:
            conn.close()
            cur.close()
        return True

