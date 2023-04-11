import msvcrt
import os
import sys
import time
import colorama

from prettytable import PrettyTable
from LoadText import LoadText
from ParametersHandler import LoadParameters


class TypeSpeedTest:
    def __init__(self):
        self.path = "texts.txt"

        load_parameters = LoadParameters("parameters.txt")

        self.choose_path = load_parameters.read_parameter("choose_path")
        self.line_length = int(load_parameters.read_parameter("line_length"))
        self.max_prev_symbols = int(load_parameters.read_parameter("max_prev_symbols"))
        self.step_table = int(load_parameters.read_parameter("step_table"))

        if self.choose_path == 'T':
            self.path = "texts.txt"
        else:
            self.path = "100k_words.txt"

        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            file_path = os.path.join(sys._MEIPASS, self.path)
        else:
            file_path = self.path
        load_text = LoadText(file_path)
        if self.choose_path == 'T':
            load_text.choose_random_part_of_text()
            self.text = load_text.part_of_file
        else:
            load_text.choose_words_by_letter()
            self.text = load_text.selected_words

        self.start_with = 0
        self.end_here = self.line_length
        self.now_pos = 0
        self.prev_symbols = 0

        self.symbols_entered = 0
        self.timer = 0
        self.end_time = 0
        self.errors_count = 0
        self.accuracy = 0
        self.start_time = 0

        self.wpm_arr = []
        self.cpm_arr = []
        self.time_arr = []
        self.accuracy_arr = []

        self.fastest_cpm = 0
        self.slowest_cpm = 10000
        colorama.init()

    def print_text_line(self):
        size = os.get_terminal_size()
        size_x = size.columns
        print("\n\n", " "*(size_x//2-self.max_prev_symbols), end='')
        print(self.text[self.start_with - self.prev_symbols:self.now_pos], end='')
        for ch in range(len(self.text)):
            if self.start_with <= ch <= self.end_here:
                if ch == self.now_pos:
                    print(colorama.Fore.LIGHTWHITE_EX+colorama.Back.GREEN, end='')
                    print(self.text[ch], end='')
                    print(colorama.Fore.LIGHTWHITE_EX+colorama.Back.BLACK, end='')
                else:
                    print(self.text[ch], end='')

    def keyboard_controller(self, ch):
        esc = 27
        if ord(ch) == esc:
            ch = msvcrt.getch().decode("ASCII")
            if ord(ch) == esc:
                sys.exit(0)

    def calculate_stat_arr(self):
        if self.symbols_entered % self.step_table == 0 and self.symbols_entered != 0:
            wpm = self.calculate_speed()[1]
            cpm = self.calculate_speed()[0]
            self.wpm_arr.append(wpm)
            self.accuracy_arr.append(self.accuracy)
            self.cpm_arr.append(cpm)
            if len(self.time_arr) != 0:
                self.time_arr.append(round(self.timer, 2))
            else:
                self.time_arr.append(round(self.timer, 2))

    def plot_table(self):
        table = PrettyTable()
        green = colorama.Fore.GREEN
        red = colorama.Fore.RED
        blue = colorama.Fore.BLUE
        white = colorama.Fore.WHITE
        cyan = colorama.Fore.CYAN
        magenta = colorama.Fore.MAGENTA

        table.field_names = [green+'Symbols'+blue, blue+'WPM'+magenta, magenta+'CPM'+red, red+'Accuracy(%)'+cyan, cyan+'Time(s)'+white]
        symbols = self.step_table
        for i in range(len(self.wpm_arr)):
            row = list()
            row.append(green+str(symbols)+blue)
            row.append(blue + str(self.wpm_arr[i]) + magenta)
            row.append(magenta + str(self.cpm_arr[i]) + red)
            row.append(red+str(self.accuracy_arr[i])+cyan)
            row.append(cyan+str(self.time_arr[i])+white)
            table.add_row(row)
            symbols += self.step_table

        if self.symbols_entered == len(self.text):
            wpm = self.calculate_speed()[1]
            cpm = self.calculate_speed()[0]
            row = list()
            row.append(green + str(self.symbols_entered) + blue)
            row.append(blue + str(wpm) + magenta)
            row.append(magenta + str(cpm) + red)
            row.append(red + str(self.accuracy) + cyan)
            row.append(cyan + str(round(self.timer, 2)) + white)
            table.add_row(row)
        table.align = 'l'
        print(table)

    def type_text(self):
        ch = msvcrt.getch().decode("ASCII")
        self.calculate_stat_arr()
        self.keyboard_controller(ch)

        cpm = self.calculate_speed()[0]
        if self.fastest_cpm < cpm and self.symbols_entered > self.step_table:
            self.fastest_cpm = cpm
        if self.slowest_cpm > cpm and self.symbols_entered > self.step_table:
            self.slowest_cpm = cpm

        if self.symbols_entered == 1:
            self.start_time = time.time()
        if self.symbols_entered >= 1:
            self.end_time = time.time()

        if ch == self.text[self.now_pos]:
            self.start_with += 1
            self.end_here += 1
            self.now_pos += 1
            self.symbols_entered += 1
            if self.prev_symbols < self.max_prev_symbols:
                self.prev_symbols += 1
        else:
            self.errors_count += 1

    def calculate_speed(self):
        self.timer = self.end_time - self.start_time
        speed_cpm = abs(round(self.symbols_entered / (self.timer+0.0001) * 60, 2))
        speed_wpm = abs(round(speed_cpm / 5, 2))
        return [speed_cpm, speed_wpm]

    def calculate_accuracy(self):
        if self.symbols_entered != 0:
            self.accuracy = round(100 - (self.errors_count / self.symbols_entered * 100), 2)
        else:
            self.accuracy = 100

    def print_statistics(self):
        print("\nWPM: {}(CPM: {})".format(str(list(self.calculate_speed())[1]), str(list(self.calculate_speed())[0])))
        print("\nAccuracy: {}%".format(self.accuracy))
        print("\nCharacters entered: {}/{}".format(self.symbols_entered, len(self.text)))
        if abs(self.timer) == self.timer:
            print("\nElapsed time: {}s".format(round(self.timer), 2))
        else:
            print("\nElapsed time: 0s")


def main():
    st = TypeSpeedTest()
    while 1:
        if st.now_pos == len(st.text):
            break
        st.print_text_line()
        st.calculate_accuracy()
        st.print_statistics()
        st.type_text()
        os.system('cls')

    st.plot_table()
    print(colorama.Fore.LIGHTGREEN_EX + str("The biggest WPM: {}(CPM: {})" + colorama.Fore.LIGHTBLUE_EX +
                                            "\nThe smallest WPM: {}(CPM: {})" + colorama.Fore.LIGHTWHITE_EX).format(
        round(st.fastest_cpm / 5, 2), st.fastest_cpm, round(st.slowest_cpm / 5, 2), st.slowest_cpm))

