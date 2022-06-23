#classe
from televisao import Televisao
#modulo
from Contador import contador_letras, teste

if __name__ == '__main__':
    # instancia classse
    televisao = Televisao()
    print("tv ligada?", televisao.ligada)
    televisao.power() #liga tv
    print("tv ligada?", televisao.ligada)

    # usa modulo
    lista = ["cachorro", "gato", "televisao"]
    total_letras = contador_letras(lista)
    print(total_letras)
    print(teste())