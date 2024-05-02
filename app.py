import pandas as pd
import streamlit as st

# Leitura dos dados
dataframe_corretos = pd.read_csv('dados-corretos.csv', encoding='utf8')

# Configurações da página
st.set_page_config(
    page_title="Wagner da Acerola",
    layout="wide",
    page_icon="cherries",
    initial_sidebar_state="collapsed"
)

st.markdown("#")
# DETALHES DA PÁGINA INICIAL
st.header(":cherries: Eleições 2024 Wagner da Acerola :cherries:")
st.markdown("#")

# Cálculo dos totais
total_aptos = round(dataframe_corretos["Aptos"].sum(), 2)
total_bairro = len(dataframe_corretos["Bairro"].unique())
total_local = len(dataframe_corretos["Local"].unique())
average_ticket = round((total_aptos / total_bairro / total_local), 2)

# Selecione os bairros
st.markdown("## Selecione os Bairros:")
bairros_selecionados = st.multiselect(
    label="",
    options=dataframe_corretos["Bairro"].unique(),
    default=dataframe_corretos["Bairro"].unique()
)

# Aplicando o filtro de bairro após a seleção do usuário
dataframe_corretos_filtrado = dataframe_corretos.query("Bairro == @bairros_selecionados")

# Recálculo dos totais após aplicação do filtro de bairro
total_aptos_filtrado = round(dataframe_corretos_filtrado["Aptos"].sum(), 2)
total_bairro_filtrado = len(dataframe_corretos_filtrado["Bairro"].unique())
total_local_filtrado = len(dataframe_corretos_filtrado["Local"].unique())

st.markdown("#")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Bairros", total_bairro_filtrado)
col2.metric("Locais de Votação", total_local_filtrado)
col3.metric("Total de Votantes", total_aptos_filtrado)
st.markdown("""---""")

# Exibição dos dados filtrados
st.dataframe(dataframe_corretos_filtrado)
st.markdown("#")

# Cálculo da porcentagem do eleitorado representado pelos 1500 votos necessários
votos_necessarios = 2000
porcentagem_eleitorado = (votos_necessarios / total_aptos_filtrado) * 100

# Verifica se a porcentagem calculada é menor que 0.01% do eleitorado
# Se sim, ajusta a porcentagem para garantir que o número de votos seja no mínimo 1500
if porcentagem_eleitorado < 0.01:
    porcentagem_eleitorado = 0.01
    votos_necessarios = int((porcentagem_eleitorado / 100) * total_aptos_filtrado)

st.write(f"Para alcançar os {votos_necessarios} votos necessários, você precisa conquistar aproximadamente {porcentagem_eleitorado:.2f}% do eleitorado.")
