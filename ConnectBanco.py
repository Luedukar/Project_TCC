import psycopg2
import os
from dotenv import load_dotenv
from decimal import Decimal

#ler e priorizar o .env com dados sensiveis
load_dotenv(override=True)

try:
    def get_connection():
        return psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            port=os.getenv("port"),
        )

    def navegarbanco(product_id):
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM produtos WHERE productID = %s", (product_id,))
                row = cur.fetchone()

                if not row:
                    return None

                return {
                    "productID": row[0],
                    "userID": row[1],
                    "nome": row[2],
                    "preco": float(row[3]) if isinstance(row[3], Decimal) else row[3],
                    "link": row[4],
                    "ativo": row[5],
                    "expirado": row[6],
                    "data": row[7]
                }
            
    def extrairID():
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("SELECT productID FROM produtos")
                return [row[0] for row in cur.fetchall()]
            
    def navegarbancoUsers(id):
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute(
                    "SELECT * FROM users WHERE id = %s",
                    (id,)
                )
                row = cur.fetchone()
                resultado = list(row) if row else []
                return resultado
    
      
except Exception as e:
    print("Deu ruin: ", e)