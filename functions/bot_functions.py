from datetime import timedelta
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_data_from_db(id, sql):
    con = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                           user=os.environ.get("PG_USER"),
                           password=os.environ.get("PG_PASSWORD"),
                           host=os.environ.get("PG_HOST"),
                           port=os.environ.get("PG_PORT"))
    query = sql
    df = pd.read_sql_query(query, con)
    return df


def insert_db(id, first_name, second_name, link, kind):
    conn = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                            user=os.environ.get("PG_USER"),
                            password=os.environ.get("PG_PASSWORD"),
                            host=os.environ.get("PG_HOST"),
                            port=os.environ.get("PG_PORT"))
    cur = conn.cursor()
    if kind == 'insert':
        sql = f""" INSERT INTO user_info (chat_id, first_name, last_name, username)
                 VALUES ({id}, '{first_name}', '{second_name}', '{link}');"""
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()


def insert_chat_id__truck_number(id, text, kind):
    conn = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                            user=os.environ.get("PG_USER"),
                            password=os.environ.get("PG_PASSWORD"),
                            host=os.environ.get("PG_HOST"),
                            port=os.environ.get("PG_PORT"))
    cur = conn.cursor()
    if kind == 'insert':
        sql = f""" INSERT INTO user_truck_info (chat_id, truck_number)
                         VALUES ({id}, '{text}');"""

    elif kind == 'update':
        pass
