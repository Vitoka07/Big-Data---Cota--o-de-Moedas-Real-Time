# Cotação de Moedas em Tempo Real👑 

![Dashboard em execução](https://github.com/user-attachments/assets/f4b2001a-d42b-4e49-9605-2345cdde9cd4)

---

## 📌 Sobre o Projeto

Este repositório contém um projeto dividido em **Back-End** e **Front-End**, que coleta cotações de moedas em tempo real e exibe os dados em um dashboard interativo utilizando **Streamlit**. As cotações são armazenadas em uma base **MongoDB Atlas**.

O **back-end** e o **front-end** operam em **intervalos distintos de atualização**, o que permite obter a melhor granularidade possível sem sobrecarregar o sistema. O usuário pode escolher uma moeda e visualizar sua variação ao longo do tempo.

---

## 🚀 Objetivo

- Coletar dados de cotação de moedas de forma contínua.
- Armazenar as cotações em banco de dados MongoDB.
- Disponibilizar visualização através de um painel interativo com Streamlit.

---

## 💻 Tecnologias Utilizadas

- Python
- MongoDB Atlas
- API AwesomeAPI ([https://economia.awesomeapi.com.br](https://economia.awesomeapi.com.br))
- Streamlit
- Pandas
- Requests

---

## Funcionalidades do Dashboard 🌐
 - Scroller de cotações em tempo real
 - Seletor de moedas
 - Exibição da última cotação com compra/venda
 - Gráfico de evolução horária das cotações
 - Atualização automática a cada 30 segundos
 - Escolha de moeda para acompanhar sua variação ao longo do tempo

---

## ⚙️ Configurações Iniciais

### 1. Criar um cluster no MongoDB Atlas

- Acesse: [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Crie um cluster gratuito
- Crie um banco de dados e uma coleção
- Copie a URI de conexão (ex: `mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/test`)

### 2. Configure suas credenciais no código

Substitua os valores das variáveis abaixo nos arquivos `backend.py` e `frontend.py`:

```python
MONGO_URI = "mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "nome_do_banco"
COLLECTION_NAME = "nome_da_colecao"
```

---

## 🚡 Como Executar
 - ▶️ Backend (Coleta de dados e armazenamento)
 - Rode isso no Terminal: `python backend.py`
   
Obs: Este script irá coletar dados da API a cada 30 segundos e armazenar no MongoDB. O backend é projetado para atualizar os dados continuamente e fornecer a maior granularidade possível nas cotações.

- 🖥️ Frontend (Dashboard Interativo)
- Rode no Terminal: `streamlit run frontend.py`

Obs: O frontend realiza atualizações automáticas em intervalos distintos do backend, permitindo uma visualização eficiente sem sobrecarregar o sistema.

---

## 📖 Licença

Este projeto é licenciado sob a Licença MIT.
