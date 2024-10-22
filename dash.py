# pip install streamlit
# pip install streamlit_option_menu
import streamlit as st 
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# primeira consulta / atualização de dados database
query = 'SELECT * FROM tb_carro'

# carregar dados do database
df = conexao(query)

# botão para atualizar database
if st.button('Atualizar Dados'):
    df = conexao(query)

# estrutura lateral de filtros
st.sidebar.header('Selecione o filtro')

marca = st.sidebar.multiselect('Marca selecionada', # nome do seletor de marca
                               options = df['marca'].unique(), # opcoes de marca de maneira agrupada
                               default=df['marca'].unique())  # as marcas unicas são por padrão todas selecionadas de maneira agrupada

modelo = st.sidebar.multiselect('Modelo selecionado', # nome do seletor de modelo
                               options = df['modelo'].unique(), # opcoes de modelo de maneira agrupada
                               default=df['modelo'].unique())

valor =st.sidebar.multiselect('Valor selecionado', # nome do seletor de valores
                               options = df['valor'].unique(), # opcoes de valores de maneira agrupada
                               default=df['valor'].unique())

cor = st.sidebar.multiselect('Cor selecionada', # nome do seletor de cores
                               options = df['cor'].unique(), # opcoes de cores de maneira agrupada
                               default=df['cor'].unique())

numero_vendas = st.sidebar.multiselect('Numero de vendas', 
                               options = df['numero_vendas'].unique(), # opcoes numero_vendas de maneira agrupada
                               default=df['numero_vendas'].unique())

ano = st.sidebar.multiselect('Ano selecionado', # nome do seletor de ano
                               options = df['ano'].unique(), # opcoes ano de maneira agrupada
                               default=df['ano'].unique()) 

# aplicar os filtros selecionados 
df_selecionado = df[
    (df['marca'].isin(marca)) &
    (df['modelo'].isin(modelo)) &
    (df['valor'].isin(valor)) &
    (df['cor'].isin(cor)) &
    (df['numero_vendas'].isin(numero_vendas)) &
    (df['ano'].isin(ano)) 
]


# exibir média dos atributos numéricos do database - estatisticas elementares/fundamentais
def home():
    with st.expander('Tabela'): # cria uma caixa espansível com o título arbitrado
        exibir_dados = st.multiselect('Filter: ', df_selecionado, default=[])

        # verifica se o user selecionou colunas para exibir
        if exibir_dados:
            # exibir dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[exibir_dados])

    
    # verifica se o dataframe filtrado (df_selecionado) não está vazio
    if not df_selecionado.empty:
        venda_total = df_selecionado['numero_vendas'].sum()
        venda_media = df_selecionado['numero_vendas'].mean()
        venda_mediana = df_selecionado['numero_vendas'].median()

        # cria tres colunas (total_a_b_c) para exibir os totais calculados
        total_a, total_b, total_c = st.columns(3, gap='large')

        with total_a:
            st.info('Valor total de vendas dos carros', icon='📌')
            st.metric(label='Total', value=f'{venda_total:,.0f}')

        with total_b:
            st.info('Valor médio de vendas dos carros', icon='📌')
            st.metric(label='Média', value=f'{venda_media:,.0f}')

        with total_c:
            st.info('Valor mediano de vendas dos carros', icon='📌')
            st.metric(label='Mediana', value=f'{venda_mediana:,.0f}')

    # exibe aviso caso não haja dados disponiveis com os filtros especificados
    else:
        st.warning('Nenhum dado disponível com os filtros selecionados')
        # linha separadora de seções
    st.markdown("""---------""")

# gráficos
def graficos(df_selecionado):
    # verifica se o dataframe filtrado está vazio. se vazio, exibe mensagem de aviso (warning)
    if df_selecionado.empty:
        st.warning('Nenhum dado disponível para gerar gráficos')
        return
    
    # criacao dos gráficos
    # 4 abas -> gráficos: barras, linhas, setores (pizza) e dispersão
    graf_a, graf_b, graf_c, graf_d = st.tabs(['Gráfico de Barras',
                                              'Gráfico de Linhas',
                                              'Gráfico de Setores',
                                              'Gráfico de Dispersão'])

home()