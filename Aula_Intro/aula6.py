#funcao eh tudo q retorna valor
#metodo nao retorna
#em python, DEF

#funcao com retorno
# def soma(a, b):
#     return a + b
# print(soma(1, 2))
#---------------------------------------------------

#calculadora 1
# class Calculadora:
#     #construtor
#     def __init__(self, num1, num2):
#         self.a = num1
#         self.b = num2
#     #funcoes
#     def soma(self):
#         return self.a + self.b
#     def sub(self):
#         return self.a - self.b
#     def mult(self):
#         return self.a * self.b
#     def div(self):
#         return self.a / self.b
# #inicia a classe (instancia com valor)
# calculadora = Calculadora(10, 2)
# print(calculadora.a, calculadora.b)
# print(calculadora.soma())
# print(calculadora.sub())
# print(calculadora.mult())
# print(calculadora.div())
#--------------------------------------------------

#calculadora 2
class Calculadora:
    #construtor vazio
    def __init__(self):
        pass
    #funcoes
    def soma(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b
    def mult(self, a, b):
        return a * b
    def div(self, a, b):
        return a / b
#inicia a classe (instancia SEM valor)
calculadora = Calculadora()
#valor na chamada
print(calculadora.soma(10,5))
print(calculadora.sub(10,5))
print(calculadora.mult(10,5))
print(calculadora.div(10,5))