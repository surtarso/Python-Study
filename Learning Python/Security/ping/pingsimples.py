#integra os programas e recursos do OS
import os

ip_ou_host = input("digite o IP ou Host: ")

#usando a lib OS para passar comandos pro OS:
os.system('ping -c 6 {}'.format(ip_ou_host))