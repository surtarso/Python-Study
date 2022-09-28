import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn")

#upload de arquivos do google colap (necessário para o google colab)
# from google.colab import files
# arq = files.upload()

df = pd.read_excel("AdventureWorks.xlsx")
# print(df.head())

#quantidade de linhas e colunas
# df.shape

#verificando os tipos de dados
# df.dtypes

#valor da receita total
df["Valor Venda"].sum()

#custo total
df["custo"] = df["Custo Unitário"].mul(df["Quantidade"])  #criando a coluna custo
round(df["custo"].sum(), 2)  #arredondando para 2 casas decimais

#com a receita, custo e o total, podemos criar a coluna de lucro (receita - custo)
df["lucro"] = df["Valor Venda"] - df["custo"]
round(df["lucro"].sum(), 2)

#criando uma coluna com o total de dias para enviar o produto
df["Tempo Envio"] = (df["Data Envio"] - df["Data Venda"]).dt.days  #dt.days -> retorna apenas os dias(remove a palavra "days" da tabela)

#verificando o tipo de dados da coluna tempo de envio
df["Tempo Envio"].dtype

#media de tempo de envio por marca
df.groupby("Marca")["Tempo Envio"].mean()

#verifica se há valores nulos
df.isnull().sum()

#agrupar por ano e marca
df.groupby([df["Data Venda"].dt.year, "Marca"])["lucro"].sum()

#resetando o index (reformata a tabela de acordo com o agrupamento)
lucro_ano = df.groupby([df["Data Venda"].dt.year, "Marca"])["lucro"].sum().reset_index()

#total de produtos vendidos
df.groupby(df["Data Venda"].dt.year)["Quantidade"].sum().sort_values(ascending=False).plot.barh(title="Total Produtos Vendidos")
plt.xlabel("Total")
plt.ylabel("Ano")

#lucro por ano
df.groupby(df["Data Venda"].dt.year)["lucro"].sum().plot.bar(title="Lucro x Ano")
plt.xlabel("Ano")
plt.ylabel("Receita")

#---selecionando apenas as vendas de 2009
df_2009 = df[df["Data Venda"].dt.year == 2009]

#lucro por mes
df_2009.groupby(df_2009["Data Venda"].dt.month)["lucro"].sum().plot(title="Lucro x Mês")
plt.xlabel("Mês")
plt.ylabel("Lucro")

#lucro por marca
df_2009.groupby("Marca")["lucro"].sum().plot.bar(title="Lucro x Marca")
plt.xlabel("Marca")
plt.ylabel("Lucro")

#lucro por classe
df_2009.groupby("Classe")["lucro"].sum().plot.bar(title="Lucro x Classe")
plt.xlabel("Classe")
plt.ylabel("Lucro")


#analise estatica
df["Tempo Envio"].describe()

#boxplot
plt.boxplot(df["Tempo Envio"])

#histograma
plt.hist(df["Tempo Envio"])

#tempo minimo de envio
df["Tempo Envio"].min()

#tempo maximo de envio
df["Tempo Envio"].max()

#identificando o outlier (numero que esta fora do padrão)
df[df["Tempo Envio"] == 20]

#salvar analise em novo arquivo
df.to_csv("df_vendas_novo.csv", index=False)