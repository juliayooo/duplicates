import pandas as pd 


filepath = "./data/DUP_CHECK.csv"

df = pd.read_csv(filepath , encoding='ISO-8859-1')

duplicate_lastnames = df[df.duplicated('Last Name', keep=False)]
duplicate_lastnames.to_csv('./data/LN_DUPLICATES.csv', index=False)
print("found ", len(duplicate_lastnames), "duplicates with the same last name")