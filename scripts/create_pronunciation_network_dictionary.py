from helpers.tokenizer import tokenizer
from helpers.util import *
from collections import Counter

words = load_english_words()
isleDict = load_isle()

pronunciations_network = {}
for word in words:
    pronunciations = isleDict.data.get(word)
    if not pronunciations:
        continue

    pronunciations_list = phone_to_syllable_list(pronunciations[-1][0])

    if len(pronunciations_list) == 1:
        continue

    tokenized_word = tokenizer(word, pronunciations_list)

    if '' in tokenized_word:
        continue

    print(tokenized_word, pronunciations_list)

    for i, syl in enumerate(pronunciations_list):
        other_syls = pronunciations_list[:]
        other_syls.remove(syl)
        if not other_syls:
            continue
        if pronunciations_network.get(syl) is None:
            pronunciations_network[syl] = []
        [pronunciations_network[syl].append(s) for s in other_syls]

pronunciations_network = [{p: dict(Counter(links))} for p, links in pronunciations_network.items()]
save_pronunciation_network(pronunciations_network)