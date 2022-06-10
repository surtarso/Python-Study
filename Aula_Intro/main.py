# operadores matematicos

a = int(input("valor 1:")) #entrada em string convertida pra int
b = int(input("valor 2:"))
soma = a + b
subtracao = a - b
multiplicacao = a * b
divisao = a / b
resto = a % b #mod

print("soma:", soma,
      "\nsub:", subtracao,
      "\nmult:", multiplicacao,
      "\ndiv:", divisao,
      "\nmod:", resto)

print("soma é do tipo", type(soma)) #busca tipo
print(type(divisao), "div pra int:", int(divisao)) #converte tipo
print("soma:" + str(soma), "em strings concatenadas") #soma de strings

x = "1"
soma2 = int(x) + 1
print(soma2, "convertendo string para int")

# chamada de funcao dentro da string
print("soma: {}. subtracao: {}".format(soma, subtracao))
# atribuida a uma variavel
resultado = "soma: {teste1}. \nsubtracao: {teste2}".format(teste1=soma, teste2=subtracao)
print(resultado)

