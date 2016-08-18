#/usr/bin/env python2.7
# vim: fileencoding=utf-8 fileformat=unix

from distutils.core import setup
try:
    import py2exe
    PY2EXE = True
except ImportError:
    PY2EXE = False

from romaja import \
        __author__, __copyright__, __license__, __version__, __email__


if PY2EXE:
    py2exe_options = dict(
        compressed = 1,
        optimize = 2,
        bundle_files = 1,
        excludes = [
                '_ssl',
                'pyreadline', 'difflib', 'doctest', 'locale',
                'pickle', 'calendar',
                ],
        #dll_excludes = ['msvcr71.dll'],
        )

kw = dict(
    name = "romaja",
    version = __version__,
    author = __author__,
    author_email = __email__,
    license = __license__,
    platforms = ["generic"],
    py_modules = ["romaja"],
    console = [ dict(script = "romaja.py",), ],
    zipfile = "romaja.zip",
    )
if PY2EXE:
    kw["options"] = dict(py2exe = py2exe_options)
setup(**kw)
