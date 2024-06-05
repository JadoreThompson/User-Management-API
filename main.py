import uvicorn
from fastapi import FastAPI, HTTPException
from db_connection import get_conn_cur, User, APIResponse
import jwt
from datetime import datetime, timedelta
import secrets

app = FastAPI()
conn, cur = get_conn_cur()


@app.get('/')
def read_root():
    return {"msg": "up and running"}




if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
