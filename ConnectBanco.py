import psycopg2
import os
from dotenv import load_dotenv

#ler e priorizar o .env com dados sensiveis
load_dotenv(override=True)

try:
    con = psycopg2.connect(
        host = os.getenv("host"),
        database = os.getenv("database"),
        user = os.getenv("user"),
        password = os.getenv("password"),
        port = os.getenv("port"),
    )

    cur = con.cursor()
    cur.execute("SELECT version();")
    resultado = cur.fetchone()

    print("Deu bom!")
    print("Versão do postgreSQL: ", resultado)

    cur.close()
    con.close()

except Exception as e:
    print("Deu ruin: ", e)