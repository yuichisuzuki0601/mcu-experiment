from machine import Pin

from util.runner import Runner

class RotaryEncoder:

    def __init__(self, gpio_number_a: int, gpio_number_b: int):
        self.gpio_number_a = gpio_number_a
        self.gpio_number_b = gpio_number_b
        self.pin_a = Pin(gpio_number_a, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(gpio_number_b, Pin.IN, Pin.PULL_UP)
        self._last_state = (self.pin_a.value(), self.pin_b.value())
        self._callback = None
        Runner(self._task).loop()

    def on_rotate(self, callback):
        self._callback = callback
        return self

    async def _task(self):
        current_state = (self.pin_a.value(), self.pin_b.value())
        if current_state != self._last_state:
            clockwise = None
            if current_state == (0, 0):
                if self._last_state == (0, 1):
                    clockwise = True
                if self._last_state == (1, 0):
                    clockwise = False
            elif current_state == (1, 1):
                if self._last_state == (1, 0):
                    clockwise = True
                if self._last_state == (0, 1):
                    clockwise = False
            self._last_state = current_state
            if clockwise != None:
                print(f'RotaryEncoder \'{(self.gpio_number_a, self.gpio_number_b)}\' rotated {'CW' if clockwise else 'CCW'}.')
                if self._callback:
                    self._callback(clockwise)
