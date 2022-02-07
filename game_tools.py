import random

def word_new(number):
    with open(f'words-{str(number)}.txt') as full_dic:
        lines = full_dic.read().splitlines()
        word = random.choice(lines)
    return word

def is_valid_word(word, num_letters):
    with open(f'words-{str(num_letters)}.txt') as full_dic:
        word = word.lower()
        lines = full_dic.read().splitlines()
        if word in lines:
            return True
        else:
            return False

def try_solve(word, attempt):
    stringback = ""
    print(word)
    print(attempt)
    for i, l in enumerate(attempt):
        if l in word:
            if l == word[i]:
                stringback += "Y"
            else:
                stringback += "C"
        else:
            stringback += "N"
    return stringback