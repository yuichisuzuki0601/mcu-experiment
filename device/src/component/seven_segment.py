from machine import Pin

class SevenSegment74hc595():
    DIGITS = {
        0:  0b00111111,
        1:  0b00000110,
        2:  0b01011011,
        3:  0b01001111,
        4:  0b01100110,
        5:  0b01101101,
        6:  0b01111101,
        7:  0b00000111,
        8:  0b01111111,
        9:  0b01101111,
        10: 0b01110111,
        11: 0b01111100,
        12: 0b00111001,
        13: 0b01011110,
        14: 0b01111001,
        15: 0b01110001,
    }

    def __init__(self, sck_gpio_number: int, sdi_gpio_number: int, lat_gpio_number: int):
        self.sck_gpio_number = sck_gpio_number
        self.sdi_gpio_number = sdi_gpio_number
        self.lat_gpio_number = lat_gpio_number
        self.sck_pin = Pin(sck_gpio_number, Pin.OUT)
        self.sdi_pin = Pin(sdi_gpio_number, Pin.OUT)
        self.lat_pin = Pin(lat_gpio_number, Pin.OUT)

    def _write_byte(self, value: int):
        self.lat_pin.value(0)
        for bit in range(7, -1, -1):
            self.sck_pin.value(0)
            self.sdi_pin.value((value >> bit) & 1)
            self.sck_pin.value(1)
        self.sck_pin.value(0)
        self.lat_pin.value(1)
        self.lat_pin.value(0)
        print(f'SevenSegment74hc595 \'{(self.sck_gpio_number, self.sdi_gpio_number, self.lat_gpio_number)}\' wrote.')

    def display(self, number: int, dot: bool = False):
        value = SevenSegment74hc595.DIGITS[number]
        if dot:
            value |= 0b10000000
        self._write_byte(value)
        return self

    def off(self):
        self._write_byte(0)
        return self
