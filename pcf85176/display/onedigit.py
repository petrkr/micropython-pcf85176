# OctopusLAB (c) 2025
# by Petr Kracik

from pcf85176 import MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_STATIC
from pcf85176.display import Display

__version__ = "0.0.1"
__license__ = "MIT"


class OneDigit(Display):
    MAX_ADDRESS = 39

    CHARSET = {
        # ABCD EFGH
        " " : 0x00,
        "0" : 0xFC,
        "1" : 0x60,
        "2" : 0xDA,
        "3" : 0xF2,
        "4" : 0x66,
        "5" : 0xB6,
        "6" : 0xBE,
        "7" : 0xE0,
        "8" : 0xFE,
        "9" : 0xF6
        }

    def __init__(self, bus, address=56, subaddress=0, version1fix=False):
        super().__init__(bus, address, subaddress)
        self._mode(MODE_STATUS_ENABLED, MODE_BIAS_13, MODE_DRIVE_STATIC)
        self._buffer = bytearray(4)
        self._v1fix = version1fix


    def _get_char_bits(self, char):
        if char not in self.CHARSET:
            return 0

        c = self.CHARSET[char]

        if self._v1fix:
            # PCB Board Version 1 have swapped E and F segments
            # So swap them in software for now
            bit_2 = (c >> 2) & 1
            bit_3 = (c >> 3) & 1

            if bit_2 != bit_3:
                c ^= (1 << 2) | (1 << 3)

        return c


    def digit(self, digit, char, dot=False):
        self._buffer[digit] = 0x00
        self._buffer[digit] |= self._get_char_bits(char)
        self._buffer[digit] |= 0x01 if dot else 0x00

        self.write(self._buffer, 0)
