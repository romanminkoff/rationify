import json
import os

_settings_root = 'settings'
_settings_file_path = os.path.join(_settings_root, 'settings.json')

def _ration_path(profile):
    f = f'ration_{profile}.json'
    return os.path.join(_settings_root, f)

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

def get_ration(profile: str) -> list:
    ration_file = _ration_path(profile)
    if os.path.exists(ration_file):
        with open(ration_file) as f:
            return json.load(f)
    return []

def store_ration(profile: str, ration_json: dict):
    ration_file = _ration_path(profile)
    with open(ration_file, 'wt') as f:
        json.dump(ration_json, f)