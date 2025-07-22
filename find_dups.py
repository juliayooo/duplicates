from fuzzywuzzy import fuzz
from unidecode import unidecode
import csv
import pandas as pd
import re
from collections import defaultdict
import networkx as nx



filepath = "./data/LN_DUPLICATES.csv"

results = "./data/dup_results2.txt"

results_file = open(results, 'w')

df = pd.read_csv(filepath, encoding='ISO-8859-1')
records = df.to_dict(orient='records')


def normalize(text):
    if pd.isnull(text):
        return ''
    text = unidecode(str(text))
    text = re.sub(r'[^a-z0-9]', '', text.lower())
    return text

def is_duplicate(r1, r2, threshold=75):
    name1 = f"{r1.get('First Name', '')}"
    name2 = f"{r2.get('First Name', '')}"

    email1 = str(r1.get('Email', ''))
    email2 = str(r2.get('Email', ''))

    # phone1 = str(r1.get('Phone', ''))
    # phone2 = str(r2.get('Phone', ''))

    name_score = fuzz.token_set_ratio(name1, name2)
    email_score = fuzz.partial_ratio(email1, email2)

    final_score = 0.6 * name_score + 0.3 * email_score
    return final_score >= threshold


blocks = defaultdict(list)
for record in records:
    last_name = record.get('Last Name', '')
    if pd.isnull(last_name):
        last_name = ''
    normalized_last_name = normalize(last_name)
    length = len(normalized_last_name)
    key = normalized_last_name[:length]
    blocks[key].append(record)
print(f"Total blocks created: {len(blocks)}\n")


limit = 0
G = nx.Graph()
for block_key, block_records in blocks.items():
    if limit == 2:
                break
    print(f"Processing block: {block_key} with {len(block_records)} records")

    for i in range(len(block_records)):
        r1 = block_records[i]
        for j in range(i + 1, len(block_records)):
            
            r2 = block_records[j]
            if is_duplicate(r1, r2):
                G.add_edge(r1['Contact ID'], r2['Contact ID'])
    limit += 1

                

clusters = list(nx.connected_components(G))

print(f"Found {len(clusters)} potential duplicate groups.\n")
results_file.write(f"Found {len(clusters)} potential duplicate groups.\n")
for idx, group in enumerate(clusters, 1):
    print(f"Group {idx}:")
    for record_id in group:
        contact = df[df['Contact ID'] == record_id].to_dict(orient='records')[0]
        print(f"  - {contact['First Name']} {contact['Last Name']} | {contact['Email']} | {contact['Phone']}| {normalize(contact['Home Zip/Postal Code'])}")
    print()
