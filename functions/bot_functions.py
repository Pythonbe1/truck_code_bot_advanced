from datetime import timedelta
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_data_from_db(id):
    con = psycopg2.connect(dbname=os.environ.get("PG_NAME"),
                           user=os.environ.get("PG_USER"),
                           password=os.environ.get("PG_PASSWORD"),
                           host=os.environ.get("PG_HOST"),
                           port=os.environ.get("PG_PORT"))
    query = f"SELECT * from user_info where chat_id={id}"
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
    # elif kind == 'update':
    #     sql = f"""update user_info
    #             set quantity = quantity+1,
    #                 link_name='{link}'
    #             where chat_id={id}"""
    #     cur.execute(sql)
    #     conn.commit()
    #     cur.close()
