import random

def word_new(number):
    with open(f'words-{str(number)}.txt') as full_dic:
        lines = full_dic.read().splitlines()
        word = random.choice(lines)
    return word