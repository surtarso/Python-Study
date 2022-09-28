import pandas as pd

#leitura dos arquivos (criando os dataframes)
df1 = pd.read_excel("Aracaju.xlsx")
df2 = pd.read_excel("Fortaleza.xlsx")
df3 = pd.read_excel("Natal.xlsx")
df4 = pd.read_excel("Recife.xlsx")
df5 = pd.read_excel("Salvador.xlsx")

#juntando os dataframes
df = pd.concat([df1, df2, df3, df4, df5])  #concatenando os dataframes

#head e tail
df.head()
df.tail()

#amostra do conjunto de dados
df.sample(10)  #10 linhas aleatórias

#tipo de dados de cada coluna
df.dtypes

#alterando o tipo de dados de uma coluna
df["LojaID"] = df["LojaID"].astype("object")  

#verificando valores nulos
df.isnull().sum()  

#substituindo valores nulos pela media
df["Vendas"].fillna(df["Vendas"].mean(), inplace=True)  #inplace=True faz a alteração no próprio dataframe

#substituindo valores nulos por zero
df["Vendas"].fillna(0, inplace=True)  

#apagando as linhas com valores nulos
df.dropna(inplace=True)  

#apagando as linhas com valores nulos em apenas uma coluna
df.dropna(subset=["Vendas"], inplace=True)  

#removendo linhas com valores faltantes em todas as colunas
df.dropna(how="all", inplace=True)  #how="all" -> todas as colunas

## -------- CRIANDO NOVAS COLUNAS

#criando a coluna de receita
df["Receita"] = df["Vendas"].mul(df["Qtde"])  #receita = vendas * quantidade

#retornando a maior e menor receita
df["Receita"].max()
df["Receita"].min()

#nlargest -> retorna as n maiores receitas
df.nlargest(3, "Receita")  #3 maiores receitas

#nsmallest -> retorna as n menores receitas
df.nsmallest(3, "Receita")  #3 menores receitas

#agrupamento por cidade
df.groupby("Cidade")["Receita"].sum()  #soma de receita por cidade

#ordenando o conjunto de dados
df.sort_values("Receita", ascending=False).head(10)  #10 maiores receitas

## -------- TRABALHANDO COM DATAS

#transformando a coluna de data em tipo inteiro
df["Data"] = df["Data"].astype("int64")

#verificando o tipo de dado de cada coluna
df.dtypes

#transformando a coluna de data em tipo data
df["Data"] = pd.to_datetime(df["Data"])

#agrupamento por ano
df.groupby(df["Data"].dt.year)["Receita"].sum()  #soma de receita por ano

#criando uma nova coluna com o ano
df["Ano_Venda"] = df["Data"].dt.year

#extração do mês e do dia
df["Mes_Venda"], df["Dia_Venda"] = (df["Data"].dt.month, df["Data"].dt.day)

#retornar a data mais antiga
df["Data"].min()

#calculando a diferença de dias
df["Diferenca_Dias"] = df["Data"] - df["Data"].min()

#criando a coluna de trimestre
df["Trimestre_Venda"] = df["Data"].dt.quarter

#filtrando vendas de 2019 do mês de março
vendas_marco_2019 = df.loc[(df["Data"].dt.year == 2019) & (df["Data"].dt.month == 3)]  #loc -> localiza

## -------- VISUALIZAÇÃO DE DADOS

#contagem de valores
df["LojaID"].value_counts(ascending=False)  #contagem de valores por loja

#grafico de barras
df["LojaID"].value_counts(ascending=True).plot.barh();  #grafico de barras horizontal

#grafico de pizza
df.groupby(df["Data"].dt.year)["Qtde"].sum().plot.pie();  #grafico de pizza

#total de vendas por cidade
df["Cidade"].value_counts()

#adicionando titulo e alterando nome dos eixos
import matplotlib.pyplot as plt

df["Cidade"].value_counts().plot.bar(title="Total de vendas por cidade")
plt.xlabel("Cidade")
plt.ylabel("Total de vendas")

#alterando a cor
df["Cidade"].value_counts().plot.bar(title="Total de vendas por cidade", color="red")
plt.xlabel("Cidade")
plt.ylabel("Total de vendas")

#alterando o estilo
plt.style.use("ggplot")

#selecionando apenas as vendas de 2019
df_2019 = df[df["Ano_Venda"] == 2019]

#total de produtos vendidos por mes
df_2019.groupby(df_2019["Mes_Venda"])["Qtde"].sum().plot(title="Total de produtos vendidos por mês", marker="v")
plt.xlabel("Mês")
plt.ylabel("Total de produtos vendidos")
plt.legend()

#plotando o histograma
plt.hist(df["Qtde"], color="coral")

#grafico de dispersao
plt.scatter(x=df_2019["Dia_Venda"], y=df_2019["Receita"])

#salvando em png
df_2019.groupby(df_2019["Mes_Venda"])["Qtde"].sum().plot(title="Total de produtos vendidos por mês", marker="o")
plt.xlabel("Mês")
plt.ylabel("Total de produtos vendidos")
plt.legend()
plt.savefig("grafico.png")