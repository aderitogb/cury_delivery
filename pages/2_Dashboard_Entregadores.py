# Bibliotecas
import pandas as pd
import datetime
import plotly.express as px
from haversine import haversine
import streamlit as st
from PIL import Image

# =============================================================
# Funções
# =============================================================


def carrega_dataframe():
    """ Função para carregar o dataframe para a memória

    Returns:
        dataframe: retorna dataframe com a base carregada
    """
    path = 'dados/'
    df = pd.read_csv(path + 'train.csv')
    df1 = df.copy()
    return df1


def tratamento_dataframe(df1):
    """Função para fazer o tratamento e limpeza da base de dados
    1. Retira espaços em branco das variáveis de texto
    2. Retira dados faltantes
    3. Ajusta formato das variáveis
    4. Retira texto da variável de tempo (numérica)
    5. Cria variável de semana do ano
    6. Cria variável de distância da entrega

    Args:
        df1 (dataframe): leitura do dataframe carregado na memória

    Returns:
        dataframe: retorna dataframe com todas as limpezas e tratamentos
    """

    # Retirando espaços em branco das variáveis categóricas
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:,
                                               'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,
                                                 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    # Retirando dados faltantes
    df1 = df1[(df1['Delivery_person_Age'] != 'NaN ')
              & (df1['multiple_deliveries'] != 'NaN ')
              & (df1['Road_traffic_density'] != 'NaN')
              & (df1['City'] != 'NaN')
              & (df1['Weatherconditions'] != 'conditions NaN')
              & (df1['Festival'] != 'NaN')
              ].reset_index(drop=True)

    # Ajustando o formato das variáveis
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype('int64')
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(
        float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype('int64')

    # Retirando texto (min) da coluna de tempo de entrega
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(
        lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype('int64')

    # Criando variável do dia da semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1['week_of_year'] = df1['week_of_year'].astype('int64')

    # Criando variavel de distancia
    df1['distancia'] = df1.apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                     (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    df1 = df1.reset_index()
    df2 = df1.copy()
    return df2


df1 = carrega_dataframe()
df2 = tratamento_dataframe(df1)


# =======================================================
#  STREAMLIT
# =======================================================

# =======================================================
#  CONFIGURA PÁGINA
# =======================================================
st.set_page_config(page_title='Visão Entregadores', page_icon='🛵', layout="wide",
                   initial_sidebar_state="auto", menu_items=None)
st.markdown('# Cury Company - **Visão Entregadores**')
# =======================================================
#  BARRA LATERAL
# =======================================================
path = ''
image = Image.open(path + 'img.jpg')
st.sidebar.image(image, width=300)
st.sidebar.markdown('# **Cury Company Delivery**🍕')

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione uma data limite')
date_slider = st.sidebar.slider('',
                                # value=datetime.datetime(2022, 4, 13),
                                value=datetime.datetime(df2['Order_Date'].max(
                                ).year, df2['Order_Date'].max().month, df2['Order_Date'].max().day),
                                min_value=datetime.datetime(df2['Order_Date'].min(
                                ).year, df2['Order_Date'].min().month, df2['Order_Date'].min().day),
                                max_value=datetime.datetime(df2['Order_Date'].max(
                                ).year, df2['Order_Date'].max().month, df2['Order_Date'].max().day),
                                format='DD-MM-YYYY')

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione as condições de trânsito')
traffic_options = st.sidebar.multiselect('',
                                         df2['Road_traffic_density'].unique(),
                                         default=df2['Road_traffic_density'].unique())

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione o tipo de veículo')
vehicle_options = st.sidebar.multiselect('',
                                         df2['Type_of_vehicle'].unique(),
                                         default=df2['Type_of_vehicle'].unique())

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione o tipo de pedido')
order_options = st.sidebar.multiselect('',
                                       df2['Type_of_order'].unique(),
                                       default=df2['Type_of_order'].unique())

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione o tipo de cidade')
city_options = st.sidebar.multiselect('',
                                      df2['City'].unique(),
                                      default=df2['City'].unique())

st.sidebar.markdown('---')
st.sidebar.markdown('### Selecione as condições climáticas')
weather_options = st.sidebar.multiselect('',
                                         df2['Weatherconditions'].unique(),
                                         default=df2['Weatherconditions'].unique())


st.sidebar.markdown('---')
st.sidebar.markdown('')
st.sidebar.markdown('##### Criado por **Adérito Bernardes**')
st.sidebar.markdown('---')


# =======================================================
#  APLICANDO FILTROS
# =======================================================

df2 = df2.loc[df2['Order_Date'] <= date_slider, :]
df2 = df2.loc[df2['Road_traffic_density'].isin(traffic_options), :]
df2 = df2.loc[df2['Type_of_vehicle'].isin(vehicle_options), :]
df2 = df2.loc[df2['Type_of_order'].isin(order_options), :]
df2 = df2.loc[df2['City'].isin(city_options), :]
df2 = df2.loc[df2['Weatherconditions'].isin(weather_options), :]


# =======================================================
#  LAYOUT STREAMLIT
# =======================================================
with st.container():
    st.markdown('## Métricas gerais')
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        maior_idade = df2['Delivery_person_Age'].max()
        col1.metric(label='Maior idade', value=maior_idade)
    with col2:
        menor_idade = df2['Delivery_person_Age'].min()
        col2.metric(label='Menor idade', value=menor_idade)
    with col3:
        melhor_veiculo = df2['Vehicle_condition'].max()
        col3.metric(label='Melhor condição de veículo', value=melhor_veiculo)
    with col4:
        pior_veiculo = df2['Vehicle_condition'].min()
        col4.metric(label='Pior condição de veículo', value=pior_veiculo)

st.markdown('---')

with st.container():
    st.markdown('## Avaliações')
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('##### Avaliação média por entregador')
        cols = ['Delivery_person_ID', 'Delivery_person_Ratings']
        df_aux = df2.loc[:, cols].groupby(
            'Delivery_person_ID').mean().reset_index()
        df_aux.columns = ['Delivery_person_ID', 'Avaliacao media']
        st.dataframe(df_aux.sort_values(
            'Avaliacao media', ascending=False), hide_index=True, use_container_width=True, column_config={'Delivery_person_ID': 'ID Entregador', 'Avaliacao media': st.column_config.NumberColumn(
                'Avaliação média',
                help='Avaliação média',
                format="%.2f ⭐")}, height=490)
    with col2:
        st.markdown('##### Avaliação média por trânsito')
        cols = ['Road_traffic_density', 'Delivery_person_Ratings']
        df_aux = df2.loc[:, cols].groupby('Road_traffic_density').agg(
            {'Delivery_person_Ratings': ['mean', 'std']})
        df_aux.columns = ['Avaliacao media', 'Avaliacao std']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux.sort_values('Avaliacao media',
                     ascending=False), hide_index=True, use_container_width=True, column_config={'Road_traffic_density': 'Densidade de tráfego', 'Avaliacao media': st.column_config.NumberColumn(
                         'Avaliação média',
                         format="%.2f ⭐"), 'Avaliacao std': 'Desvio padrão'})

        st.markdown('##### Avaliação média por clima')
        cols = ['Weatherconditions', 'Delivery_person_Ratings']
        df_aux = df2.loc[:, cols].groupby('Weatherconditions').agg(
            {'Delivery_person_Ratings': ['mean', 'std']})
        df_aux.columns = ['Avaliacao media', 'Avaliacao std']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux.sort_values('Avaliacao media',
                     ascending=False), hide_index=True, use_container_width=True, column_config={'Weatherconditions': 'Condições climáticas', 'Avaliacao media': st.column_config.NumberColumn(
                         'Avaliação média',
                         format="%.2f ⭐"), 'Avaliacao std': 'Desvio padrão'})

st.markdown('---')

with st.container():
    st.markdown('## Tempo de entrega')
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('##### Entregadores mais rápidos')
        cols = ['City', 'Delivery_person_ID', 'Time_taken(min)']
        df_aux = df2.loc[:, cols].groupby(['City', 'Delivery_person_ID']).agg({
            'Time_taken(min)': ['mean']})
        df_aux.columns = ['tempo_medio']
        df_aux = df_aux.reset_index().sort_values(
            ['City', 'tempo_medio'], ascending=True)

        df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
        df_aux03 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)

        df_aux = pd.concat([df_aux01, df_aux02, df_aux03]
                           ).reset_index(drop=True)
        st.dataframe(df_aux, hide_index=True, use_container_width=True, column_config={
                     'City': 'Cidade', 'Delivery_person_ID': 'ID Entregador', 'tempo_medio': st.column_config.NumberColumn(
                         'Tempo médio',
                         format="%.2f 🕜")})

    with col2:
        st.markdown('##### Entregadores mais lentos')
        cols = ['City', 'Delivery_person_ID', 'Time_taken(min)']
        df_aux = df2.loc[:, cols].groupby(['City', 'Delivery_person_ID']).agg({
            'Time_taken(min)': ['mean']})
        df_aux.columns = ['tempo_medio']
        df_aux = df_aux.reset_index().sort_values(
            ['City', 'tempo_medio'], ascending=False)

        df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
        df_aux03 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)

        df_aux = pd.concat([df_aux01, df_aux02, df_aux03]
                           ).reset_index(drop=True)
        st.dataframe(df_aux, hide_index=True, use_container_width=True, column_config={
                     'City': 'Cidade', 'Delivery_person_ID': 'ID Entregador', 'tempo_medio': st.column_config.NumberColumn(
                         'Tempo médio',
                         format="%.2f 🕜")})
