import requests
from io import StringIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

import etl

import streamlit as st
st.set_page_config(layout="wide")

df_ex_vinho = etl.read_file('ExpVinho.csv')
df = etl.transform_df_expvinho(df_ex_vinho)
#Titulo de Página
st.title('Análise de Países Importadores de Vinho')

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(["Relevantes","Histórico Top 5",])

# Separando as Tabs
with tab0:
    '''
    ## Análise de Países Importadores de Vinho

    Fontes:
    http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01
   
    '''
    #DataFrame
    
    df_valor_importado_por_pais = df.sort_values('vl_total_dolar', ascending=False)
    df_valor_importado_por_pais = df_valor_importado_por_pais.loc[:, ['pais', 'vl_total_dolar']]
  
    # st.dataframe(df_valor_importado_por_pais, use_container_width=True)
    data = df_valor_importado_por_pais[:5]

    # Gerar o gráfico de barras
    # fig, ax = plt.subplots()

    fig = go.Figure(data=go.Bar(x=data['pais'],y=data['vl_total_dolar']))
    fig.update_layout(
        title= 'Maiores importadores em U$ (15 anos)',
        yaxis=dict(title='Valor em Dólar U$ importado'),
        width=600,  # Largura da figura em pixels
        height=600  # Altura da figura em pixels
    ) 
   
    st.plotly_chart(fig,  use_container_width = False)

    df_valor_importado_por_pais = df.sort_values('vl_total_litros', ascending=False)
    df_valor_importado_por_pais = df_valor_importado_por_pais.loc[:, ['pais', 'vl_total_litros']]
    data1 = df_valor_importado_por_pais[:5]

    fig1 = go.Figure(data=go.Bar(x=data1['pais'],y=data1['vl_total_litros']))
    fig.update_layout(
        title= 'Maiores importadores em litros (15 anos)',
        yaxis=dict(title='Litros'),
        width=600,  # Largura da figura em pixels
        height=600  # Altura da figura em pixels
    ) 

    st.plotly_chart(fig1, use_container_width = False)

with tab1:
    
    df_dolar_5 = etl.top_por_dolar(df, 5)

    lines = []
    for country in df_dolar_5.index:
        line = go.Scatter(x=df_dolar_5.columns, y=df_dolar_5.loc[country], mode='lines', name=country)
        lines.append(line)

    # Criar o layout do gráfico
    layout = go.Layout(title='5 Países que mais importam vinhos do Brasil',
                      yaxis=dict(title='Dólares'))

    # Criar a figura com os dados e layout
    fig = go.Figure(data=lines, layout=layout)
    st.plotly_chart(fig,  use_container_width = True)


    df_litros_5 = etl.top_por_litro(df, 5)
    lines1 = []
    for country in df_litros_5.index:
        line1 = go.Scatter(x=df_litros_5.columns, y=df_litros_5.loc[country], mode='lines', name=country)
        lines1.append(line1)

    # Criar o layout do gráfico
    layout1 = go.Layout(title='Valores de litros',
                      xaxis=dict(title='Ano'),
                      yaxis=dict(title='Litros'))

    # Criar a figura com os dados e layout
    fig1 = go.Figure(data=lines1, layout=layout1)
    st.plotly_chart(fig1,  use_container_width = True)

    df_preco = etl.top_por_preco(df, 5)
    lines2 = []
    for country in df_preco.index:
        line2 = go.Scatter(x=df_preco.columns, y=df_preco.loc[country], mode='lines', name=country)
        lines2.append(line2)

    # Criar o layout do gráfico
    layout2 = go.Layout(title='Preço médio do litro do vinho USD/L',
                    xaxis=dict(title='Ano'),
                    yaxis=dict(title='Dólar/Litro'))

    # Criar a figura com os dados e layout
    fig2 = go.Figure(data=lines2, layout=layout2)
    st.plotly_chart(fig2,  use_container_width = True)

      
   
