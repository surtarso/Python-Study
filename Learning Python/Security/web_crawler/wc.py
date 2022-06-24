from collections import Counter
#manipulacao de listas tuplas etc
from bs4 import BeautifulSoup
#operadores and or etc
import operator
#requisicao http
import requests



def start(url):

    wordlist = []
    source_code = requests.get(url).text

    #requisicao dos dados e passa pra html
    soup = BeautifulSoup(source_code, 'html.parser')

    #caso o texto esteja em <div> com a classe "entry-content"
    for each_text in soup.findAll('div', {'class': 'entry-content'}):
        #transforma em string
        content = each_text.text

        words = content.lower().split()

        for each_word in words:
            wordlist.append(each_word)
        clean_wordlist(wordlist)


def clean_wordlist(wordlist):
    clean_list = []
    #remove simbolos indesejados
    for word in wordlist:
        symbols = '!@#$%^&*()_+-={[}]|\;:"<>?/,. '

        for i in range(0, len(symbols)):
            #troca o simbolo por nada ''
            word = word.replace(symbols[i], '')

        if len(word) > 0:
            #se existir ainda o simbolo, add ele
            clean_list.append(word)
    create_dictionary(clean_list)


def create_dictionary(clean_list):
    word_count = {}

    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    #conta as palavras
    for key, value in sorted(word_count.items(),
                            key = operator.itemgetter(1)):
        print("% s : % s" % (key, value))

    c = Counter(word_count)
    top = c.most_common(10)
    print(top)

#procura start e passa o site
if __name__ == '__main__':
    start("https://www.geeksforgeeks.org/python-programming-language/?ref=leftbar")