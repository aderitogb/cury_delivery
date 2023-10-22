# Bibliotecas
import pandas as pd
import datetime
import plotly.express as px
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

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
st.set_page_config(page_title='Visão Empresa', page_icon='📈', layout="wide",
                   initial_sidebar_state="auto", menu_items=None)
st.markdown('# Cury Company - **Visão Empresa**')

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
tab1, tab2, tab3 = st.tabs(
    ['Visão Gerencial', 'Visão Estratégica', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('##### Pedidos por dia')
        df_aux = df2[['Order_Date', 'ID']].groupby(
            ['Order_Date']).count().reset_index()
        df_aux.columns = ['Order_Date', 'qtd_entregas']
        fig = px.bar(df_aux, x='Order_Date', y='qtd_entregas', labels={'Order_Date': 'Data do pedido',
                                                                       'qtd_entregas': 'Qtd entregas'
                                                                       })
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown('##### Pedidos por densidade de tráfego')
            df_aux = df2[['Road_traffic_density', 'ID']].groupby(
                ['Road_traffic_density']).count().reset_index()
            df_aux.columns = ['Road_traffic_density', 'qtd_entregas']
            df_aux['perc_ID'] = 100 * \
                (df_aux['qtd_entregas']/df_aux['qtd_entregas'].sum())
            fig = px.pie(df_aux, values='perc_ID', names='Road_traffic_density', labels={'Road_traffic_density': 'Densidade de tráfego',
                                                                                         'perc_ID': '% entregas'
                                                                                         })
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown('##### Pedidos por densidade de tráfego e cidade')
            df_aux = df2[['Road_traffic_density', 'City', 'ID']].groupby(
                ['City', 'Road_traffic_density']).count().reset_index()
            df_aux.columns = ['Road_traffic_density', 'City', 'qtd_entregas']
            df_aux['perc_ID'] = 100 * \
                (df_aux['qtd_entregas']/df_aux['qtd_entregas'].sum())

            fig = px.bar(df_aux, x='City', y='qtd_entregas', color='Road_traffic_density', barmode='group', labels={'Road_traffic_density': 'Densidade de tráfego',
                                                                                                                    'City': 'Cidade',
                                                                                                                    'qtd_entregas': 'Qtd entregas'})
            st.plotly_chart(fig, use_container_width=True)


with tab2:
    with st.container():
        st.markdown('##### Pedidos por semana')
        df_aux = df2[['week_of_year', 'ID']].groupby(
            ['week_of_year']).count().reset_index()
        df_aux.columns = ['week_of_year', 'qtd_entregas']
        fig = px.line(df_aux, x='week_of_year', y='qtd_entregas', labels={'week_of_year': 'Semana do ano',
                                                                          'qtd_entregas': 'Qtd entregas'
                                                                          })
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('##### Pedidos por entregador por semana')
        df_aux1 = df2.loc[:, ['ID', 'week_of_year']].groupby(
            'week_of_year').count().reset_index()
        df_aux2 = df2.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(
            'week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner')
        df_aux['order_by_delivery'] = df_aux['ID'] / \
            df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x='week_of_year', y='order_by_delivery', labels={'week_of_year': 'Semana do ano',
                                                                               'order_by_delivery': 'Pedidos por entregador'})
        st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.markdown('##### Mapa geográfico das entregas')
    columns = [
        'City',
        'Road_traffic_density',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
    ]

    columns_grouped = ['City', 'Road_traffic_density']
    data_plot = df2.loc[:, columns].groupby(
        columns_grouped).median().reset_index()
    data_plot.columns = [
        'Cidade', 'Densidade de tráfego', 'latitude', 'longitude']

    # Desenhar o mapa
    map_ = folium.Map(zoom_start=11, tiles='Stamen Terrain')
    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['latitude'],
                       location_info['longitude']],
                      popup=location_info[['Cidade', 'Densidade de tráfego']],
                      icon=folium.Icon(color='red', icon='info-sign')).add_to(map_)
    folium_static(map_, width=1024, height=500)
