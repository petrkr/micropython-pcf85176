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

    CHARSET = {
        # ABCH FGED
        "0" : 0xEB,
        "1" : 0x60,
        "2" : 0xC7,
        "3" : 0xE5,
        "4" : 0x6C,
        "5" : 0xAD,
        "6" : 0xAF,
        "7" : 0xE0,
        "8" : 0xEF,
        "9" : 0xED,
        "e" : 0x8F,
        "f" : 0x8E,
        "d" : 0x77,
        "h" : 0x76
        }

    def __init__(self, bus, address=56, subaddress=0):
        super().__init__(bus, address, subaddress)
        self._mode(MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_14)
        self._buffer_battsig = bytearray(1)
        self._buffer_smalldig = bytearray(4)
        self._buffer_bigdig = bytearray(6)


    def _get_char_bits(self, char):
        if char not in self.CHARSET:
            return 0

        return self.CHARSET[char]


    def progress(self, value):
        data = bytearray(3)
        data[0] = value
        self.write(data, self.ADDR_PROGRESS)


    def batt(self, level):
        if value > 4:
            raise ValueError("Out of range")

        self._buffer_battsig[0] &= ~(0x0f)
        if level > 0:
            self._buffer_battsig[0] |= 8
        if level > 1:
            self._buffer_battsig[0] |= 4
        if level > 2:
            self._buffer_battsig[0] |= 2
        if level > 3:
            self._buffer_battsig[0] |= 1

        self.write(self._buffer_battsig, self.ADDR_SIGNAL_BATT)


    def signal(self, level):
        if value > 4:
            raise ValueError("Out of range")

        self._buffer_battsig[0] &= ~(0xf0)
        if level > 0:
            self._buffer_battsig[0] |= 128
        if level > 1:
            self._buffer_battsig[0] |= 64
        if level > 2:
            self._buffer_battsig[0] |= 32
        if level > 3:
            self._buffer_battsig[0] |= 16


        self.write(self._buffer_battsig, self.ADDR_SIGNAL_BATT)


    def wheel(self, data):
        self.write(data, self.ADDR_WHEEL)


    def digit_small(self, digit, char, dot=False):
        self._buffer_smalldig[digit-1] = 0x00
        self._buffer_smalldig[digit-1] |= self._get_char_bits(char)
        self._buffer_smalldig[digit-1] |= 0x10 if dot else 0x00

        self.write(self._buffer_smalldig, self.ADDR_SMALL_SEGS)


    def digit_big(self, digit, char, dot=False):
        self._buffer_bigdig[6-digit] = 0x00
        self._buffer_bigdig[6-digit] |= self._get_char_bits(char)
        self._buffer_bigdig[6-digit] |= 0x10 if dot else 0x00

        self.write(self._buffer_bigdig, self.ADDR_BIG_SEGS)
