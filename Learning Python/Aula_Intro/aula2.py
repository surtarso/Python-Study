#comparadores
a = int(input("valor 1:"))
b = int(input("valor 2:"))
c = int(input("valor 3:"))
d = int(input("valor 4:"))


if a > b and a > c:
    print("maior é {}".format(a))
elif b > a and b > c:
    print("maior é {}".format(b))
else:
    print("maior é {}".format(c))

#ver se valor 1 é par (ou impar)
if a % 2 == 0:
    print("valor 1 é par")
else:
    print("valor 1 é impar")

if a % 2 == 0 or b % 2 == 0:
    print("valor 1 ou 2 é par")
else:
    print("valor 1 e 2 nao sao pares")

## media
media = (a + b + c + d) / 4
print("media: {}".format(media))
