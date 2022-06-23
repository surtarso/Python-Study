def contador_letras(lista_palavras):
    contador = []
    for i in lista_palavras:
        quantidade = len(i)
        contador.append(quantidade)
    return contador

def teste():
    print("teste")

if __name__ == '__main__':
    lista = ["cachorro", "gato"]
    print(contador_letras(lista))