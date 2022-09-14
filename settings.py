import json
import os

_settings_file_path = os.path.join('settings', 'settings.json')

def _read_settings(f=_settings_file_path):
    with open(f) as f:
        return json.load(f)

def _store_settings(settings, f=_settings_file_path):
    with open(f, 'w') as f:
        json.dump(settings, f)

def _read_setting(name):
    return _read_settings()[name]


def get_profiles():
    return _read_setting('profiles')

def store_profile(name):
    s = _read_settings()
    s['profiles'].append(name)
    _store_settings(s)