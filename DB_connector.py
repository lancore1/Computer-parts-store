import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()  # завантажує змінні із .env
DB_PASSWORD = os.getenv("DB_PASSWORD")

# const connect to DB
CONNECT = mysql.connector.connect(
    host="mysql-3e73850d-kravastok13345-85d8.d.aivencloud.com",
    port=16533,
    user="avnadmin",
    password=DB_PASSWORD,
    database="Silicon_Store_DB"
)
