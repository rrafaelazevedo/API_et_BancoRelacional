# pip install streamlit
# pip install streamlit_option_menu
import streamlit as st 
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao
import numpy as np
from sklearn.linear_model import LinearRegression

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
        exibir_dados = st.multiselect('Filter: ', df_selecionado.columns, default=[])

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
    graf_a, graf_b, graf_c, graf_d, graf_e = st.tabs(['Gráfico de Barras', 
                                              'Gráfico de Linhas', 
                                              'Gráfico de Setores (Pizza)', 
                                              'Gráfico de Dispersão',
                                              'Gráfico de Dispersão com Ajuste'])
    
    with graf_a:
        st.write('Gráfico de Barros') #título

        dados_a = df_selecionado.groupby('marca').count()[['valor']].sort_values(by='valor', ascending = False)
        # agrupa pela marca e conta o número de ocorrências da coluna 'valor'

        fig_valores_a = px.bar(dados_a, x=dados_a.index, y = 'valor', orientation='v', title='<b>Valores de Carros</b>', 
                              color_discrete_sequence=['#0083b3'])
        
        # exibe a figura e ajusta na tela 
        st.plotly_chart(fig_valores_a, use_container_width=True)

    with graf_b:
        st.write('Gráfico de Linhas')
        dados_b = df_selecionado.groupby('marca').count()[['valor']]
        fig_valores_b = px.line(dados_b, x=dados_b.index, y='valor', title='<b> Valor por Marca</b>', 
                               color_discrete_sequence=['#0083b3'])

        st.plotly_chart(fig_valores_b, use_container_width=True)

    with graf_c:
        st.write('Gráfico de Setores (Pizza)')
        dados_c = df_selecionado.groupby('marca').sum()[['valor']]
        fig_valores_c = px.pie(dados_c, values='valor', names=dados_c.index, title='<b>Distribuição de Valor por Marca </b>')
        st.plotly_chart(fig_valores_c, use_container_width=True)

    with graf_d:
        st.write('Gráfico de Dispersão')
        dados_d = df_selecionado.melt(id_vars=['marca'], value_vars=['valor'])
        fig_valores_d = px.scatter(dados_d, x='marca', y='value', color='variable', title='<b>Dispersão de Valor por Marca</b>')
        st.plotly_chart(fig_valores_d, use_container_width=True)

    # gráfico de dispersão experimental com ajuste de função teórica f(x)
    with graf_e:
        st.write('Gráfico de Dispersão com Ajuste de Curva')

        # filtrando as colunas necessárias: ano e valor
        dados_e = df_selecionado[['numero_vendas', 'valor']].dropna()

        # Dispersão experimental
        fig_valores_e = px.scatter(dados_e, x='numero_vendas', y='valor', title='<b>Dispersão de Valor por Vendas</b>', 
                                   labels={'numero_vendas': 'Vendas', 'valor': 'Valor do Carro'},
                                   color_discrete_sequence=['#FF5733'])

        # função teórica
        x = np.array(dados_e['numero_vendas']).reshape(-1, 1)  # ano como variável independente
        y = np.array(dados_e['valor'])  # valor como variável dependente

        # criar e ajustar o modelo de regressão linear
        modelo_regressao = LinearRegression()
        modelo_regressao.fit(x, y)

        # previsão de valores ajustados
        y_pred = modelo_regressao.predict(x)

        # adicionar a linha da função teórica (ajuste linear) ao gráfico
        fig_valores_e.add_scatter(x=dados_e['numero_vendas'], y=y_pred, mode='lines', name='Ajuste Linear', line=dict(color='blue'))

        # exibir o gráfico de dispersão com ajuste
        st.plotly_chart(fig_valores_e, use_container_width=True)

def barra_progresso():
    valor_atual = df_selecionado['numero_vendas'].sum()
    objetivo = 1000000
    percentual = round((valor_atual / objetivo * 100))    

    if percentual > 100:
        st.subheader('Valores Atingidos!!')
    else:
        st.write(f'Você tem {percentual}% de {objetivo}. Maximize as vendas!')
        mybar = st.progress(0)
        for percentual_completo in range(percentual):
            mybar.progress(percentual_completo + 1, text='Alvo %')


# menu lateral
def menu_lateral():
    with st.sidebar:
        selecionado = option_menu(menu_title='Menu',
                                 options=['Home', 'Progresso'],
                                 icons=['house', 'eye'],
                                 menu_icon='cast',
                                 default_index=0)
    if selecionado == 'Home':
        st.subheader(f'Página: {selecionado}')
        home()
        graficos(df_selecionado)

    if selecionado == 'Progresso':
        st.subheader(f'Página: {selecionado}')
        barra_progresso()
        graficos(df_selecionado)

# ajustar o CSS

menu_lateral()