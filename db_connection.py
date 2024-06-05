import os
from dotenv import load_dotenv
import psycopg2



load_dotenv('.env')


def get_conn_cur():
    conn = psycopg2.connect(
        host=os.getenv('HNAME'),
        dbname=os.getenv('DBNAME'),
        user=os.getenv('UNAME'),
        password=os.getenv('PASSWORD'),
        port=os.getenv('PORT')
    )
    cur = conn.cursor()

    return conn, cur


conn, cur = get_conn_cur()

create_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR (20) UNIQUE NOT NULL,
        email VARCHAR (40)  UNIQUE NOT NULL,
        password VARCHAR (40) NOT NULL
    );
"""

create_table2 = """
    CREATE TABLE IF NOT EXISTS api_keys (
        key_id SERIAL PRIMARY KEY,
        key VARCHAR (20) UNIQUE NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
"""

cur.execute(create_table)
cur.execute(create_table2)

conn.commit()
cur.close()
conn.close()
