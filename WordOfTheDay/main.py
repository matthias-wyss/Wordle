import random

path = ""


def random_word(length):
    input = open(path + 'input' + str(length) + '.txt', 'r')
    lines = input.read().splitlines()

    output = open(path + 'word' + str(length) + '.txt', 'w')
    word = random.choice(lines)
    output.write(word)

    return word


for i in range(5, 8):
    print(random_word(i))
