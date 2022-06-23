import socket
import sys


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as e:
        print('conexão falhou')
        print(e)
        sys.exit()
    
    print('socket criado')

    HostAlvo = input('ip/host p/ conectar: ')
    PortaAlvo = input('porta: ')

    try:
        s.connect((HostAlvo, int(PortaAlvo)))
        print('conectado com sucesso em {}:{}'.format(HostAlvo,PortaAlvo))
        s.shutdown(2)
    except socket.error as e:
        print('conexão falhou em {}:{}'.format(HostAlvo,PortaAlvo))
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()