import sys


class LoadParameters:
    def __init__(self, path):

        self.params_file = ""
        self.path = path

        self.choose_path = "T"

        self.line_length = "30"
        self.max_prev_symbols = "15"

        self.step_table = "25"

        self.size_of_part = "100"
        self.count_of_words = "20"
        self.create_params()
        try:
            with open(self.path, "r") as f:
                self.params_file = f.read()
        except FileNotFoundError:
            with open(self.path, "w") as f:
                self.create_params()
                f.write(self.params_file)

    def create_params(self):
        self.params_file = "choose_path:{};\nline_length:{};\nmax_prev_symbols:{};\nstep_table:{};" \
                           "\nsize_of_part:{};\ncount_of_words:{};".format(self.choose_path, self.line_length,
                                                                           self.max_prev_symbols,
                                                                           self.step_table, self.size_of_part,
                                                                           self.count_of_words)

    def read_parameter(self, token):
        start_index = self.params_file.find(token) + len(token) + 1
        part_of_file = self.params_file[start_index:]
        end_index = part_of_file.find(";")
        parameter = part_of_file[:end_index]
        return parameter

    def edit_parameter(self, token, new_value):
        start_index = self.params_file.find(token) + len(token) + 1
        part_of_file_old = self.params_file[start_index:]
        end_index = part_of_file_old.find(";")
        parameter = part_of_file_old[:end_index]
        part_of_file_new = part_of_file_old.replace(parameter, new_value, 1)
        self.params_file = self.params_file.replace(part_of_file_old, part_of_file_new)

    def write_parameters(self):
        try:
            with open(self.path, "w") as f:
                f.write(self.params_file)
        except FileNotFoundError:
            print('File in path "{}" no found!'.format(self.path))
            sys.exit(1)






