from email.policy import strict
import random, string

#tamanho da senha a ser gerada
tamanho = 16
#estrutura da senha
chars = string.ascii_letters + string.digits + '!@#$%&*()=-+,.:/?'

rnd = random.SystemRandom()


print(''.join(rnd.choice(chars) for i in range(tamanho)))