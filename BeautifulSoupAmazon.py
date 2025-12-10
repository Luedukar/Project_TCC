#imports utilizados
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bf
import time as tm
import re
import EnviarGmail as gm
import schedule
from schedule import repeat, every
import datetime

#Função para converter a string preco em um float
def converte_string_float (preco):
    preco = preco.split()
    preco = preco[1]
    preco = preco.replace('.', '')
    preco = preco.replace(',', '.')
    preco = float(preco)
    return preco

#Função para extrair or valores em meio ao texto 
def extrair_preco_de_texto(texto):
    # encontra padrões como 3.599,04 ou 3299,00
    matches = re.findall(r'\d{1,3}(?:\.\d{3})*(?:,\d{2})', texto)
    if not matches:
        return None
    s = matches[-1]
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None

#Variaveis de entrada:
nome = input("Insira seu nome: ")
destinatario = input("Insira o e-mail na qual deseja ser avisado: ")
nome_produto = input("Insira o nome do produto que deseja acompanhar: ")
link = input("Insira o link completo do produto que deseja acompanhar: ")
preco_desejado = float(input("Insira o preço desejado: "))

#loop e função principal
@repeat(every(5).minutes)

def main():
    # Abre o navegador (Chrome)
    driver = webdriver.Chrome()
    driver.get(link)

    # Espera o site carregar (ajuste o tempo conforme necessário)
    tm.sleep(5)

    # Ler o HTML e extrair o que for preciso direto da pag web com o BeautifulSoup
    site = bf(driver.page_source, "html.parser")
    preco= []
    valores1 = site.find('span', class_='aok-offscreen')
    valores2 = site.find_all('span', class_="olpWrapper a-size-small")
    preco.append(valores1)
    preco.append(valores2)

    driver.quit()

    #Pega todos os preços encontrados (texto todo poluido) passa 1 por 1 dos itens fazendo as devidas conversões
    precos_encontrados = []
    for tag in preco:
        texto = tag.get_text() if hasattr(tag, 'get_text') else str(tag)
        valor = extrair_preco_de_texto(texto)
        if valor is not None:
            precos_encontrados.append(valor)

    #Imprimi todos os preços encontrados 9comente caso não seja necessario)
    print(precos_encontrados)
    
    #enviar Email fica desativado quando usado no PC da firma pois não funciona, no PC de casa é só descomentar
    #Encontra o menor preço na lista (esse que interresa), se for dentro do preço desejado, envia o email
    if precos_encontrados:
        print("Menor preço:", min(precos_encontrados))
        if min(precos_encontrados) <= preco_desejado:
            print("Pode comprar")
            gm.dispararEmail(nome, destinatario, nome_produto, link, preco_desejado)
        else: print("O Preço encontrado está acima do desejado")
    else:
        #Caso não tenha sido encontrado nenhum preço
        print("Preço não encontrado")
    
    #Validação do loop de tempo, informando a hora da execução dessa linha (comentar quando não for mais util)
    data_hora = datetime.datetime.now()
    print("Hora da operação: ", data_hora )

#Roda o loop infinitamente
while True:
    schedule.run_pending()
    tm.sleep(1)