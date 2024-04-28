import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px

dataframe = pd.read_csv('dados-eleitorais-sem-colunas.csv', index_col=0, encoding='latin1')


#Configurações da pagina.
st.set_page_config(
    page_title="Wagner da acerola",
    layout= "wide",
    initial_sidebar_state="collapsed"
)

#FILTROS DO MENU LATERAL
bairro = st.sidebar.multiselect(
    key= 1,
    label= "Bairro",
    options=dataframe["Bairro"].unique(),
    default=dataframe["Bairro"].unique()
)

# FAZENDO FUNCIONAR OS FILTROS
dataframe = dataframe.query("Bairro == @bairro")



# DETALHES DA PAGINA INICIAL
st.header("Eleições 2024 Wagner da Acerola")
st.markdown("""---""")

st.dataframe(dataframe)