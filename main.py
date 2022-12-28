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

        self.settings = Settings(os.path.abspath(f"{__file__}/../settings.json"), os.path.abspath(f"{__file__}/../configs"))

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
            if entry.split(".")[-1].lower() != "json":
                continue
            self.output(f"Load config '{'.'.join(entry.split('.')[:-1])}' ...", True)
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
                if self.settings.recent_config not in self.configs:
                    print("Cannot find configuration!")
                    return self.menu_main()
                if not os.path.exists(self.settings.recent_path):
                    print("The path don't exist anymore!")
                    return self.menu_main()
                print(f"Start scan of '{self.settings.recent_path}' with configuration '{self.settings.recent_config}' ...")
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
        print("SCAN")

        while True:
            path = self.input("Enter the path of the directory to scan:", "Path (Default: '.') | Cancel: 'cancel'", str)
            if path.lower() == "cancel":
                return
            if os.path.exists(path):
                break
            print("Invalid path!")

        print("")
        if len(self.configs) > 0:
            print("Available configurations:")
        else:
            print("No configurations available! Type 'manage' to create one ...")
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
        print(f"Start scan of '{path}' with configuration '{config}' ...")
        self.scan(path, config)

    def menu_configs(self):

        print("")
        if len(self.configs) > 0:
            print("Configurations:")
        else:
            print("No configurations available!")
        for config in self.configs:
            print(f"- {config}")

        value = self.input("MANAGE CONFIGURATIONS", "1: Main Menu | 2: Create | 3: Edit | 4: Delete | 5: Reload", int)
        if not value:
            print("Invalid input!")
            return self.menu_configs()
        match value:
            case 1:
                return
            case 2:
                print("")
                print("Create configuration ...")
                while True:
                    name = self.input("Type the name for the configuration to create:", "Configuration Name | Cancel: 'cancel'", str)
                    if name.lower() == "cancel":
                        return self.menu_configs()
                    if name in self.configs:
                        print("A configuration with this name already exists!")
                        continue
                    if name.strip() != "":
                        break
                    print("Invalid configuration name!")
                self.configs[name] = Config(os.path.join(self.settings.configs, name + ".json"))
                self.configs[name].save()
                return self.menu_configs()
            case 3:
                print("")
                print("Edit configuration ...")
                while True:
                    name = self.input("Type the name of the configuration to edit:", "Configuration Name | Cancel: 'cancel'", str)
                    if name.lower() == "cancel":
                        return self.menu_configs()
                    if name in self.configs:
                        break
                    print("Invalid configuration name!")
                print("")
                print("Open editor ...")
                os.system(self.settings.editor.replace("#path", self.configs[name].path))
                print("")
                print("Reload ...")
                self.load()
                return self.menu_configs()
            case 4:
                print("")
                print("Delete configuration ...")
                while True:
                    name = self.input("Type the name of the configuration to delete:", "Configuration Name | Cancel: 'cancel'", str)
                    if name.lower() == "cancel":
                        return self.menu_configs()
                    if name in self.configs:
                        break
                    print("Invalid configuration name!")
                self.configs[name].delete()
                self.configs.pop(name)
                return self.menu_configs()
            case 5:
                print("")
                print("Reload")
                self.load()
                return self.menu_configs()
            case _:
                print("Invalid input!")
                return self.menu_configs()

    def scan(self, path, config):

        result = Scan(path, self.configs[config], self)

        print("")
        print("RESULT")
        print(f"Real size: {Scan.format_size(result.real_size)} ({result.real_size} bytes)")
        print(f"Filtered size: {Scan.format_size(result.filtered_size)} ({result.filtered_size} bytes)")
        print("Type sizes:")
        for file_type, size in result.type_size.items():
            print(f"- {file_type}: {Scan.format_size(size)} ({size} bytes)")
        print(f"Lines: {result.lines} lines")
        print("Type lines:")
        for file_type, lines in result.type_lines.items():
            print(f"- {file_type}: {lines} lines")

        self.settings.recent_path = path
        self.settings.recent_config = config
        self.settings.save()

    def output(self, message, debug=False, end="\n"):

        if not debug:
            print(f"INFO:  {message}", end=end)
            return

        if self.debug:
            print(f"DEBUG: {message}", end=end)

    @staticmethod
    def input(prompt, options="String", cast=str):

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
