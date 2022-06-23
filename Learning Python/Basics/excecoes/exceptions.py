
## forcar um erro
# divisao = 10 / 0 ## erro: division by zero
lista = [1, 10] ## index error se acessar [3]

#tratamento do erro:
try:
    divisao = 10 / 1 #0 cai no primeiro erro
    numero = lista[1] #3 cai no segundo erro
    x = a

##ordem dos testes
except ZeroDivisionError:
    print("dividiu por zero")
except ArithmeticError: ##PAI de zeroDivisionError
    print("erro aritimetico")
except IndexError:
    print("indice invalido")
except Exception as ex: #filho de BaseException
    print("erro desconhecido: {}".format(ex))
except BaseException as ex:  # PAI de todas as excecoes
    print("erro desconhecido: {}".format(ex))

## quando n ocorrer nenhuma excecao
else:
    print("no exception ocurred")

## sempre executa
finally:
    print("vou sempre executar tendo erros ou nao")