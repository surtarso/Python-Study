import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('socket criado')

host = 'localhost'
porta = 5432

#faz a ligacao entre cliente/server atras do host/porta
s.bind((host, porta))
mensagem = '\nServidor: Olá clientela'

while 1:
    dados, end = s.recvfrom(4096)

    if dados:
        print('enviando mensagem...')
        s.sendto(dados + (mensagem.encode()), end)