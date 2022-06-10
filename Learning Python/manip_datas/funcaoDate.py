from datetime import date, time, datetime, timedelta

def vendo_dates():
    data_atual = date.today() #contem as funcoes de data
    data_atual_str = data_atual.strftime('%a, %d %B - %Y') #virou string
    print(type(data_atual)) #ints
    print(type(data_atual_str)) #strings
    print(data_atual_str)


def vendo_times():
    horario = time(hour=15, minute=18, second=20)
    horario_str = horario.strftime('%H:%M:%S')
    print(type(horario))
    print(type(horario_str))
    print(horario_str)

def vendo_date_time():
    data_atual = datetime.now()
    print(data_atual)
    print(data_atual.strftime('%d/%m - %H:%M')) #escolhe atributos a serem vistos
    print(data_atual.strftime('%c')) ## console time padrao
    print(data_atual.day) # apenas o dia (.hour .minute etc)
    print(data_atual.weekday())
    ## segunda = 1 <---> domingo = 6
    tupla = ('segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo')
    print(tupla[data_atual.weekday()])
    data_criada = datetime(2018, 6, 20, 15, 30, 20) #cria uma data nao atual
    print(data_criada)
    print(data_criada.strftime('%c'))
    data_string = '10/01/2019' #data em string
    print(type(data_string))
    data_convertida = datetime.strptime(data_string, '%d/%m/%Y')
    print(data_convertida) #tipo string
    print(type(data_convertida)) #tipo datetime

    #operacoes com datas:
    nova_data = data_convertida - timedelta(days=365, hours=2) #retira 1 ano e 2 hs
    print(nova_data)


if __name__ == '__main__':
    vendo_dates()
    vendo_times()
    vendo_date_time()