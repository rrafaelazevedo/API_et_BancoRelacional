# conexão com o database e enviar dados para o dash
# pip install mysql-connector-python

import mysql
import mysql.connector
import pandas as pd

# conexão
def conexao(query):
    conn = mysql.connector.connect(
        host = '127.0.0.1',
        port = '3306',
        user = 'root',
        password = 'senai@134',
        db = 'bd_carro')
    
    dataframe = pd.read_sql(query, conn)
    # executa a consulta SQL e armazena o resultado em um dataframe    

    conn.close()
    return dataframe

