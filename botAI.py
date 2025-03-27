import streamlit as st
import openai
import keyboard
import os
import psutil
import time
from dotenv import load_dotenv

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
st.set_page_config(page_title="hacBot responde!!!")
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("### :sunglasses: Dicas & Dúvidas / Hospedagem & Turismo")

client = OpenAI(api_key=os.getenv("chaveApi"))

# Instrucoes iniciais para o Bot
assistant_instructions = {
    "role": "system",
    "content": os.getenv("contentBot")
}

lista = []
lista.insert(0, assistant_instructions)

st.session_state["messages"] = lista

@st.cache_data

def enviarIA(textoRecebido, _lista):
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
            st.chat_message("assistant").write(msg)
        i = i + 1
        

