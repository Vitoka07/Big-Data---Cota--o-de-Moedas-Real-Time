import time
import requests
import pymongo
import pandas as pd
from pymongo import MongoClient
from datetime import datetime


# Configuração do MongoDB Atlas (substitua pelos seus dados e suas credenciais do MongoDB Atlas)
MONGO_URI = ""
DB_NAME = ""
COLLECTION_NAME = ""

# Conectar ao MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# URL da API
data_url = "https://economia.awesomeapi.com.br/last/USD-BRLPTAX,EUR-BRLPTAX,BTC-BRL,ETH-BRL,BNB-BRL"

def fetch_and_store_data():
    try:
        response = requests.get(data_url)
        if response.status_code == 200:
            data = response.json()
            dt_extracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Filtrar apenas os campos necessários
            filtered_data = []
            for key, value in data.items():
                filtered_data.append({
                    "code": value["code"],
                    "codein": value["codein"],
                    "name": value["name"],
                    "bid": float(value["bid"]),
                    "ask": float(value["ask"]),
                    "timestamp": int(value["timestamp"]),
                    "create_date": value["create_date"],
                    "dt_extracao": dt_extracao

                })
            
            # Criar DataFrame
            df = pd.DataFrame(filtered_data)
            print("DataFrame criado com sucesso:")
            print(df)
            
            # Inserir dados no MongoDB
            document = {
                "timestamp": time.time(),
                "cotacoes": filtered_data
            }
            collection.insert_one(document)
            print("Dados inseridos com sucesso:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print(f"Erro ao buscar os dados: {response.status_code}")
    except Exception as e:
        print("Erro na requisição ou inserção no MongoDB:", str(e))

# Loop para buscar e armazenar dados a cada xx segundos
while True:
    fetch_and_store_data()
    time.sleep(30)