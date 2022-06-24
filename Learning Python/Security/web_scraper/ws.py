from bs4 import BeautifulSoup
import requests

site = requests.get('https://www.climatempo.com.br/').content


soup = BeautifulSoup(site, 'html.parser')


## prettify transforma o html em string
# print(soup.prettify())

# ondamax = soup.find('img', class_="lazyload _margin-l-10 _margin-r-5")
# print(ondamax.string)

print(soup.a.string)