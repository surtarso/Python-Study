import os
import time

#acessar o arquivo de texto
with open('pingmultiplo_hosts.txt') as file:
    #coloca o conteudo em uma variavel
    dump = file.read()
    dump = dump.splitlines()

    for ip in dump:
        print('\nVERIFICANDO:')
        os.system('ping -c 2 {}'.format(ip))
        time.sleep(2)