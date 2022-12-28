import json
import os


class Settings:

    def __init__(self, path, default_config_path):

        self.path = path

        self.configs = default_config_path
        self.editor = "notepad.exe #path"
        self.recent_path = ""
        self.recent_config = "all"

    def load(self):

        if not os.path.exists(self.path):
            self.save()

        try:
            with open(self.path, "r", encoding="utf-8") as file:

                data = json.load(file)

                if "configs" in data:
                    self.configs = data["configs"]
                if "editor" in data:
                    self.editor = data["editor"]
                if "recent_path" in data:
                    self.recent_path = data["recent_path"]
                if "recent_config" in data:
                    self.recent_config = data["recent_config"]

        except (IOError, json.JSONDecodeError):
            return False

        return True

    def save(self):

        try:
            with open(self.path, "w", encoding="utf-8") as file:

                data = {

                    "configs": self.configs,
                    "editor": self.editor,
                    "recent_path": self.recent_path,
                    "recent_config": self.recent_config

                }

                json.dump(data, file, indent=4, separators=(", ", ": "))

        except IOError:
            return False

        return True
