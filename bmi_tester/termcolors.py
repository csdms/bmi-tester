#! /usr/bin/env python


_ATTRS = {
    "reset": "39;49;00m",
    "bright": "01m",
    "dim": "02m",
    "standout": "03m",
    "underline": "04m",
    "blink": "05m",
    "fast": "06m",
    "reverse": "07m",
    "hidden": "08m",
    "xout": "09m",
}

_COLORS = [
    ("black", "darkgray"),
    ("red", "lightred"),
    ("green", "lightgreen"),
    ("brown", "yellow"),
    ("blue", "lightblue"),
    ("purple", "lightpurple"),
    ("cyan", "lightcyan"),
    ("lightgray", "white"),
]

_CODES = {}

for (_attr, _val) in _ATTRS.items():
    _CODES[_attr] = "\x1b[" + _val

for (i, (dark, light)) in enumerate(_COLORS):
    _CODES[dark] = "\x1b[%im" % (i + 30)
    _CODES[light] = "\x1b[%i;01m" % (i + 30)


def format(name, text):
    return _CODES.get(name, "") + text + _CODES.get("reset", "")


def create_color_func(name):
    def f(text):
        return format(name, text)

    globals()[name] = f


for _name in _CODES:
    create_color_func(_name)
