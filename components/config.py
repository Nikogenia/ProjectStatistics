import json
import os


class Config:

    def __init__(self, path):

        self.path = path

        self.included_types = []
        self.excluded_types = []

        self.included_names = []
        self.excluded_names = []

        self.calc_size = True
        self.calc_lines = True

    def load(self):

        try:
            with open(self.path, "r", encoding="utf-8") as file:

                data = json.load(file)

                if "included_types" in data:
                    self.included_types = data["included_types"]
                if "excluded_types" in data:
                    self.excluded_types = data["excluded_types"]

                if "included_names" in data:
                    self.included_names = data["included_names"]
                if "excluded_names" in data:
                    self.excluded_names = data["excluded_names"]

                if "calc_size" in data:
                    self.calc_size = data["calc_size"]
                if "calc_lines" in data:
                    self.calc_lines = data["calc_lines"]

        except (IOError, json.JSONDecodeError):
            return False

        return True

    def save(self):

        try:
            with open(self.path, "w", encoding="utf-8") as file:

                data = {

                    "included_types": self.included_types,
                    "excluded_types": self.excluded_types,

                    "included_names": self.included_names,
                    "excluded_names": self.excluded_names,

                    "calc_size": self.calc_size,
                    "calc_lines": self.calc_lines

                }

                json.dump(data, file, indent=4, separators=(", ", ": "))

        except IOError:
            return False

        return True

    def delete(self):

        os.remove(self.path)
