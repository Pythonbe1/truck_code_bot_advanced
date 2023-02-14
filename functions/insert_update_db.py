from datetime import timedelta
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_data_from_db(sql):
    con = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                           user=os.environ.get("PG_USER"),
                           password=os.environ.get("PG_PASSWORD"),
                           host=os.environ.get("PG_HOST"),
                           port=int(os.environ.get("PG_PORT")))
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

        cur.execute(sql)
        conn.commit()
        cur.close()


def insert_chat_id__truck_number(id, text, date, kind):
    conn = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                            user=os.environ.get("PG_USER"),
                            password=os.environ.get("PG_PASSWORD"),
                            host=os.environ.get("PG_HOST"),
                            port=os.environ.get("PG_PORT"))
    cur = conn.cursor()
    if kind == 'insert':
        sql = f""" INSERT INTO user_truck_info (chat_id, truck_code, added_date)
                         VALUES ({id}, '{text}', '{date}');"""
        cur.execute(sql)
        conn.commit()
        cur.close()


def insert_chat_id_permission(id):
    conn = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                            user=os.environ.get("PG_USER"),
                            password=os.environ.get("PG_PASSWORD"),
                            host=os.environ.get("PG_HOST"),
                            port=os.environ.get("PG_PORT"))
    cur = conn.cursor()
    sql = f"""Update user_truck_info
     set is_paid=True where chat_id={id}"""
    cur.execute(sql)
    conn.commit()
    cur.close()
