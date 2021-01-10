# file to help with the editing of isle.txt
import regex
import pathlib

data_folder = str(pathlib.Path(__file__).parent.parent.absolute()) + '/data/'
isle_new = data_folder + 'isle_new.txt'
isle = data_folder + 'isle.txt'
with open(isle_new, mode='w') as new_f:
    with open(isle) as f:
        for line in f.readlines():
            new_line = regex.sub('(?<=x.*)g . ʒ', '. g ʒ', line)
            new_f.writelines(new_line)
