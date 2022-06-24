import phonenumbers
from phonenumbers import geocoder



phone = input('digite o tel: formato -> +552122265656\n')

phone_number = phonenumbers.parse(phone)

print(geocoder.description_for_number(phone_number, 'pt'))