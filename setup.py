#/usr/bin/env python3.5
# vim: set fileencoding=utf-8 fileformat=unix :

from setuptools import setup

from romaja import \
        __author__, __copyright__, __license__, __version__, __email__

setup(
    name = "romaja",
    version = __version__,
    author = __author__,
    author_email = __email__,
    license = __license__,
    platforms = ["generic"],
    py_modules = ["romaja"],
    console = [ dict(script = "romaja.py",), ],
    zipfile = "romaja.zip",
    entry_points = dict(
            console_scripts = ["romaja=romaja:main"],
            ),
    )
