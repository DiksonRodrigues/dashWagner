import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px

dataframe = pd.read_csv('dados-corretos.csv', index_col=0, encoding='utf8')


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

# CARDS ACIMA DA TABELA
total_aptos = round(dataframe["Aptos"].sum(),2)
total_bairro = len(dataframe["Bairro"].unique())
total_local = len(dataframe["Local"].unique())
average_ticket = round((total_aptos / total_bairro / total_local),2)

col1,col2,col3 = st.columns(3)
col1.metric("Total de Bairros", total_bairro)
col2.metric("Locais de Votação", total_local)
col3.metric("Total de Votantes", total_aptos)



st.dataframe(dataframe)