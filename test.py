from datetime import datetime, timedelta
from main import User
from db_connection import get_conn_cur
import secrets
import bcrypt
import hashlib

conn, cur = get_conn_cur()


h = hashlib.new('sha256')
h.update(b"password".encode())
print(h.hexdigest())
