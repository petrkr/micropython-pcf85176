# OctopusLAB (c) 2024
# by Petr Kracik

from pcf85176 import PCF85176

__version__ = "0.0.1"
__license__ = "MIT"

class Display(PCF85176):
    def __init__(self, bus, address, subaddress):
        super().__init__(bus, address, subaddress)
