#contador versao Modulos_Classes_Lambda
from Contador import contador_letras

contador_letras = lambda lista: [len(i) for i in lista]

lista_animais = ["cachorro", "gato", "elefante"]
print(contador_letras(lista_animais))

#funcoes lambda
soma = lambda a, b: a + b
sub = lambda a,b: a - b
print(soma(5,10))
print(sub(10,5))

## dicionario de funcoes lambda
calculadora = {
    'soma': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mult': lambda a, b: a * b,
    'div': lambda a, b: a / b,
    'mod': lambda a, b: a % b
}
print(type(calculadora)) # class dictonary

soma = calculadora['soma'] ##lambda a, b: a + b
mult = calculadora['mult']
print(soma(10, 5))
print(mult(10, 2))
