import uvicorn
from fastapi import FastAPI, HTTPException
from db_connection import get_conn_cur
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import secrets

app = FastAPI()
conn, cur = get_conn_cur()

class User(BaseModel):
    name: str
    email: str
    password: str

class APIResponse(BaseModel):
    key: str


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

    insert_script = f"""
        INSERT INTO users (name, email, password) VALUES ('{user.name}', '{user.email}', '{user.password}');
    """
    cur.execute(insert_script)
    conn.commit()
    cur.close()
    conn.close()

    return {"msg": "User registered successfully"}




if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
