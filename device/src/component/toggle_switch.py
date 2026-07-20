from machine import Pin

from util.runner import Runner

class ToggleSwitch:
    OFF_VALUE = 1
    ON_VALUE  = 0

    def __init__(self, gpio_number: int):
        self.gpio_number = gpio_number
        self.pin = Pin(gpio_number, Pin.IN, Pin.PULL_UP)
        self._last_value = self.value()
        self._callback = None
        Runner(self._task).loop()

    def value(self):
        return self.pin.value()

    def is_on(self):
        return self.value() == ToggleSwitch.ON_VALUE

    def on_change(self, callback):
        self._callback = callback
        return self

    async def _task(self):
        current_value = self.value()
        if current_value != self._last_value:
            is_on = self.is_on()
            print(f'ToggleSwitch \'{self.gpio_number}\' changed to {is_on}.')
            self._last_value = current_value
            if self._callback:
                self._callback(is_on)
