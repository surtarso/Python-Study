# listas MUTAVEIS
lista = [12, 10, 7, 5] #colchetes
lista_animal = ["cachorro", "gato", "elefante", "lobo", "arara"]
lista_mix = [1, "3", "gato", 3]
# tuplas IMUTAVEIS
tupla = (1, 10, 12, 14) #parenteses
print(tupla)
# print(tupla[1])
##tupla[1] = 12 #erro, nao pode ser alterada
print(len(tupla))
print(len(lista_animal))

## converter lista para tupla
tupla_animal = tuple(lista_animal)
print(type(tupla_animal))
print(tupla_animal)
## converter tupla em lista
lista_numerica = list(tupla)
print(type(lista_numerica))
lista_numerica[0] = 10
print(lista_numerica)

##------- apenas listas ------------------
# print(lista_mix)
# print(type(lista_mix)) #list
#
# print(lista_mix[2]) #gato
#
# for i in lista:
#     print(i)
# #ints
# print(sum(lista))
# print(max(lista))
# print(min(lista))
# #string (alfabetico)
# print(max(lista_animal))
#
# if "lobo" in lista_animal: #iterando com if
#     print("existe")
# else:
#     print("nope, incluindo")
#     lista_animal.append("lobo")
#
# nova_lista = lista_animal * 3 #repete a lista
# print(nova_lista)
# #apagando
# nova_lista.pop() #retira a ultima posicao da lista
# print(nova_lista)
# nova_lista.pop(2) # retira a segunda posicao
# print(nova_lista)
# #ou
# nova_lista.remove("elefante") #remove um dos elefantes
# print(nova_lista)
#
# #ordenar
# lista.sort()
# lista_animal.sort()
# print(lista, "\n", lista_animal)
# #ordenar reverso
# lista_animal.reverse()
# print(lista_animal)
