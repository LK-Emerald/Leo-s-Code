b_word in related_words_list:

            sub_word_result_list = find_word_recursive(sub_word, data_list, index + 1, result)
            print(f"recursive results for {sub_word}, {sub_word_result_list}")
            for res_word in sub_word_result_list:
                re