import pandas as pd 


filepath = "./data/CONTACTS_FULL.csv"

df = pd.read_csv(filepath , encoding='ISO-8859-1')

duplicate_lastnames = df[df.duplicated('Last Name', keep=False)]
duplicate_lastnames.to_csv('./data/LN_DUPLICATES_FULL.csv', index=False)
print("found ", len(duplicate_lastnames), "duplicates with the same last name")