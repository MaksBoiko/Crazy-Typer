import os

from ParametersHandler import LoadParameters


class Settings:
    def __init__(self):
        self.load_parameters = LoadParameters('parameters.txt')

    def print_type_speed_test_parameters(self):
        print("You can change such parameters: ")
        print("(1) Set type of text: dict into words with definite\n letters or fragment of text:(D/T) {}".format(self.load_parameters.read_parameter('choose_path')))
        print("(2) Text line length: {}".format(self.load_parameters.read_parameter('line_length')))
        print("(3) Max previous symbols length line: {}".format(self.load_parameters.read_parameter('max_prev_symbols')))
        print("(4) Step of characters in table: {}".format(self.load_parameters.read_parameter('step_table')))
        print("(5) Approximate size of string: {}".format(self.load_parameters.read_parameter('size_of_part')))
        print("(6) Size set of words: {}".format(self.load_parameters.read_parameter('count_of_words')))

    def set_type_speed_test_parameters(self, index, new_value):
        if index == '1':
            self.load_parameters.edit_parameter('choose_path', new_value)
        elif index == '2':
            self.load_parameters.edit_parameter('line_length', new_value)
        elif index == '3':
            self.load_parameters.edit_parameter('max_prev_value', new_value)
        elif index == '4':
            self.load_parameters.edit_parameter('step_table', new_value)
        elif index == '5':
            self.load_parameters.edit_parameter('size_of_part', new_value)
        elif index == '6':
            self.load_parameters.edit_parameter('count_of_words', new_value)

        self.load_parameters.write_parameters()
        os.system('pause')

    def remove_parameters(self):
        os.remove("parameters.txt")

def main():
    settings = Settings()
    settings.print_type_speed_test_parameters()

