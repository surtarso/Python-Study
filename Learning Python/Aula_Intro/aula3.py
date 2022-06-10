## for/while

# for i in range(100): # 0 a 99
#     print(i)
# for j in range(1,100): # 1 ao 99
#     print(j)

#numeros primos
# a = int(input("numero: "))
# div = 0
# for x in range(1, a+1):
#     resto = a % x
#     if resto == 0:
#         div += 1
# if div == 2: #se conseguir divisao apenas 2 vezes é primo
#     print("numero", a, "é primo")
# else:
#     print("numero {} nao é primo".format(a))
#-------------------------------------------------------------------

# a = int(input("valor: "))
# for i in range(a+1):
#     div = 0
#     for x in range(1, i+1):
#         resto = i % x
#         if resto == 0:
#             div += 1
#     if div == 2: #se conseguir divisao apenas 2 vezes é primo
#         print("numero", i, "é primo")
#-------------------------------------------------------------------

# a = 0
# while a < 10: #do 0 ao 9
#     print(a)
#     a += 1
# #-------
# b = 1
# while b <= 10: #do 1 ao 10
#     print(b)
#     b +=1
#---------------------------------------------------------------------

# imput continuo ate receber valor correto
nota = int(input("entre com a nota (entre 1 e 10):"))
while nota > 10:
    nota = int(input("range incorreto, novamente:"))
print(nota)