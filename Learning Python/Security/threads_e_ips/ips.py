import ipaddress


ip = '192.168.15.252'
endereco = ipaddress.ip_address(ip)
print(endereco)
print(endereco + 100)

ip_range = '192.168.15.0/24'
rede = ipaddress.ip_network(ip_range, strict=False)
print(rede)

for ip_range in rede:
    print(ip_range)