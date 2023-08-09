import random

def get_random_numbers():
    numbers = sorted(random.sample(range(1, 26), 15))
    print(numbers)
    return numbers

print("15 random numbers between 1-25: ")
get_random_numbers()
