import pandas as pd
import plotly.express as px


def lerdados1():
    dados = pd.read_csv('dados.csv')
    return dados
def lerdados():
    dados = pd.read_csv('dados.csv')
    dados_numericos = dados.select_dtypes(include='number')
    return dados_numericos

def lerdados2():
    dados = pd.read_csv('dados2.csv')
    return dados