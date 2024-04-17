import pandas as pd
import plotly.express as px

def lerdados():
    dados = pd.read_csv('dados.csv')
    dados_numericos = dados.select_dtypes(include='number')
    return dados_numericos

def lerdados1():
    dados = pd.read_csv('dados.csv')
    dados['Porcentagem'] = (dados['PIB'] / dados['PIB'].sum()) * 100
    return dados

def lerdados2():
    dados = pd.read_csv('dados2.csv')
    return dados