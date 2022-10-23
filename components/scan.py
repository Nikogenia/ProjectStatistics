import os


class Scan:

    def __init__(self, path, config, main):

        self.path = path
        self.config = config
        self.main = main

        self.main.output("Iterate ...")

        self.real_size = 0
        self.filtered_size = 0
        self.type_size = {}

        self.whitelist_types = len(self.config.included_types) > 0
        self.whitelist_names = len(self.config.included_names) > 0

        self.iterate(self.path, True)

    def iterate(self, path, valid):

        if valid:
            self.main.output(f"Scan directory '{path}' ...", True)

        try:

            for entry in os.scandir(path):

                entry_valid = self.check_name(entry) and valid

                if entry.is_dir():
                    self.iterate(entry.path, entry_valid)

                if entry.is_file():
                    self.handle_file(entry, entry_valid)

        except PermissionError:
            self.main.output(f"Permission error on scanning directory '{path}' ...", True)
        except OSError:
            self.main.output(f"Unknown error on scanning directory '{path}' ...", True)

    def check_name(self, entry):

        if self.whitelist_names:
            for include_name in self.config.included_names:
                if include_name.lower() == entry.name.lower():
                    break
            else:
                return False

        for exclude_name in self.config.excluded_names:
            if exclude_name.lower() == entry.name.lower():
                return False

        return True

    def handle_file(self, entry, valid):

        if self.config.calc_size:
            file_size = os.path.getsize(entry.path)
            self.real_size += os.path.getsize(entry.path)

        if not valid:
            return

        if self.whitelist_types:
            for include_type in self.config.included_types:
                if "." + include_type.lower() == entry.name.split(".")[-1].lower():
                    break
            else:
                return

        for exclude_type in self.config.excluded_types:
            if "." + exclude_type.lower() == entry.name.split(".")[-1].lower():
                return

        self.main.output(f"Scan file '{entry.path}' ...", True)

        if self.config.calc_size:
            self.filtered_size += file_size
            if not entry.name.split(".")[-1].lower() in self.type_size:
                self.type_size[entry.name.split(".")[-1].lower()] = 0
            self.type_size[entry.name.split(".")[-1].lower()] += file_size
