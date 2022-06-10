## [] Lista
## () Tupla
## {} Conjunto

# conjunto = {1, 2, 3, 4, 4, 3, 3, 2, 1, 1} #nao repete elementos repetidos
# print(type(conjunto))
# print(conjunto)
#
# conjunto.add(5)
# print(conjunto)
#
# conjunto.discard(2)
# print(conjunto)
#--------------------------------------------------

conjunto = {1, 2, 3, 4, 5}
conjunto2 = {5, 6, 7, 8, 9, 10}
conjunto_uniao = conjunto.union(conjunto2)
print(conjunto_uniao) #nao repete o 5 repetido
conjunto_intersecao = conjunto.intersection(conjunto2)
print(conjunto_intersecao) #mostra o repetido
conjunto_diferenca = conjunto.difference(conjunto2)
print(conjunto_diferenca) #numeros q tem apenas no conjunto1
conjunto_diferenca2 = conjunto2.difference(conjunto)
print(conjunto_diferenca2) #numeros apenas do conjunto2

#diferenca simetrica (o que nao tem nos 2, so tem no 1 e so tem no 2)
conjunto_diff_simetrico = conjunto.symmetric_difference(conjunto2)
print(conjunto_diff_simetrico) #remove o q tem de repetido (no caso o 5)

## pertinencia
# "está contido"
# subset retorna se um conjunto é um sobconjunto do outro conjunto
conjunto_a = {1, 2, 3}
conjunto_b = {1, 2, 3, 4, 5}
conjunto_subset_true = conjunto_a.issubset(conjunto_b)
conjunto_subset_false = conjunto_b.issubset(conjunto_a)
print(conjunto_subset_true) # true = a esta contido em b
print(conjunto_subset_false) # false = b nao esta contido em a
# "contém"
conjunto_superset = conjunto_b.issubset(conjunto_a)
print(conjunto_superset) # true = b contem a

## converter lista para conjunto
# para tirar duplicidade
lista = ["cachorro", "cachorro", "gato", "zebra"]
lista_para_conjunto = set(lista) # retira cachorro repetido
print(lista_para_conjunto)