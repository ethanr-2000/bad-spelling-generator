import pickle
import pathlib
from pysle import isletool as it
data_folder = str(pathlib.Path(__file__).parent.parent.absolute()) + '/data/'


def clean(p_list):
    punc = [u'ˈ', u'ˌ', u' ', u'-', u',', u'\'', u'ˈ', u'̩']
    for p in punc:
        for i, phone in enumerate(p_list):
            p_list[i] = phone.replace(p, '')
    return p_list


def phone_to_syllable_list(phone):
    p_list = phone.replace('#', '.').split('.')
    p_list = [x for x in p_list if x]
    p_list = clean(p_list)
    return p_list


def load_english_words():
    words = []
    with open(data_folder + 'english3.txt') as f:
        for word in f.readlines():
            words.append(word.strip('\n'))
    return words


def load_symbol_table():
    symbol_table = {}
    with open(data_folder + 'symbol_table.txt') as f:
        for sound in f.readlines():
            sound = sound.strip('\n')
            l, pronunciation = sound.split('\t')[:2]
            pronunciation = pronunciation.replace(':', '').split(' ')
            if symbol_table.get(l):
                symbol_table[l].append(pronunciation)
                continue
            symbol_table.update({l: [pronunciation]})
    return symbol_table


def save_pronunciation_dictionary(new_pron_dict):
    with open(data_folder + 'pronunciation_dictionary', mode='wb') as file:
        pickle.dump(new_pron_dict, file)


def load_pronunciation_dictionary():
    with open(data_folder + 'pronunciation_dictionary', mode='rb') as file:
        return pickle.load(file)


def save_pronunciation_network(new_pron_dict):
    with open(data_folder + 'pronunciations_network', mode='wb') as file:
        pickle.dump(new_pron_dict, file)


def load_pronunciation_network():
    with open(data_folder + 'pronunciations_network', mode='rb') as file:
        return pickle.load(file)


def load_isle():
    return it.LexicalTool(data_folder + 'isle.txt')
