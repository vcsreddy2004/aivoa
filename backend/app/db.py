# app/db.py
import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MY_SQL_HOST"),
        user=os.getenv("MY_SQL_USER"),
        password=os.getenv("MY_SQL_PASSWORD"),
        database=os.getenv("MY_SQL_DB")
    )