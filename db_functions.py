import mysql.connector
from config import *

#Estabelece conexão com o DB
def conectar_db():
    conexao = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
    cursor = conexao.cursor(dictionary=True)
    return conexao, cursor

#Encerra a conexao com o DB
def encerrar_db(cursor, conexao):
    cursor.close
    conexao.close

def limpar_input(campo):
    campoLimpo = campo.replace(".","").replace("/","").replace("-","").replace(" ","").replace("(","").replace("R$","").replace(")","")
    return campoLimpo