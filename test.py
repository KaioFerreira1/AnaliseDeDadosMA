import pandas as pd

# Carregando os dados do arquivo CSV
df = pd.read_csv("dados2.csv")

# Adicionando uma nova coluna com a soma das matrículas dos três níveis de ensino
df['Total Matrículas'] = df.sum(axis=1)

# Exibindo o DataFrame atualizado
print(df)
