import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Leitura dos dados
dataframe_corretos = pd.read_csv('dados-corretos1.csv', encoding='utf8')

# Configurações da página
st.set_page_config(
    page_title="Wagner da Acerola",
    layout="wide",
    page_icon="cherries",
    initial_sidebar_state="collapsed"
)

# Cabeçalho na página principal

st.header(":cherries: Eleições 2024 Wagner da Acerola :cherries:")


# Cabeçalho no menu lateral
st.sidebar.markdown("#")
st.sidebar.header(":cherries: Eleições 2024 Wagner da Acerola :cherries:")


# Cálculo dos totais
total_aptos = round(dataframe_corretos["Aptos"].sum(), 2)
total_bairro = len(dataframe_corretos["Bairro"].unique())
total_local = len(dataframe_corretos["Local"].unique())
average_ticket = round((total_aptos / total_bairro / total_local), 2)

# Selecione os bairros
st.sidebar.markdown("## Selecione os Bairros:")
bairros_selecionados = st.sidebar.multiselect(
    label="",
    options=dataframe_corretos["Bairro"].unique(),
    default=dataframe_corretos["Bairro"].unique()
)

# Aplicando o filtro de bairro após a seleção do usuário
dataframe_corretos_filtrado = dataframe_corretos.query("Bairro == @bairros_selecionados")

# Substituir valores NaN por 0
dataframe_corretos_filtrado = dataframe_corretos_filtrado.fillna(0)

# Recálculo dos totais após aplicação do filtro de bairro
total_aptos_filtrado = round(dataframe_corretos_filtrado["Aptos"].sum(), 2)
total_bairro_filtrado = len(dataframe_corretos_filtrado["Bairro"].unique())
total_local_filtrado = len(dataframe_corretos_filtrado["Local"].unique())


col1, col2, col3 = st.columns(3)
col1.metric("Total de Bairros", total_bairro_filtrado)
col2.metric("Locais de Votação", total_local_filtrado)
col3.metric("Total de Votantes", total_aptos_filtrado)
#st.markdown("""---""")

# Cálculo da porcentagem do eleitorado representado pelos 1500 votos necessários
votos_necessarios = st.number_input("Digite a quantidade de votos que quer alcançar:", min_value=0, step=1, value=2000)
porcentagem_eleitorado = (votos_necessarios / total_aptos_filtrado) * 100

# Verifica se a porcentagem calculada é menor que 0.01% do eleitorado
# Se sim, ajusta a porcentagem para garantir que o número de votos seja no mínimo 1500
if porcentagem_eleitorado < 0.01:
    porcentagem_eleitorado = 0.01
    votos_necessarios = int((porcentagem_eleitorado / 100) * total_aptos_filtrado)

st.write(f"Para alcançar os {votos_necessarios} votos necessários, você precisa conquistar aproximadamente {porcentagem_eleitorado:.2f}% do eleitorado.")
st.markdown('#')

################################################################
col1, col2 = st.columns([ 2, 1])

# Exibição do arquivo CSV dados-apoia-sarg.csv
st.markdown("## Dados Apoiadores e Sargentos:")
data_apoia_sarg = pd.read_csv('dados-apoia-sarg.csv').fillna(0)
data_apoia_sarg['Quantidade de Votos do Apoiador'] = data_apoia_sarg['Quantidade de Votos do Apoiador'].fillna(0).astype(int)
data_apoia_sarg['Quantidade de Votos do Sargento'] = data_apoia_sarg['Quantidade de Votos do Sargento'].fillna(0).astype(int)

# Substituindo 'NA' por vazio
data_apoia_sarg.replace('NA', '', inplace=True)

total_votos_apoiadores = st.number_input("Digite a quantidade total de votos dos apoiadores:", min_value=0, step=1, value=data_apoia_sarg['Quantidade de Votos do Apoiador'].sum())
total_votos_sargentos = st.number_input("Digite a quantidade total de votos dos sargentos:", min_value=0, step=1, value=data_apoia_sarg['Quantidade de Votos do Sargento'].sum())


st.write(f"Total de Votos dos Apoiadores: {total_votos_apoiadores}")
st.write(f"Total de Votos dos Sargentos: {total_votos_sargentos}")

############ GRAFICO DE BARRA ################
with col1:
    total_votos = total_votos_apoiadores + total_votos_sargentos
    tamanho_barra = votos_necessarios / total_votos  # Tamanho relativo da barra

    # Criar o gráfico de barras
    plt.figure(figsize=(5, 3), facecolor='#FFFFFF')  # Tamanho da figura
    bar_width = 0.4  # Largura das barras
    plt.bar(-bar_width/2, total_votos_sargentos, color='#EBBF04', width=bar_width, label='Sargentos')  # Barra dos sargentos
    plt.bar(bar_width/2, total_votos_apoiadores, color='#209A0D', width=bar_width, label='Apoiadores')  # Barra dos apoiadores
    plt.bar(1.5 * bar_width, votos_necessarios, color='#FF5733', width=bar_width, label='Desejado')  # Barra desejada
    plt.ylim(0, total_votos * 1.2)  # Ajustar os limites do eixo y
    plt.xticks([])  # Remover os ticks do eixo x
    plt.title(f'Total de Votos: {total_votos}', color='white')  # Título do gráfico
    

    # Configurar cor do texto nos eixos
    plt.gca().yaxis.label.set_color('white')
    plt.gca().title.set_color('white')

    # Exibir o gráfico
    st.pyplot(plt)
############ GRAFICO DE BARRA ################


############ GRAFICO DE PIZZA ################
with col2:
    labels = ['Apoiadores', 'Sargentos']
    sizes = [
        total_votos_apoiadores,
        total_votos_sargentos
    ]
    colors = ['#209A0D', '#EBBF04']  # Cores correspondentes aos segmentos

    # Criar o gráfico de pizza
    plt.figure(facecolor='#037D0A', frameon=False, figsize=(5, 3))  # Definindo o tamanho da figura
    pie = plt.pie(sizes + [votos_necessarios], labels=labels + ['Desejado'], colors=colors + ['#FF5733'], autopct='%1.1f%%', textprops={'color': 'white'})  # Definindo a cor do texto das porcentagens
    plt.axis('equal')  # Aspecto do círculo para garantir que seja um círculo
    plt.axis('off')  # Remover os eixos
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), labels=labels + ['Desejado'], title_fontsize="large", prop={'size': 12})  # Adicionar legenda e definir a posição abaixo do gráfico e cor do texto

    # Exibir o gráfico
    st.pyplot(plt)
############ GRAFICO DE PIZZA ################

st.markdown("#")
st.title("Dados das comunidade e locais de votação")
st.dataframe(dataframe_corretos_filtrado)

