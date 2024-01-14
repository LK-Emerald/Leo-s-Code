# Various tests for reading in the TSV file

import csv
RULE_PREFIX = "_"



def read_tsv_file(file_path):
    word_list = []
    rule_list = []
    bad_row_count = 0

    with open(file_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter="\t")
        
        # Skip the header if present
        header = next(tsv_reader, None)

        for row in tsv_reader:  
            if row[0] == "":
                bad_row_count += 1
                continue

            if row[0][0] == RULE_PREFIX:
                rule_list.append(row)
            elif row[0][0].isalpha():
                word_list.append(row)
            else:
                bad_row_count += 1

    return word_list, rule_list, bad_row_count

# Replace 'data.csv' with the actual path to your CSV file
file_path = 'Fira.tsv'
result = read_tsv_file(file_path)

# Display the result
for row in result[0]:
    print(f"Word: {row}")
          
for row in result[1]:
    print(f"Rule: {row}")

print(f"Total Words: {len(result[0])}")
print(f"Total Rules: {len(result[1])}")
print(f"Bad rows: {result[2]}")
