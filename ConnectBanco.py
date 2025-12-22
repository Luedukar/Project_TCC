import psycopg2
import os
from dotenv import load_dotenv
from decimal import Decimal

#ler e priorizar o .env com dados sensiveis
load_dotenv(override=True)

try:
    #Conexão com o banco
    def get_connection():
        return psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            port=os.getenv("port"),
        )
    
    #Encontrar dados do produto com base em seu ID
    def navegarbanco(product_id):
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM produtos WHERE productID = %s", (product_id,))
                row = cur.fetchone()

                if not row:
                    return None

                return row
            
    #Encontrar todos os IDs de produtos
    def extrairID():
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("SELECT productID FROM produtos")
                return [row[0] for row in cur.fetchall()]
            
    #Encontrar informações do usuario com base em um ID de usuario
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
            
    #Caso o e-mail seja enviado, alterar no banco para evitar multiplos envios diarios do mesmo item
    def avisoEnviado(id):
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute(f"UPDATE produtos SET AvisoDiario = TRUE, atualizado = NOW() WHERE productid = {id}")
                print(f"horario alterado para id: {id}")

    #Caso o tempo desde o ultimo aviso seja maior que 24 horas, o item volta a estar apto para enviar um novo aviso
    def ResetAviso():
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("UPDATE produtos SET AvisoDiario = FALSE, atualizado = NOW() WHERE AvisoDiario = TRUE AND atualizado < NOW() - INTERVAL '24 hours';")
                print("Executado")
      
except Exception as e:
    print("Erro: ", e)