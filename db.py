from benedict import benedict
import json
from pathlib import Path


class DB:
    def __init__(self, name):
        self.name = name
        if not Path(f'data/{self.name}.json').is_file():
            with open(f'data/{self.name}.json', 'w') as f: f.write('{}')

    def get(self, key):
        with open(f'data/{self.name}.json', 'r') as f:
            data = benedict(json.load(f))
            return data.get(key)

    def set(self, key, val):
        with open(f'data/{self.name}.json', 'r') as f:
            data = benedict(json.load(f))
        with open(f'data/{self.name}.json', 'w') as f:
            data.set(key, val)
            json.dump(data, f, indent=4)

    def has_key(self, key, mainkey):
        with open(f'data/{self.name}.json', 'r') as f:
            if len(key) != 0:
                data = benedict(json.load(f))
                return mainkey in data.get(key).keys()

            else:
                data = benedict(json.load(f))
                return mainkey in data.keys()

