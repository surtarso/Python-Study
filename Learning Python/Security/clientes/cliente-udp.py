import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('socket criado')

host = 'localhost'
porta = 5433
mensagem = '\nOlá servidor!'

try:
    print('cliente: ', mensagem)
    s.sendto(mensagem.encode(), (host, 5432))

    dados, servidor = s.recvfrom(4096)
    dados = dados.decode()
    print('cliente: ' +  dados)
finally:
    print('cliente: disconnecting')
    s.close()