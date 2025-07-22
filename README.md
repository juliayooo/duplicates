# duplicates
## overview 
This repo contains all files used to identify potential duplicate records in Salesforce Contacts. 

### required packages 

- python  
- pandas  
- fuzzywuzzy
- unidecode
- re
- collections
- networkx 

### LN_match.py 
To use, edit the input file path to your **full contact record**, and output path if desired.
Run

```  python LN_match.py   ```

The script will output a list of only records with last name matches (strict). 

### find_dups.py

To use, edit input path to the output location of LN_match. Edit output paths as desired and run 

``` python find_dups.py ```

This script uses fuzzy wuzzy (Levenshtein Distance Algo) to find potential duplicates based on first name and email matches within a given similarity threshold. This can be edited by editing the "threshold" argument. 
The script creates a graph and adds edges between potential contacts.
The script will output a new CSV with all potential matches grouped together, grouped by a new "group number" column. 


