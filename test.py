from datetime import datetime, timedelta
from main import User
from db_connection import get_conn_cur
import secrets

conn, cur = get_conn_cur()


# user = User(name='john', email='john@email.com', password='password')
# db_query = f"""
#     SELECT * FROM users WHERE email = '{user.email}' ;
# """
# cur.execute(db_query)
# rows = cur.fetchall()
#
# cur.close()
# conn.close()
#
# print(rows)
#
# # print(datetime.now()+timedelta(minutes=15))

print(secrets.token_urlsafe(16))
