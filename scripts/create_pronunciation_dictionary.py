import pickle
from helpers.tokenizer import tokenizer
from helpers.util import phone_to_syllable_list, load_english_words, load_isle

words = load_english_words()
isleDict = load_isle()

pronunciations_dictionary = {}

for word in words:
    pronunciations = isleDict.data.get(word)
    if not pronunciations:
        continue

    pronunciations_list = phone_to_syllable_list(pronunciations[-1][0])
    tokenized_word = tokenizer(word, pronunciations_list)

    if '' in tokenized_word:
        continue

    print(tokenized_word, pronunciations_list)

    for i, syl in enumerate(pronunciations_list):
        if pronunciations_dictionary.get(syl) is None:
            pronunciations_dictionary[syl] = {tokenized_word[i]: [tokenized_word]}
            continue
        pronunciations_dictionary[syl].setdefault(tokenized_word[i], []).append(tokenized_word)


with open('src/pronunciations/pronunciation_dictionary', mode='wb') as file:
    pickle.dump(pronunciations_dictionary, file)
