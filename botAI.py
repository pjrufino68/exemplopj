import streamlit as st
import pandas as pd
import PyPDF2
import openai
import keyboard
import os
import psutil
import time
from dotenv import load_dotenv
import secrets

from openai import OpenAI

load_dotenv(override=True)

hide_st_style = """
            <style>
            #bui1 > div > div > ul >ul:nth-child(1) {visibility: hidden;}
            #bui1 > div > div > ul >ul:nth-child(2) {visibility: hidden;}
            #bui1 > div > div > ul >ul:nth-child(4) {visibility: hidden;}
            #bui1 > div > div > ul >ul:nth-child(5) {visibility: hidden;}
            #bui1 > div > div > ul >ul:nth-child(7) {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .reportview-container .main footer {visibility: hidden;}
            </style>
            """
st.set_page_config(page_title="BotTina responde!!!")
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("### 🤖 Dicas & Dúvidas / Fretamento & Turismo")

client = OpenAI(api_key=os.getenv("chaveApi"))

# Função para processar arquivo PDF
def processar_pdf(caminho_pdf):
    with open(caminho_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        textoPDF = ""
        for page in range(len(reader.pages)):
            textoPDF += reader.pages[page].extract_text()
    return textoPDF

# Função para processar arquivos CSV
def processar_csv(caminho_csv):
    df = pd.read_csv(caminho_csv)
    return df.to_string()

# Função para processar arquivos de texto (.txt)
def processar_txt(caminho_txt):
    with open(caminho_txt, "r", encoding="utf-8") as file:
        return file.read()
    
# Carregar o conteúdo dos arquivos da pasta secreta
def carregar_arquivos_secretos(pasta_secreta):
    dados_adicionais = {}
    
    # Caminhos dos arquivos

    #caminho_pdf = os.path.join(pasta_secreta, "dados.pdf")
    #caminho_csv = os.path.join(pasta_secreta, "dados.csv")
    #caminho_txt = os.path.join(pasta_secreta, "dados.txt")
    
    caminho_pdf = st.secrets["dados"]["arquivoPDF"]
    caminho_csv = st.secrets["dados"]["arquivoCSV"]
    caminho_txt = st.secrets["dados"]["arquivoTXT"]

    #print(caminho_pdf)
    #print(caminho_txt)

    # Processar arquivos se existirem
    if os.path.exists(caminho_pdf):
        dados_adicionais["pdf"] = processar_pdf(caminho_pdf)
    else:
        dados_adicionais["pdf"] = "Arquivo PDF não encontrado."
    
    #if os.path.exists(caminho_csv):
    #    dados_adicionais["csv"] = processar_csv(caminho_csv)
    #else:
    #    dados_adicionais["csv"] = "Arquivo CSV não encontrado."
    
    if os.path.exists(caminho_txt):
        dados_adicionais["txt"] = processar_txt(caminho_txt)
    else:
        dados_adicionais["txt"] = "Arquivo TXT não encontrado."
    
    return dados_adicionais

# Caminho para a pasta secreta (ajuste conforme necessário)
pasta_secreta = "/dados"

# Carregar o conteúdo dos arquivos
dados_adicionais = carregar_arquivos_secretos(pasta_secreta)

maisDados = f"""Usar também estas informações:
    
    {dados_adicionais['pdf']}
    
    {dados_adicionais['txt']}
    """
# Instrucoes iniciais para o Bot
assistant_instructions = {
    "role": "system",
    "content": os.getenv("contentBot") + maisDados
}

#print (maisDados)
#st.write(maisDados)

lista = []
lista.insert(0, assistant_instructions)

st.session_state["messages"] = lista

@st.cache_data

def enviarIA(textoRecebido, _lista):
    lista.append(assistant_instructions)
    lista.append({"role": "user", "content": texto})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=lista)
    lista.append(response)
    return response.choices[0].message.content

with st.container():
    i = 0
    texto = ""
    texto_voz = ""

    while True:
        texto = st.text_input("", placeholder="Faça sua pergunta", key=f'texto_{i}')

        if texto == "fim" or len(texto) < 1:
            break
        else:
            msg = enviarIA(texto, lista)
            st.chat_message("🤖").write(msg)
        i = i + 1
        

