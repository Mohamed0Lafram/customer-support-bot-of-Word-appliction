import pandas as pd



file = pd.read_json(r'C:\KOLCHI\me\customer-support-bot-of-Word-appliction\DataBase\paragraph_chunks.json',lines=True)

print(file.iloc[0,0]) # Display the first few rows of the DataFrame
