import pandas as pd 



file = pd.read_json(r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\DataBase\paragraph_chunks.json', lines=True) 

def cheak_lenght(sentence):
    space = 0
    for letter in sentence:
        if letter == " " :
            space += 1
    if space <= 6:
        return True
    else:
        return False

drop_index = []
for i in range(len(file)):
    if cheak_lenght(file.iloc[i, 1]):
        drop_index.append(i)
        

file = file.drop(drop_index)

file.to_json(r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\DataBase\paragraph_chunks.json', orient='records', lines=True)

