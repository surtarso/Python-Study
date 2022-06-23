from ast import arg
from termios import TIOCM_CAR
from threading import Thread
import time


# def carro1(velocidade):
#     trajeto = 0
#     while trajeto <= 100:
#         print('carro1 ', trajeto)
#         trajeto += velocidade

# def carro2(velocidade):
#     trajeto = 0
#     while trajeto <= 100:
#         print('carro2 ', trajeto)
#         trajeto += velocidade

# carro1(10)
# carro2(20)

def carro(velocidade, piloto):
    trajeto = 0
    while trajeto <= 100:
        trajeto += velocidade
        time.sleep(0.5)
        print('piloto {}'.format(piloto), 'km:{}'.format(trajeto))

t_carro1 = Thread(target=carro, args=[1, 'eu'])
t_carro2 = Thread(target=carro, args=[1.5, 'voce'])

t_carro1.start()
t_carro2.start()