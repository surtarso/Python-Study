import hashlib

arquivo1 = 'a.txt'
arquivo2 = 'b.txt'

hash1 = hashlib.new('ripemd160') #sha1, md5 etc
#compara
hash1.update(open(arquivo1, 'rb').read())

hash2 = hashlib.new('ripemd160')
hash2.update(open(arquivo2, 'rb').read())

#resume(digest) os dados passados do update
if hash1.digest() != hash2.digest():
    print(f'O arquivo {arquivo1} difere de {arquivo2}')
    print(f'{arquivo1} hash', hash1.hexdigest())
    print(f'{arquivo2} hash', hash2.hexdigest())
else:
    print(f'Os arquivos são iguais!')
    print(f'{arquivo1} hash', hash1.hexdigest())
    print(f'{arquivo2} hash', hash2.hexdigest())