import sys
import msvcrt
import os
import colorama

import TypeSpeedTest
import Settings

from Settings import Settings as Set

# pyinstaller --onefile --name 'Crazy typer' --add-data '100k_words.txt;.' --add-data 'texts.txt;.' --add-data 'parameters.txt;.' MainMenu.py

class MainMenu:
    def __init__(self):
        self.items = {'1': 'Start typing', '2': 'User statistics', '3': 'Options', '4': 'Exit'}
        colorama.init()

    def print_menu(self):
        for item in self.items:
            print(colorama.Fore.LIGHTWHITE_EX+"({}) {}".format(item, self.items[item]))

    def choose_item_menu(self):
        while 1:
            os.system('cls')
            self.print_menu()
            choose = msvcrt.getch().decode('ASCII')
            if choose == '1':
                os.system('cls')
                TypeSpeedTest.main()
                green = colorama.Fore.GREEN
                red = colorama.Fore.RED
                white = colorama.Fore.LIGHTWHITE_EX
                print("\nDo you want to retry?(" + green + "y" + white + "/" + red + colorama.Fore.RED + "n" + white + ")")
                retry = msvcrt.getch().decode('ASCII')
                if retry == 'n':
                    self.choose_item_menu()
                else:
                    os.system('cls')
                    TypeSpeedTest.main()
            elif choose == '2':
                pass
            elif choose == '3':
                os.system('cls')
                Settings.main()
                print("Enter 'x' for exit from settings \nor numbers(1-6) for setting of program...")
                setting = msvcrt.getch().decode('ASCII')
                if setting == '1' or setting == '2' or setting == '3' or setting == '4' or setting == '5' or setting == '6':
                    while 1:
                        settings = Set()
                        new_value = input("Enter new value for setting ({})".format(setting))
                        settings.set_type_speed_test_parameters(setting, new_value)
                        os.system('cls')
                        break
                else:
                    self.choose_item_menu()
            elif choose == '4':
                sys.exit(0)


mm = MainMenu()
mm.choose_item_menu()
