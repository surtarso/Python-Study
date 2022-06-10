## cria arquivo ou abre ja abertos
## open ( 'nome do arquivo', 'WRITE')
#w - write
#a - append (tambem cria arquivo se n existir)

#--------------------------------------------
# arquivo = open('teste.txt', 'w')
# # faz uma nova escrita ou SOBREPOE um arquivo
# arquivo.write('meu primeiro teste no arquivo')
# arquivo.close() #fecha o arquivo apos abrir
#
# arquivo = open('teste.txt', 'a')
# arquivo.write('\nsegunda linha')
# arquivo.close() #fecha o arquivo apos abrir
#--------------------------------------------

def escrever_arquivo(texto):
    arquivo = open('teste.txt', 'w') #write
    arquivo.write(texto)
    arquivo.close()

def atualizar_arquivo(texto):
    arquivo = open('teste.txt', 'a') #append
    arquivo.write(texto)
    arquivo.close()

def ler_arquivo(nome_arquivo):
    arquivo = open(nome_arquivo, 'r') #read
    texto = arquivo.read()
    print(texto)

if __name__ == '__main__':
    # escrever_arquivo('primeira linha\n')
    # atualizar_arquivo('segunda linha.\n')
    ler_arquivo('teste.txt')