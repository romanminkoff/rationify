import json
import os

_default_settings_content = '{"profiles": []}'

class Settings:
    def __init__(self, root_path='settings'):
        self._root = root_path
        self._file = os.path.join(self._root, 'settings.json')
        if not os.path.exists(self._root):
            os.mkdir(self._root)
        if not os.path.exists(self._file):
            with open(self._file, 'wt') as f:
                f.write(_default_settings_content)

    def _ration_path(self, profile):
        f = f'ration_{profile}.json'
        return os.path.join(self._root, f)

    def _read_settings(self):
        with open(self._file) as f:
            return json.load(f)

    def _store_settings(self, settings):
        with open(self._file, 'w') as f:
            json.dump(settings, f)

    def _read_setting(self, name):
        return self._read_settings()[name]

    def get_profiles(self):
        return self._read_setting('profiles')

    def store_profile(self, name):
        s = self._read_settings()
        s['profiles'].append(name)
        self._store_settings(s)

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