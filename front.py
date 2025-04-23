
import streamlit as st
import pymongo
import pandas as pd
import time
import altair as alt
from datetime import datetime
from pymongo import MongoClient


# Configurar a tela em formato wide
st.set_page_config(layout="wide")

# ******************************************** EXTRAÇÃO DOS DADOS *****************************************************

# Configuração do MongoDB Atlas (substitua pelos seus dados e suas credenciais do MongoDB Atlas)
MONGO_URI = ""
DB_NAME = ""
COLLECTION_NAME = ""

# Conectar ao MongoDB Atlas
@st.cache_resource
def get_database():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[DB_NAME]

db = get_database()
collection = db[COLLECTION_NAME]

# Função para buscar os dados
def fetch_all_data():
    try:
        all_documents = collection.find()
        all_cotacoes = []
        for doc in all_documents:
            all_cotacoes.extend(doc.get("cotacoes", []))
        df = pd.DataFrame(all_cotacoes)
        df["dt_extracao"] = pd.to_datetime(df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")

        return df
    except Exception as e:
        st.error(f"Erro ao recuperar os dados do MongoDB: {str(e)}")
        return None


# Função para buscar o ultimo registro
def fetch_last_data():
    try:
        # Buscar apenas o último documento inserido no MongoDB
        last_document = collection.find_one(sort=[("_id", -1)])  # Ordena pelo _id (assumindo que _id é crescente)
        
        if not last_document or "cotacoes" not in last_document:
            return None
        
        # Criar um DataFrame com os dados do último documento
        df = pd.DataFrame(last_document["cotacoes"])
        df["dt_extracao"] = pd.to_datetime(df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
        
        return df
    except Exception as e:
        st.error(f"Erro ao recuperar os dados do MongoDB: {str(e)}")
        return None


# ******************************************* FROMATAÇÃO SCROLLER *****************************************************

last = fetch_last_data()

if last is not None and not last.empty:
    moedas = [tuple(row) for row in last[['code', 'bid']].values]


# Criando a string para exibição com espaçamento maior entre moedas
espaco = "    "  # Espaço entre as moedas
texto_base = espaco.join(
    [f"{moeda}: <span style='color: #02E201; font-weight: bold;'>R${valor:,.2f}</span>" for moeda, valor in moedas]
)



# Função para obter a data e hora da última atualização
def get_last_updated():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

# CSS atualizado para o scroller
css = """
<style>
.title {
    font-size: 32px !important;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}
.scroller-container {
    width: 60%;
    overflow: hidden;
    white-space: nowrap;
    margin: auto;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}
.scroller-text {
    font-size: 24px !important;
    font-weight: bold;
    font-family: Arial, sans-serif;
    display: inline-block;
    animation: scrollText 15s linear infinite;
}
.update-time {
    font-size: 18px;
    font-weight: bold;
    color: #555;
    margin: 10px 0;
}
@keyframes scrollText {
    from { transform: translateX(100%); }
    to { transform: translateX(-100%); }
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Criando a estrutura do container para exibição do scroller
container_style = """
<div style="width: 60%; margin: auto; text-align: center;">
    <img src="https://i.postimg.cc/tTc29F0x/Capa.png" width="1200">
    <div>---</div>
    <div>
        Frequência atualizações: 
        <span style="color:#02E201;">API - Tempo real</span> | 
        <span style="color:#02E201;">MongoDb Atlas - 60 segundos</span> | 
        <span style="color:#02E201;">Streamlit - 30 segundos</span>
    </div>
    <div class="update-time">Última atualização dashboard: {}</div>
    <div>---</div>
    <div class="scroller-container">
        <p class="scroller-text">{}</p>
    </div>
</div>
""".format(get_last_updated(), texto_base)

# Exibir a estrutura completa centralizada
st.markdown(container_style, unsafe_allow_html=True)

# ******************************************************* ÚLTIMA COTAÇÃO ****************************************************

# Atualizar os dados periodicamente
df = fetch_all_data()

if df is not None and not df.empty:
    df['ask'] = pd.to_numeric(df['ask'], errors='coerce')
    df['bid'] = pd.to_numeric(df['bid'], errors='coerce')
    df['dt_extracao'] = pd.to_datetime(df['dt_extracao'], errors='coerce')

    # Criar lista de moedas disponíveis
    available_currencies = df['name'].unique().tolist()

    # Centralizar o seletor de moeda e o texto "Última Cotação"
    container_style_seletor = """
    <div style="width: 50%; margin: auto; text-align: left; padding: 10px;">
        <p style="font-size: 18px; color: gray;font-weight: bold;"> Selecione a moeda:</p>
    </div>
    """
    st.markdown(container_style_seletor, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])  # A coluna do meio será maior
    with col2:
        selected_currency = st.selectbox("", available_currencies, key="moeda")

    # Aplicar CSS para aumentar o tamanho da fonte do selectbox acima
    st.markdown(
        """
        <style>
            div[data-baseweb="select"] {
                font-size: 20px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centralizar o título "Última Cotação"
    container_style_titulo = """
    <div style="width: 50%; margin: auto; text-align: left; padding: 10px;">
        <p style="font-size: 18px; color: gray;font-weight: bold;">Última Cotação da Moeda Selecionada</p>
    </div>
    """
    st.markdown(container_style_titulo, unsafe_allow_html=True)

    # Filtrar dados para a moeda selecionada
    df_currency = df[df['name'] == selected_currency]

    # Ordenar os dados por data para pegar as últimas cotações
    df_currency = df_currency.sort_values(by='dt_extracao', ascending=False)
    
    # Selecionar as últimas 50 cotações
    df_currency_last_50 = df_currency.head(50)

    # Exibir a última cotação
    last_record = df_currency_last_50.iloc[0]
    
    container_style_cotacao = """
    <div style="width: 50%; margin: auto; text-align: left; border: 2px solid gray; padding: 10px; border-radius: 10px;">
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">💰 Preço de Compra: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{}</span></p>
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">💲 Preço de Venda: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{}</span></p>
        <p style="font-size: 18px; font-weight: bold; color: #fffff;">📅 Última Atualização: <span style="font-size: 20px; font-weight: bold; color: #02E201;">{}</span></p>
    </div>
    """.format(last_record['bid'], last_record['ask'], last_record['dt_extracao'])

    st.markdown(container_style_cotacao, unsafe_allow_html=True)

    # Criar uma linha horizontal centralizada
    st.markdown(
        """
        <div style="width: 50%; margin: auto;">
            <hr style="border: 1px solid gray;">
        </div>
        """,
        unsafe_allow_html=True
    )

# ************************************ GRÁFICO DE LINHA **********************************************************************
    # Exibir título

    df_fig = df_currency[['bid', 'ask', 'dt_extracao']]
    df_fig['dt_extracao'] = pd.to_datetime(df_fig['dt_extracao'], errors='coerce')

    # Definir a coluna 'dt_extracao' como índice
    df_fig.set_index('dt_extracao', inplace=True)

    # Agrupar os dados em períodos de 10 minutos e calcular a média para 'bid' e 'ask'
    df_fig_resample = df_fig.resample('60T').mean()
    
    df_fig_resample = df_fig_resample.dropna()
    #st.dataframe(df_fig_resample)
    # Resetar o índice, se necessário, para continuar manipulando o DataFrame
    df_fig_resample.reset_index(inplace=True)

    # Exibir o DataFrame resultante
    #st.write(df_fig_resample)
    df_currency_last_50 = df_fig_resample
    style_titulo = """
    <div style="width: 50%; margin: auto; text-align: left; padding: 10px;">
        <p style="font-size: 18px; color: gray;font-weight: bold;"> Evolução moeda selecionada </p>
    </div>
    """
    st.markdown(style_titulo, unsafe_allow_html=True)

    # Alterar os nomes de 'bid' e 'ask' para 'compra' e 'venda' no gráfico
    df_currency_last_50['compra'] = df_fig_resample['bid']
    df_currency_last_50['venda'] = df_fig_resample['ask']

    # Criar layout para os botões
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])

    with col2:
        compra_button = st.button("Compra", use_container_width=True)

    with col3:
        venda_button = st.button("Venda", use_container_width=True)

    # Determinar a escolha do usuário, padrão 'compra'
    display_choice = "compra" 
    if compra_button:
        display_choice = "compra"
    elif venda_button:
        display_choice = "venda"
    # Calcular o mínimo e máximo dinâmicos
    min_val = df_currency_last_50[display_choice].min()
    max_val = df_currency_last_50[display_choice].max()
    min_limit = min_val * 0.9  # 30% abaixo do mínimo
    max_limit = max_val * 1.1  # 30% acima do máximo



    # Criar o gráfico com linha e marcadores
    line_chart = alt.Chart(df_currency_last_50).mark_line(
        strokeWidth=2
    ).encode(
        x=alt.X('dt_extracao:T', axis=alt.Axis(title=None)),
        y=alt.Y(f'{display_choice}:Q', axis=alt.Axis(title=None),scale=alt.Scale(domain=[min_limit, max_limit])),  # Escolha dinâmica entre compra/venda
    
        color=alt.value("#02E201" if display_choice == "compra" else "#FE0560")  # Verde para compra, vermelho para venda
    )

    # Adicionar marcadores nos pontos
    point_chart = alt.Chart(df_currency_last_50).mark_circle(
        size=50  # Tamanho dos pontos
    ).encode(
        x='dt_extracao:T',
        y=f'{display_choice}:Q',
        color=alt.value("#02E201" if display_choice == "compra" else "#FE0560")
    )

    # Combinar linha e pontos
    chart = (line_chart + point_chart).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_view(
        stroke=None
    )

    # Exibir o gráfico centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(chart, use_container_width=True)


else:
    st.warning("⚠️ Nenhum dado encontrado no banco!")

# ******************************** REFRESH PÁGINA *****************************************************************************

update_interval = 30

# Atualização automática da página
st.query_params["refresh_time"] = int(time.time())
time.sleep(update_interval) 
st.rerun()