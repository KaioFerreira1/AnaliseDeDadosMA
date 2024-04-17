import psycopg2
def verificarlogin(nome, senha, conexao):
    cur = conexao.cursor()
    cur.execute(f"SELECT count(*) FROM usuarios WHERE login = '{nome}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False

def conectardb():
    con = psycopg2.connect(
        host='localhost',
        database='trabalho1',
        user='postgres',
        password='root'
    )
    return con

def inseriruser(login, senha, conexao):
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO usuarios (login, senha) VALUES ('{login}', '{senha}' )"
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True
    conexao.close()
    return exito

def salvar_correlacao_banco(matriz_correlacao):
    conn = conectardb()
    for ind1, row in matriz_correlacao.iterrows():
        for ind2, valor in row.items():
            if ind1 != ind2:
                inserir_correlacao(conn, ind1, ind2, valor)
    conn.close()
def inserir_correlacao(conexao, ind1, ind2, valor):
    cur = conexao.cursor()
    exito = False
    try:
        sql = "INSERT INTO resultado_correlacao (indicador1, indicador2, valor) VALUES (%s, %s, %s)"
        cur.execute(sql, (ind1, ind2, valor))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True
    return exito

def salvar_grafico_pib_municipios(conexao, dados):
    cur = conexao.cursor()
    exito = False
    try:
        sql = "INSERT INTO grafico_pib_municipios (municipio, pib) VALUES (%s, %s)"
        # Iterar sobre os dados e inserir cada registro no banco de dados
        for index, row in dados.iterrows():
            cur.execute(sql, (row['Municipios'], row['PIB']))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True
    return exito

def salvar_dados_matriculas(conexao, dados):
    cur = conexao.cursor()
    exito = False
    try:
        sql = "INSERT INTO dados_matriculas (ano, total_matriculas) VALUES (%s, %s)"
        for index, row in dados.iterrows():
            cur.execute(sql, (int(row['Ano']), int(row['Total Matrículas'])))
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True
    return exito