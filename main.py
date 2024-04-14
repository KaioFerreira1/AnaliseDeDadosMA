import pandas as pd
from flask import Flask, render_template, request, redirect, session
import dao
import plotly.express as px
import dataanalise as da

app = Flask(__name__)

app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conexao = dao.conectardb()
        if dao.verificarlogin(nome, senha, conexao):
            session['nome'] = nome
            return redirect('/menu')
        else:
            return render_template('login.html', error="Credenciais inválidas. Tente novamente.")
    return render_template('login.html')


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        login = request.form['nome']
        senha = request.form['senha']
        conexao = dao.conectardb()
        if dao.inseriruser(login, senha, conexao):
            return redirect('/login')
        else:
            return render_template('cadastro.html', error="Erro ao cadastrar usuário. Tente novamente.")
    return render_template('cadastro.html')


@app.route('/pibpormunicipios', methods=['GET', 'POST'])
def pibpormunicipios():
    if request.method == 'POST':
        dados = da.lerdados1()
        dados_ordenados = dados.sort_values(by='PIB', ascending=False)
        num_municipios = int(request.form['num_municipios'])
        melhores_municipios = dados_ordenados.head(num_municipios)
        fig = px.bar(melhores_municipios, x='Municipios', y='PIB',
                     color='Municipios',
                     title='Grafíco de PIB por Municípios')
        return render_template('pibpormunicipios.html', grafico1=fig.to_html())
    else:
        return render_template('pibpormunicipios.html')


@app.route('/grafmatriculaspb', methods=['GET', 'POST'])
def grafmatriculaspb():
    if request.method == 'POST':
        dados = da.lerdados2()
        dados['Total Matrículas'] = dados.sum(axis=1)
        fig = px.line(dados, x='Ano', y=['Pré-escolar', 'Ensino Fundamental', 'Ensino Médio'],
                      title="Matrículas por Ano e Nível de Ensino",
                      labels={'value': 'Total de Matrículas', 'Ano': 'Ano'},
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      markers=True)
        return render_template('matriculasescolasPB.html', grafico2=fig.to_html())
    else:
        return render_template('matriculasescolasPB.html')


@app.route('/grafcorrindicadores', methods=['GET', 'POST'])
def correlacao_indicadores():
    if request.method == 'POST':
        # Carregar os dados
        dados = da.lerdados()

        # Calculando a matriz de correlação
        matriz_correlacao = dados.corr()

        # Criando o gráfico de matriz de correlação usando Plotly
        fig = px.imshow(matriz_correlacao,
                        labels=dict(x="Indicadores", y="Indicadores", color="Correlação"),
                        x=matriz_correlacao.columns,
                        y=matriz_correlacao.columns,
                        title='Matriz de Correlação entre Indicadores')

        # Renderizar o gráfico e passar para o template HTML
        return render_template('graficomatrizcorr.html', grafico3=fig.to_html())
    else:
        return render_template('graficomatrizcorr.html')


@app.route('/menu')
def menu():
    if 'nome' in session:
        return render_template('menu.html')
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
