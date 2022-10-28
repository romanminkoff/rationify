import json
import os

_default_db_content = '{"profiles": []}'

class DB:
    def __init__(self, root_path='db'):
        self._root = root_path
        self._file = os.path.join(self._root, 'db.json')
        if not os.path.exists(self._root):
            os.mkdir(self._root)
        if not os.path.exists(self._file):
            with open(self._file, 'wt') as f:
                f.write(_default_db_content)

    def _ration_path(self, profile):
        f = f'ration_{profile}.json'
        return os.path.join(self._root, f)

    def _read_db(self):
        with open(self._file) as f:
            return json.load(f)

    def _store_db(self, data):
        with open(self._file, 'w') as f:
            json.dump(data, f)

    def _read_db_entry(self, name):
        return self._read_db()[name]

    def get_profiles(self):
        return self._read_db_entry('profiles')

    def store_profile(self, name):
        s = self._read_db()
        s['profiles'].append(name)
        self._store_db(s)

    def get_ration(self, profile: str) -> dict:
        ration_file = self._ration_path(profile)
        if os.path.exists(ration_file):
            with open(ration_file) as f:
                return json.load(f)
        return {}

    def store_ration(self, profile: str, ration_json: dict):
        ration_file = self._ration_path(profile)
        with open(ration_file, 'wt') as f:
            json.dump(ration_json, f)