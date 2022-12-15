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


async def add_zeus(steamid, member):
    try:
        conn = PostgresConnection.connect
        cur = PostgresConnection.cur
        cur.execute("INSERT INTO Zeuses (steamid, member) VALUES ({steamid},{member})")
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        add_zeus(steamid, member)
    finally:
        conn.commit()
        if cur is not None: cur.close()
        if conn is not None: conn.close()


async def delete_zeus(steamid, member):
    try:
        conn = PostgresConnection.connect
        cur = PostgresConnection.cur
        cur.execute("DELETE FROM Zeuses WHERE steamid = {steamid} AND member = {member}")
    except psycopg2.InterfaceError:
        logging.warning(psycopg2.InterfaceError)
        delete_zeus(steamid, member)
    finally:
        conn.commit()
        if cur is not None: cur.close()
        if conn is not None: conn.close()
