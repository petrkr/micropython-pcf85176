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
        self._buffer_battsig = bytearray(1)


    def progress(self, value):
        data = bytearray(3)
        data[0] = value
        self.write(data, self.ADDR_PROGRESS)


    def batt(self, level):
        self._buffer_battsig[0] &= ~(0x0f)
        self._buffer_battsig[0] |= 15 << (4 - level)

        self.write(self._buffer_battsig, self.ADDR_SIGNAL_BATT)


    def signal(self, level):
        self._buffer_battsig[0] &= ~(0xf0)
        self._buffer_battsig[0] |= (15 << (8 - level))
        self.write(self._buffer_battsig, self.ADDR_SIGNAL_BATT)


    def wheel(self, data):
        self.write(data, self.ADDR_WHEEL)
