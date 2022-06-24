import hashlib


string = input('digite algo para gerar hash: ')

menu = int(input(''' qual hash:
                1- md5
                    2- sha1
                        3- sha256
                            4- sha512
                escolha: '''))

if menu == 1:
    resultado = hashlib.md5(string.encode('utf-8'))
    print('MD5 da string: ', resultado.hexdigest())
elif menu == 2:
    resultado = hashlib.sha1(string.encode('utf-8'))
    print('SHA1 da string: ', resultado.hexdigest())
elif menu == 3:
    resultado = hashlib.sha256(string.encode('utf-8'))
    print('SHA256 da string: ', resultado.hexdigest())
elif menu == 4:
    resultado = hashlib.sha512(string.encode('utf-8'))
    print('SHA512 da string: ', resultado.hexdigest())
else:
    print('escolha inválida, tente novamente')