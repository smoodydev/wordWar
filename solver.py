import random

# A Clean Python File of the game wordle
#######################
def solve(word, attempt):
    stringback = ""
    # print(word)
    for i, l in enumerate(attempt):
        if l in word:
            if l == word[i]:
                stringback += "Y"
            else:
                stringback += "C"
        else:
            stringback += "N"
    return stringback

def round(word):
    attempt = (input("What is the word?\n" )).lower()
    result  = solve(word, attempt)
    print(result)
    if result == ("Y"*len(word)):
        return True
    else:
        return False

def play():
    word = ""
    number = random.randint(4, 8)
    with open(f'words-{str(number)}.txt') as full_dic:
        lines = full_dic.read().splitlines()
        word = random.choice(lines)
    solved = False
    attempts = 0
    print(f'The word has {number} letters')
    while(not solved and attempts < 5):
        solved = round(word)
        attempts += 1
    print(f'The word was {word}.')
        

if __name__ == '__main__':
    play()
