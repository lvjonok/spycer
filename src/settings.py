import os
import sys
import tempfile as tmp
from os import path
import shutil

import yaml
import vtk

_sett = None  # do not forget to load_settings() at start


def sett():
    return _sett


_colors = {}  # Available colors: https://en.wikipedia.org/wiki/File:SVG_Recognized_color_keyword_names.svg
_vtk_colors = vtk.vtkNamedColors()


def get_color(key):
    if key in _colors:
        return _colors[key]
    val = _vtk_colors.GetColor3d(key)
    _colors[key] = val
    return val


def load_settings():
    settings_filename = path.join("lib", "settings.yaml")
    if getattr(sys, 'frozen', False):
        app_path = path.dirname(sys.executable)
        # uncomment if you want some protection that nothing would be broken
        # if not path.exists(path.join(app_path, settings_filename)):
        #     bundle_path = sys._MEIPASS
        #     shutil.copyfile(path.join(bundle_path, settings_filename), path.join(app_path, settings_filename))
    else:
        # have to add .. because settings.py is under src folder
        app_path = path.join(path.dirname(__file__), "..")
    with open(path.join(app_path, settings_filename)) as f:
        data = yaml.safe_load(f)
        global _sett
        _sett = Settings(data)


def save_settings():
    settings_filename = path.join("lib", "settings.yaml")
    if getattr(sys, 'frozen', False):
        app_path = path.dirname(sys.executable)
    else:
        # have to add .. because settings.py is under src folder
        app_path = path.join(path.dirname(__file__), "..")
    temp = yaml.dump(_sett)
    temp = temp.replace("!!python/object:src.settings.Settings", "").strip()
    with open(path.join(app_path, settings_filename), 'w') as f:
        f.write(temp)


class Settings(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Settings(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Settings(b) if isinstance(b, dict) else b)
