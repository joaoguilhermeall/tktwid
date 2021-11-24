from .widgets import HowTkinterThemeWidgetsWorks

from sys import argv

if len(argv) < 2:
    hit = HowTkinterThemeWidgetsWorks()
    hit.run()