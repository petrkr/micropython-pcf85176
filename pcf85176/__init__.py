# OctopusLAB (c) 2024
# by Petr Kracik

__version__ = "0.0.1"
__license__ = "MIT"

MODE_STATUS_BLANK = 0
MODE_STATUS_ENABLED = 1

MODE_BIAS_13 = 0
MODE_BIAS_12 = 1

MODE_DRIVE_STATIC = 1
MODE_DRIVE_12 = 2
MODE_DRIVE_13 = 3
MODE_DRIVE_14 = 0

BLINK_FREQUENCY_OFF = 0
BLINK_FREQUENCY_1 = 1
BLINK_FREQUENCY_2 = 2
BLINK_FREQUENCY_3 = 3

BLINK_MODE_NORMAL = 0
BLINK_MODE_ALTRAM = 1

class PCF85176():
    MAX_ADDRESS = 39

    CMD_LOAD_POINTER = 0x00
    CMD_MODE = 0x40
    CMD_DEVICE_SELECT = 0x60
    CMD_BLINK = 0x70
    CMD_BANK_SELECT = 0x78


    def __init__(self, bus, address=56, subaddress=0):
        self._bus = bus
        self._addr = address
        self._subaddr = subaddress


    def _device_select(self, lastcommand=False):
        data = bytearray(1)
        data[0] |= 0x00 if lastcommand else 0x80
        data[0] |= self.CMD_DEVICE_SELECT
        data[0] |= self._subaddr

        self._bus.writeto(self._addr, data)


    def _mode(self, status=MODE_STATUS_ENABLED, bias=MODE_BIAS_13, drive=MODE_DRIVE_14, lastcommand=False):
        data = bytearray(1)
        data[0] |= 0x00 if lastcommand else 0x80
        data[0] |= self.CMD_MODE
        data[0] |= status << 3
        data[0] |= bias << 2
        data[0] |= drive
        
        print(data)
    
        self._bus.writeto(self._addr, data)


    def bank_select(self, input_bank=0, output_bank=0, lastcommand=False):
        data = bytearray(1)
        data[0] |= 0x00 if lastcommand else 0x80
        data[0] |= self.CMD_BANK_SELECT
        data[0] |= self.input_bank << 1
        data[0] |= self.output_bank

        self._bus.writeto(self._addr, data)


    def blink(self, freq=BLINK_FREQUENCY_OFF, mode=BLINK_MODE_NORMAL, lastcommand=False):
        data = bytearray(1)
        data[0] |= 0x00 if lastcommand else 0x80
        data[0] |= self.CMD_BLINK
        data[0] |= mode << 2
        data[0] |= freq
        
        self._bus.writeto(self._addr, data)


    def write(self, lcddata, address=0):
        if not isinstance(lcddata, (bytes, bytearray)):
            raise ValueError("Invalid data type, use bytes or bytearray")

        if address > self.MAX_ADDRESS:
            raise ValueError("Invalid address")

        if address + (len(lcddata) // 2) > self.MAX_ADDRESS:
            raise ValueError("Data overflow address")

        data = bytearray(1)
        data[0] |= address
        data.extend(lcddata)
        
        print(data)

        self._bus.writeto(self._addr, data)
