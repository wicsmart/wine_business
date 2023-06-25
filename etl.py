import requests
from io import StringIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

lista_de_arquivos_csv = [
    'Comercio.csv',
    'ExpEspumantes.csv',
    'ExpSuco.csv',
    'ExpUva.csv',
    'ExpVinho.csv',
    'ImpEspumantes.csv',
    'ImpFrescas.csv',
    'ImpPassas.csv',
    'ImpSuco.csv',
    'ImpVinhos.csv',
    'ProcessaAmericanas.csv',
    'ProcessaMesa.csv',
    'ProcessaSemclass.csv',
    'ProcessaViniferas.csv',
    'Producao.csv'
]

def read_file(file):
    
    url = f'https://raw.githubusercontent.com/guilhermeonrails/data-1-pos-tech/main/content/{file}'
    response = requests.get(url)
    csv_data = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_data), delimiter=';')
    return df

def read_all_files():
    dataframes = {}

    for arq in lista_de_arquivos_csv:
        nome_do_df = f'df_{arq[:-4].lower()}'
        url = f'https://raw.githubusercontent.com/guilhermeonrails/data-1-pos-tech/main/content/{arq}'
        response = requests.get(url)
        csv_data = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(csv_data), delimiter=';')
        dataframes[nome_do_df] = df

    return dataframes

def transform_df_expvinho(df):
    
    df = df.rename(columns={'Id': 'id','País': 'pais'})

    # Selecionar as colunas de 2007 em diante e mantendo id e pais
    colunas_a_manter = ['id', 'pais'] + list(df.loc[:, '2007':].columns)

    # Atualizar o DataFrame apenas com as colunas desejadas
    df = df.loc[:, colunas_a_manter]

    # alterando o nome
    rename_dict = {col: f"{col}_vl_litros" for col in df.columns if not col.endswith('.1')}
    df = df.rename(columns=rename_dict)

    rename_dict = {col: col.replace('.1', '_vl_dolar') for col in df.columns if '.1' in col}
    df = df.rename(columns=rename_dict)

    rename_dict = {'id_vl_litros': 'id', 'pais_vl_litros': 'pais'}
    df = df.rename(columns=rename_dict)

    # criando a coluna somando o valor total de importações de vinho de 2007 até 2021
    colunas_litros = [col for col in df.columns if col.endswith('_vl_litros')]
    df['vl_total_litros'] = df[colunas_litros].sum(axis=1)

    colunas_dolar = [col for col in df.columns if col.endswith('_vl_dolar')]
    df['vl_total_dolar'] = df[colunas_dolar].sum(axis=1)

    for ano in range(2007, 2022):
        col_litros = f"{ano}_vl_litros"
        col_dolar = f"{ano}_vl_dolar"
        df[f'{ano}_preco_do_litro'] = np.divide(df[col_dolar], df[col_litros]).fillna(0)
        df[f'{ano}_preco_do_litro'] = df[f'{ano}_preco_do_litro'].apply(lambda x: round(x, 2))

    ordered_columns = ['id', 'pais', 'vl_total_litros', 'vl_total_dolar']
    for ano in range(2007, 2022):
        ordered_columns.append(f'{ano}_vl_litros')
        ordered_columns.append(f'{ano}_vl_dolar')
        ordered_columns.append(f'{ano}_preco_do_litro')
    
    df = df.reindex(columns=ordered_columns)

    return df

def top_por_litro(df, number):

    colunas_pais_litros = [col for col in df.columns if not col.endswith(('_vl_dolar','preco_do_litro'))]
    df_litros = df[colunas_pais_litros]

    rename_dict = {col: col.replace('_vl_litros', '') for col in df_litros.columns}

    df_litros = df_litros.rename(columns=rename_dict)

    df_litros = df_litros.sort_values('vl_total_litros', ascending=False)
    df_litros = df_litros.set_index('pais')
    df_litros = df_litros.drop(['id',], axis=1)

    df_litros_5 = df_litros.head(number)
    df_litros_5 = df_litros_5.drop(['vl_total_dolar','vl_total_litros'], axis=1)

    return df_litros_5


def top_por_dolar(df, number):
    colunas_pais_dolar = [col for col in df.columns if not col.endswith(('_vl_litros','preco_do_litro'))]
    df_dolar = df[colunas_pais_dolar]

    rename_dict = {col: col.replace('_vl_dolar', '') for col in df_dolar.columns}

    df_dolar = df_dolar.rename(columns=rename_dict)

    df_dolar = df_dolar.sort_values('vl_total_dolar', ascending=False)
    df_dolar = df_dolar.set_index('pais')
    df_dolar = df_dolar.drop(['id',], axis=1)

    # filtra os dez maiores importadores
    df_dolar_5 = df_dolar.head(number)
    df_dolar_5 = df_dolar_5.drop(['vl_total_dolar','vl_total_litros'], axis=1)

    return df_dolar_5

def top_por_preco(df, number):

    colunas_pais_dolar = [col for col in df.columns if not col.endswith(('_vl_litros','_vl_dolar'))]
    df_preco = df[colunas_pais_dolar]

    rename_dict = {col: col.replace('_preco_do_litro', '') for col in df_preco.columns}

    df_preco = df_preco.rename(columns=rename_dict)

    df_preco = df_preco.sort_values('vl_total_dolar', ascending=False)
    df_preco = df_preco.set_index('pais')
    df_preco = df_preco.drop(['id',], axis=1)

    # filtra os dez maiores importadores
    df_preco_5 = df_preco.head(number)
    df_preco_5 = df_preco_5.drop(['vl_total_dolar','vl_total_litros'], axis=1)

    return df_preco_5
   