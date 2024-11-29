# OctopusLAB (c) 2024
# by Petr Kracik

from pcf85176 import MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_14
from pcf85176.display import Display

__version__ = "0.0.1"
__license__ = "MIT"


class SixDigitSigBattProgress(Display):
    MAX_ADDRESS = 31
    
    ADDR_SIGNAL_BATT = 0
    ADDR_WHEEL = 2
    ADDR_SMALL_SEGS = 6
    ADDR_PRES_LABELS = 14
    ADDR_PROGRESS = 16
    ADDR_BIG_SEGS = 20

    def __init__(self, bus, address=56, subaddress=0):
        super().__init__(bus, address, subaddress)
        self._mode(MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_14)
        self._buffer = bytearray(16)
    
    def progress(self, value):
        data = bytearray(3)
        data[0] = value
        self.write(data, self.ADDR_PROGRESS)
