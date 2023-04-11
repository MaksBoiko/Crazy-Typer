import sys
import random
import os
from ParametersHandler import LoadParameters


class LoadText:
    def __init__(self, path):
        load_parameters = LoadParameters("parameters.txt")
        self.file = ""
        self.size_of_part = int(load_parameters.read_parameter('size_of_part'))
        self.start_read_with = 0
        self.part_of_file = ""
        self.count_of_words = int(load_parameters.read_parameter('count_of_words'))
        self.selected_words = ""
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            path = os.path.join(sys._MEIPASS, path)
        try:
            with open(path, "r", encoding="utf8") as f:
                self.file = f.read()
        except FileNotFoundError:
            print('File in path "{}" no found!'.format(path))
            sys.exit(1)

    def choose_random_part_of_text(self):
        self.start_read_with = random.randint(0, len(self.file)-self.size_of_part)
        for ch in range(self.start_read_with, self.start_read_with+self.size_of_part):
            if self.file[ch] == "\n":
                self.part_of_file += " "
            else:
                self.part_of_file += self.file[ch]

        for ch in range(len(self.part_of_file)):
            if self.part_of_file[ch] == '.':
                ch += 1
                while self.part_of_file[ch] == " ":
                    ch += 1
                self.part_of_file = self.part_of_file[ch:]
                break
        banned_symbols = ['—', '”', "’", '`', "‚", "„", "‘", "’", '“', '–', "—", "«", "»", "“", "”", '’']
        for ch in banned_symbols:
            self.part_of_file.replace(ch, '')

    def choose_words_by_letter(self):
        letter = chr(random.randint(ord('a'), ord('z')))
        list_of_words = self.file.split("\n")
        counter = 0
        while counter <= self.count_of_words:
            rand_word = random.randint(0, len(list_of_words))
            if letter in list_of_words[rand_word]:
                self.selected_words += str(list_of_words[rand_word])+" "
                counter += 1
        print(self.selected_words)


