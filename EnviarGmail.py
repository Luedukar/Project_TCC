#Imports utilizados
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

#ler e priorizar o .env com dados sensiveis
load_dotenv(override=True)

#variaveis não sensiveis e padrões
assunto = "Monitoramento de preço"

#função que monta e dispara o e-mail
def dispararEmail(nome, destinatario, nome_produto, link, preco_desejado):

    #Mensagem padrão de envio, precisa estar aqui para receber as devidas variaveis
    mensagem_html = f""" 
    <p> Olá {nome}, aqui é o aplicativo vilão passando para avisar</p>
    <p> O produto {nome_produto} atingiu um valor igual ou inferior ao desejado (R$ {preco_desejado}) </p>
    <p> Confera lá, vou deixar o link aqui novamente: {link} <p>
    """
    
    #montar email
    msg = EmailMessage()
    msg["From"] = os.getenv("remetente")
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content("Seu cliente não suporta HTML.")
    msg.add_alternative(mensagem_html, subtype="html")

    #realizar o disparo do e-mail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(os.getenv("remetente"), os.getenv("senha"))
        email.send_message(msg)

    #mensagem de sucesso se o e-mail for enviado 
    print("E-mail enviado com sucesso!")
