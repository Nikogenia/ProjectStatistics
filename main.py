import sys
import os

from components.settings import Settings
from components.config import Config
from components.scan import Scan


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

        value = self.input("MAIN MENU", "1: Exit | 2: Scan | 3: Recent | 4: Configurations | 5: Reload", int)
        if not value:
            print("Invalid input!")
            return self.menu_main()
        match value:
            case 1:
                print("")
                print("Exit")
            case 2:
                self.menu_scan()
                return self.menu_main()
            case 3:
                print("")
                print("Scan recent")
                print("")
                print(f"Start scan of {self.settings.recent_path} with configuration {self.settings.recent_config} ...")
                self.scan(self.settings.recent_path, self.settings.recent_config)
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

        print("")
        print("Scan")

        while True:
            path = self.input("Enter the path of the directory to scan:", "Path (Default: '.') | Cancel: 'cancel'", str)
            if path.lower() == "cancel":
                return
            if os.path.exists(path):
                break
            print("Invalid path!")

        print("")
        print("Available configurations:")
        for config in self.configs:
            print(f"- {config}")

        while True:
            config = self.input("Type the name of the configuration to use:", "Configuration Name | Manage configurations: 'manage' | Cancel: 'cancel'", str)
            if config.lower() == "cancel":
                return
            if config.lower() == "manage":
                return self.menu_configs()
            if config in self.configs:
                break
            print("Invalid configuration name!")

        print("")
        print(f"Start scan of {path} with configuration {config} ...")
        self.scan(path, config)

    def menu_configs(self):
        pass

    def scan(self, path, config):

        result = Scan(path, self.configs[config], self)

        print(f"Real size: {result.real_size}")
        print(f"Filtered size: {result.filtered_size}")
        print("Type sizes:")
        for file_type, size in result.type_size.items():
            print(f"- {file_type}: {size}")

        self.settings.recent_path = path
        self.settings.recent_config = config
        self.settings.save()

    def output(self, message, debug=False):

        if not debug:
            print(f"INFO:  {message}")
            return

        if self.debug:
            print(f"DEBUG: {message}")

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
