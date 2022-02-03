# A handy tool to split python
for num in range(4, 9):
    with open(f'words-{num}.txt', 'w') as dest:
        with open('words_alpha.txt') as full_dic:
            lines = full_dic.read().splitlines()
            for line in lines:
                
                if len(line) == num:
                    print(len(line))
                    print(line)
                    dest.write(line+"\n")