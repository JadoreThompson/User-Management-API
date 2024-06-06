import uvicorn
from fastapi import FastAPI, HTTPException, Header
from typing import Union
from datetime import datetime, timedelta
from db_connection import get_conn_cur
from pydantic import BaseModel

import os
from dotenv import load_dotenv
import jwt
from typing_extensions import Annotated
import secrets
import hashlib

import smtplib
import ssl
from email.message import EmailMessage

# ENVIRONMENT VARIABLES

load_dotenv('.env')
app = FastAPI()
conn, cur = get_conn_cur()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

h = hashlib.new('sha256')
# PYDANTIC MODELS

class User(BaseModel):
    name: str
    email: str
    password: str

class APIResponse(BaseModel):
    key: str

class Email(BaseModel):
    sender: str
    recipient: str
    subject: str
    message: str

#ENDPOINTS

@app.get('/')
def read_root():
    return {"msg": "yes"}

@app.post('/register')
def register(user: User):
    db_query = f"""
        SELECT * FROM users WHERE email = '{user.email}' ;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    if len(rows) > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hashlib.md5(user.password.encode())
    insert_script = f"""
        INSERT INTO users (name, email, password) VALUES ('{user.name}', '{user.email}', '{hashed_password}');
    """
    cur.execute(insert_script)

    key = secrets.token_urlsafe(10)
    key_script = f"""
        INSERT INTO api_keys (key, user_id)
        VALUES ('{key}', (SELECT user_id FROM users WHERE email = '{user.email}')) ;
    """
    cur.execute(key_script)

    conn.commit()
    cur.close()
    conn.close()

    raise HTTPException(status_code=200, detail="User registered successfully", headers={"key": key})


@app.post('/login/{api_key}')
def login(user: User):
    hashed_password = hashlib.md5(user.password.encode())
    db_query = f"""
        SELECT * FROM users WHERE email = '{user.email}' AND password = '{hashed_password}' ;
    """
    cur.execute(db_query)
    rows = cur.fetchall()

    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # api_script = f"""
    #     SELECT * FROM api_keys WHERE key = '{api_key}' ;
    # """
    # cur.execute(api_script)
    # rows = cur.fetchall()
    # if len(rows) == 0:
    #     raise HTTPException(status_code=400, detail="Invalid API key")


    conn.commit()
    cur.close()
    conn.close()

    raise HTTPException(status_code=200, detail="User logged in successfully")


@app.post('/email/send')
def send_email(email: Email, api_key: str = Header(None)):
    api_script = f"""
        SELECT * FROM api_keys WHERE key = '{api_key}' ;
    """
    cur.execute(api_script)
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="Invalid API key")

    try:
        em = EmailMessage()
        em['From'] = email.sender
        em['To'] = email.recipient
        em['Subject'] = email.subject
        em.set_content(email.body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(email.sender, os.getenv('EMAIL_PASSWORD'))
            server.sendmail(email.sender, email.recipient, em.as_string())

    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

    conn.commit()
    cur.close()
    conn.close()

    raise HTTPException(status_code=200, detail="Email sent successfully")




if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
