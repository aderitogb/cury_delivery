import streamlit as st
from PIL import Image

st.set_page_config(page_title='Cury Company Delivery',
                   page_icon='🍕',
                   #    layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

path = ''
image = Image.open(path + 'img.jpg')

st.sidebar.image(image, width=300)

st.sidebar.markdown('# **Cury Company Delivery**🍕')
st.sidebar.markdown('---')
st.sidebar.markdown('')
st.sidebar.markdown('##### Criado por **Adérito Bernardes**')
st.sidebar.markdown('---')

st.write('# Cury Company Delivery - Dasboard')

st.markdown("""
            Este dashboard foi construído para acompanhar as métricas de crescimento das entregas e das vendas dos restaurantes da **Cury Company Delivery**.
            ### Como utilizar o dasboard?
            - Visão Empresa:
                - Visão Gerencial: métricas gerais de comportamento;
                - Visão Estratégica: indicadores semanais de crescimento;
                - Visão Geográfica: localização geográfica das entregas.
            - Visão Entregador:
                - Acompanhamento das principais métricas dos entregadores.
            - Visão Restaurantes:
                - Principais indicadores relacionados aos restaurantes.
            """)
