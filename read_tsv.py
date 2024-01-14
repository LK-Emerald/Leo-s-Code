# Various tests for reading in the TSV file

import csv
import re
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


def find_sublist_by_word(word, list_of_lists):
    for sublist in list_of_lists:
        if word.lower() == sublist[0].lower():
            return sublist
    return None  # Return None if the word is not found in any sublist


def find_word_recursive(word, data_list, index=0, result=[]):
    matched_row = []
    related_words_str = ""
    related_words_list = []
    sub_word_result_list = []


    print(f"find words: {word}, {index}, {len(data_list)}")
    if index >= len(data_list):
        return result

    matched_row = find_sublist_by_word(word, data_list)
    if matched_row:
        # print(f"Found row with {word} as first entry")
        print(matched_row)

        # Extract the related words from col 3 (index 2)
        related_words_str = matched_row[2]
        # related_words_list = re.findall(r'\b\w+\b', related_words_str)       
        related_words_list = re.split(r'\s*\+\s*', related_words_str)
 
        # print(f"Related words:")
        # print(f"Related word str: {related_words_str}")
        # print(f"Related word list: {related_words_list}")

        for sub_word in related_words_list:

            sub_word_result_list = find_word_recursive(sub_word, data_list, index + 1, result)
            print(f"recursive results for {sub_word}, {sub_word_result_list}")
            for res_word in sub_word_result_list:
                result.append(res_word)
    else:
        print(f"Didn't find row matching word {word}")

    # if word.lower() in data_list[index][1].lower():  # Check if the word is in the sub-list


        # result.append(data_list[index])

    # Call the function recursively with the next index
    return result
    #find_word_recursive(word, data_list, index + 1, result)


search_word = input(" Lists built, now enter a word, to carry on to find all the rows related to that word")
result_recursive = find_word_recursive(search_word, result[0])

print(f"Related sub-lists for '{search_word}' using recursive approach:")
if result_recursive:
    for sublist in result_recursive:
        print(sublist)