import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()  # завантажує змінні із .env
DB_PASSWORD = os.getenv("DB_PASSWORD")

CONNECT = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=DB_PASSWORD,
    database="Silicon_Store_DB_TEST"
)
