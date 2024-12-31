# OctopusLAB (c) 2024
# by Petr Kracik

from pcf85176 import MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_14
from pcf85176.display import Display

__version__ = "0.0.1"
__license__ = "MIT"


class TempHumiditySigBatt(Display):
    MAX_ADDRESS = 16

    ADDR_SIGNAL_BATT = 14
    ADDR_SMALL_SEGS = 8
    ADDR_BIG_SEGS = 0

    CHARSET = {
        # DEGF HCBA
        
        " " : 0x00,
        "0" : 0xD7,
        "1" : 0x06,
        "2" : 0xE3,
        "3" : 0xA7,
        "4" : 0x36,
        "5" : 0xB5,
        "6" : 0xF5,
        "7" : 0x07,
        "8" : 0xF7,
        "9" : 0xB7,
        "c" : 0xD1,
        "e" : 0xF1,
        "f" : 0x71,
        "d" : 0xE6,
        "h" : 0x66,
        "p" : 0x73,
        "*" : 0x33
        }

    def __init__(self, bus, address=56, subaddress=0):
        super().__init__(bus, address, subaddress)
        self._mode(MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_14)
        self._buffer_battsig = bytearray(1)
        self._buffer_smalldig = bytearray(3)
        self._buffer_bigdig = bytearray(4)


    def _get_char_bits(self, char):
        if char not in self.CHARSET:
            return 0

        return self.CHARSET[char]


    def batt(self, level):
        if level > 4:
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
        if level > 4:
            raise ValueError("Out of range")

        self._buffer_battsig[0] &= ~(0xf0)
        if level > 0:
            self._buffer_battsig[0] |= 16
        if level > 1:
            self._buffer_battsig[0] |= 32
        if level > 2:
            self._buffer_battsig[0] |= 64
        if level > 3:
            self._buffer_battsig[0] |= 128


        self.write(self._buffer_battsig, self.ADDR_SIGNAL_BATT)


    def digit_small(self, digit, char, dot=False):
        self._buffer_smalldig[digit-1] = 0x00
        self._buffer_smalldig[digit-1] |= self._get_char_bits(char)
        self._buffer_smalldig[digit-1] |= 0x08 if dot else 0x00

        self.write(self._buffer_smalldig, self.ADDR_SMALL_SEGS)


    def digit_big(self, digit, char, dot=False):
        self._buffer_bigdig[digit-1] = 0x00
        self._buffer_bigdig[digit-1] |= self._get_char_bits(char)
        self._buffer_bigdig[digit-1] |= 0x08 if dot else 0x00

        self.write(self._buffer_bigdig, self.ADDR_BIG_SEGS)
