import itertools



string = input('string a ser permutada: ')

## quantidade de caracteres. tamanho da string ('abc', 3)
resultado = itertools.permutations(string, len(string))

for i in resultado:
    print(''.join(i))
