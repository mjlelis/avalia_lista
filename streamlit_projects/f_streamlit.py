import streamlit as st
import numpy as np
import pandas as pd

st.title("teste APP")
st.write("Este aplicativo tem como objetivo permitir aos avaliadores validares a aderência de uma ocorrência dentro do mesmo conjunto")

df = pd.DataFrame({
    "coluna 1":[1,2,3,4,5,6],
    "coluna_2": [30,40,50,60,70,80]
})

df

option = st.selectbox(
    " O que selecionar",
    df["coluna 1"]
)

"voce selecionou", option

coluna_direita, coluna_esquerda = st.beta_columns(2)
pressionado = coluna_esquerda.button("Pressione")

if pressionado:
    coluna_direita.write("Eita")

expander = st.beta_expander("o que ")
expander.write("Esta é a coluna expandida da direita")