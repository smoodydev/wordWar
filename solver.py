import random

words = [
    "abuse",
    "adult",
    "agent",
    "anger",
    "apple",
    "award",
    "basis",
    "beach"
    ]

def solve(word, attempt):
    stringback = ""
    print(word)
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
    word = random.choice(words)
    # print(word)
    solved = False
    attempts = 0
    while(not solved and attempts < 5):
        solved = round(word)
        attempts += 1
        




if __name__ == '__main__':
    play()