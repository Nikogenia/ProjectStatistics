import sys
import os

from components.settings import Settings
from components.config import Config


class Main:

    def __init__(self, debug):

        self.debug = debug

        print("Welcome to Project Statistics")
        print("-----------------------------")
        print("")
        print("This is a statistic tool for software projects.")
        print("It's calculates file sizes, line counts and more")
        print("interesting things about the project.")
        print("")
        print("Author: Nikocraft")
        print("Version: 1.0")
        print("Language: Python")
        print(f"Debug mode: {self.debug}")
        print("")

        self.settings = Settings("./settings.json")

        self.configs = {}

        self.load()

        self.menu_main()

    def load(self):

        self.output(f"Load settings from '{self.settings.path}' ...")
        if not self.settings.load():
            self.output("Error occurred on loading settings!", True)

        self.output(f"Load configs from '{self.settings.configs}' ...")
        os.makedirs(self.settings.configs, exist_ok=True)
        for entry in os.listdir(self.settings.configs):
            if os.path.isdir(os.path.join(self.settings.configs, entry)):
                continue
            if os.path.splitext(entry)[1] != ".json":
                continue
            self.output(f"Load config '{os.path.splitext(entry)[0]}' ...", True)
            config = Config(os.path.join(self.settings.configs, entry))
            if not config.load():
                self.output("Error occurred on loading a config!", True)
            self.configs[os.path.splitext(entry)[0]] = config

    def menu_main(self):

        value = self.input("MAIN MENU", "1: Exit | 2: Scan | 3: Recent | 4: Configs | 5: Reload", int)
        if not value:
            print("Invalid input!")
            return self.menu_main()
        match value:
            case 1:
                print("")
                print("Exit ...")
            case 2:
                self.menu_scan()
                return self.menu_main()
            case 3:
                print("")
                print("Scan recent ...")
                return self.menu_main()
            case 4:
                self.menu_configs()
                self.menu_main()
            case 5:
                print("")
                print("Reload")
                self.load()
                return self.menu_main()
            case _:
                print("Invalid input!")
                return self.menu_main()

    def menu_scan(self):
        pass

    def menu_configs(self):
        pass

    def output(self, message, debug=False):

        if not debug:
            print("INFO:  " + message)
            return

        if self.debug:
            print("DEBUG: " + message)

    def input(self, prompt, options="String", cast=str):

        print("")
        print(prompt)
        print(f"[{options}]")
        value = input("> ")
        try:
            return cast(value)
        except ValueError:
            return None


if __name__ == '__main__':

    Main("-d" in sys.argv)

    sys.exit(0)
