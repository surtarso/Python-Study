#error herda de Exception (classe oficial)
class Error(Exception):
    pass
#inputerror herda de Error (classe personalizada)
class InputError(Error):
    def __init__(self, message):
        self.message = message

while True:
    try:
        x = int(input("numero de 0 a 10: "))

        if x > 10:
            raise InputError("valor maior que 10") ## puxa um erro propositalmente
        elif x < 0:
            raise InputError("valor menor que 0")

        break; #forca saida do loop se der tudo certo
    except ValueError:
        print("valor invalido, apenas numeros")
    except InputError as ex: ## trata o erro proposital
        print(ex)