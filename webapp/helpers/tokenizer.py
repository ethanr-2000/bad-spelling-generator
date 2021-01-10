import regex
from helpers.util import load_symbol_table
symbol_table = load_symbol_table()


def matching_at_start_of_syllable(syl, pron):
    if pron == '' or syl == '':
        return False
    if pron == syl:
        return [len(syl), len(pron)]
    for i in reversed(range(len(syl)+1)):
        l = syl[:i]
        pronunciations = symbol_table.get(l)
        if pronunciations is None:
            continue
        for p in pronunciations:
            p = p[0]
            if len(pron) < len(p):
                continue
            if pron[:len(p)] == p:
                return [len(l), len(p)]
    return False


def syllables_match(spelling, pronunciation):
    if spelling == '' and pronunciation == '':
        return True
    lengths = matching_at_start_of_syllable(spelling, pronunciation)
    if not lengths:
        return False
    return syllables_match(spelling[lengths[0]:], pronunciation[lengths[1]:])


def remove_last_vowels(letters):
    matches = regex.findall('(?:(?:(?![eiou])[b-z])[aeiou]+(?![eiou])[b-z])', letters, overlapped=True)
    if not matches:
        return letters
    substring = matches[-1]  # take last match only (that's usually the one)
    vowel_start = letters.index(substring) + 1
    vowel_end = vowel_start + len(substring) - 2  # guaranteed to be a consonant on each side
    return letters[:vowel_start] + letters[vowel_end:]


def remove_all_internal_vowels(letters):
    matches = regex.findall('(?:(?:(?![eiou])[b-z])[aeiou]+(?![eiou])[b-z])', letters, overlapped=True)
    if not matches:
        return letters
    for match in matches:
        vowel_start = letters.index(match) + 1
        vowel_end = vowel_start + len(match) - 2  # guaranteed to be a consonant on each side
        letters = letters[:vowel_start] + letters[vowel_end:]
    return letters


def calculate_next_syllable(remaining_word, syl_pron):
    for letter_index in range(len(remaining_word)):
        word_start = remaining_word[:letter_index+1]
        if syllables_match(word_start, syl_pron):
            return word_start
        if syllables_match(remove_last_vowels(word_start), syl_pron):
            return word_start
        if syllables_match(remove_all_internal_vowels(word_start), syl_pron):
            return word_start
    return ''


def tokenizer(word, pl):
    if len(pl) == 1:
        return [word]
    tokenized = ['']*len(pl)
    for i, syl_pron in enumerate(pl):
        parsed = False
        while not parsed:
            tokenized[i] = calculate_next_syllable(word, syl_pron)
            if tokenized[i] != '':
                word = word[len(tokenized[i]):]
                break
            if i == 0 or len(word) <= 1:
                return tokenized
            tokenized[i-1] += word[0]
            word = word[1:]
    if word != '':
        tokenized[-1] += word
    return tokenized
