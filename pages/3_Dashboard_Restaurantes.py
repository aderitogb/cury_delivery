# Bibliotecas
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
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
st.set_page_config(page_title='Visão Restaurantes', page_icon='🍔', layout="wide",
                   initial_sidebar_state="auto", menu_items=None)
st.markdown('# Cury Company - **Visão Restaurantes**')

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
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap='large')
    with col1:
        entregadores = len(df2['Delivery_person_ID'].unique())
        col1.metric(label='Qtd entregadores', value=entregadores)

    with col2:
        distancia_media = np.round(df2['distancia'].mean(), 2)
        col2.metric(label='Distância média', value=distancia_media)

    with col3:
        df_aux = df2.loc[:, ['Festival', 'Time_taken(min)']].groupby(
            'Festival').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['tempo_medio', 'tempo_std']
        df_aux = df_aux.reset_index()
        festival = df_aux.loc[df_aux['Festival'] == 'Yes', :]
        col3.metric(label='Tempo médio Festival',
                    value=np.round(festival['tempo_medio'], 2))

    with col4:
        col4.metric(label='Desvio padrão Festival',
                    value=np.round(festival['tempo_std'], 2))

    with col5:
        nao_festival = df_aux.loc[df_aux['Festival'] == 'No', :]
        col5.metric(label='Tempo médio Não Festival',
                    value=np.round(nao_festival['tempo_medio'], 2))
    with col6:
        col6.metric(label='Desvio padrão Não Festival',
                    value=np.round(nao_festival['tempo_std'], 2))

st.markdown('---')

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('##### Tempo médio das entregas por cidade')
        df_aux = df2.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg(
            {'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['tempo_medio', 'tempo_std']
        df_aux = df_aux.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Cidade', x=df_aux['City'], y=df_aux['tempo_medio'], error_y=dict(
            type='data', array=df_aux['tempo_std'])))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('##### Tempo médio por cidade e densidade de tráfego')
        df_aux = df2.loc[:, ['City', 'Road_traffic_density', 'Time_taken(min)']].groupby(
            ['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['tempo_medio', 'tempo_std']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux, hide_index=True, column_config={
                     'City': 'Cidade', 'Road_traffic_density': 'Densidade de tráfego', 'tempo_medio': st.column_config.NumberColumn(
                         'Tempo médio',
                         format="%.2f 🕜"), 'tempo_std': 'Desvio padrão'},
                     use_container_width=True
                     )


st.markdown('---')

with st.container():
    col1, col2, = st.columns(2, gap='large')
    with col1:
        st.markdown('##### Distância média por cidade')
        distancia_media = df2.loc[:, ['City', 'distancia']].groupby(
            'City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=distancia_media['City'],
                                     values=distancia_media['distancia'], pull=[0, 0, 0.05])])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('##### Tempo médio por cidade e tráfego')
        df_aux = df2.loc[:, ['City', 'Road_traffic_density', 'Time_taken(min)']].groupby(
            ['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['tempo_medio', 'tempo_std']
        df_aux = df_aux.reset_index()
        fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='tempo_medio',
                          color='tempo_std', color_continuous_scale='bluered',
                          color_continuous_midpoint=np.average(
                              df_aux['tempo_std']),
                          labels={'City': 'Cidade', 'Road_traffic_density': 'Densidade de tráfego',
                                  'tempo_medio': 'Tempo médio', 'tempo_std': 'Desvio padrão'}
                          )
        st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown('##### Tempo médio de entrega por tipo de pedido')
        df_aux = df2.loc[:, ['Type_of_order', 'Time_taken(min)']].groupby(
            ['Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['tempo_medio', 'tempo_std']
        df_aux = df_aux.reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Tipo de pedido', x=df_aux['Type_of_order'], y=df_aux['tempo_medio'], error_y=dict(
            type='data', array=df_aux['tempo_std'])))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('##### Distribuição dos tipos de pedido')
        df_aux = df2.loc[:, ['Type_of_order', 'ID']].groupby(
            'Type_of_order').count().reset_index()
        df_aux['pct_type_order'] = df_aux['ID']/df_aux['ID'].sum()
        fig = go.Figure(data=[go.Pie(labels=df_aux['Type_of_order'],
                        values=df_aux['pct_type_order'], pull=[0.01, 0.01, 0.01, 0.01])])
        st.plotly_chart(fig, use_container_width=True)
