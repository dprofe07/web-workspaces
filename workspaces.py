import json
import os

from site import Site


class Workspace:
    def __init__(self, sites=None):
        self.sites = sites or []

    def to_jsonable_list(self):
        return [site.to_dict() for site in self.sites]

    @staticmethod
    def from_json_list(sites):
        return Workspace([Site.from_dict(site) for site in sites])

    def add(self, site):
        self.sites.append(site)

    def remove_at(self, index):
        if 0 <= index < len(self.sites):
            self.sites.pop(index)

    def move_down(self, index):
        if 0 <= index < len(self.sites) - 1:
            self.sites[index], self.sites[index + 1] = self.sites[index + 1], self.sites[index]

    def move_up(self, index):
        if 0 < index < len(self.sites):
            self.sites[index], self.sites[index - 1] = self.sites[index - 1], self.sites[index]


class Storage:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

    def save(self):
        # todo async
        with open(self.filename, 'w') as f:
            json.dump(self.to_json_data(), f)

    def load(self):
        self.create_if_missing()
        with open(self.filename, 'r') as f:
            self.data = self.from_json_dict(json.load(f))

    def to_json_data(self):
        return {name: wsp.to_jsonable_list() for (name, wsp) in self.data.items()}

    def create_if_missing(self):
        if not os.path.exists(self.filename):
            self.save()

    @staticmethod
    def from_json_dict(dct):
        return {k: Workspace.from_json_list(v) for (k, v) in dct.items()}

    def get_or_create_workspace(self, code):
        if code not in self.data:
            self.data[code] = Workspace()
            self.save()
        return self.data[code]

    def get_or_null(self, code):
        return self.data.get(code, None)
