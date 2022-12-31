import random
from helpers.tokenizer import tokenizer
from helpers.util import *


def spell_bad(original_word, isledict, pd):
    spell_bad_result = {
        'word': original_word,
        'badlySpelled': [original_word],
        'syllableOrigins': []
    }
    try:
        phones = random.choice(isledict.lookup(original_word))[0][0]
    except it.WordNotInISLE:
        spell_bad_result['syllableOrigins'] = None
        return spell_bad_result

    phones = clean([''.join(syl) for syl in phones])
    tokenized_word = tokenizer(original_word, phones)
    if len(phones) != len(tokenized_word):
        return spell_bad_result

    new_word = []
    for p in phones:
        if not pd.get(p):
            return spell_bad_result
        new_spelling = random.choice(list(pd[p].keys()))
        spelling_origin = random.choice(pd[p][new_spelling])
        new_word.append(new_spelling)
        spell_bad_result['syllableOrigins'].append({
            'word': spelling_origin,
        })
    spell_bad_result['badlySpelled'] = new_word

    return spell_bad_result

