from machine import Pin, ADC

from util.runner import Runner

class PotentionMeter():

    def __init__(self, gpio_number: int, resolution: int = 16):
        self.gpio_number = gpio_number
        self.pin = Pin(gpio_number)
        self.adc = ADC(self.pin)
        self.resolution = resolution
        self._last_value = self.value()
        self._callback = None
        Runner(self._task).loop()

    def value(self):
        current_value = self.adc.read_u16() * self.resolution // 65536
        current_value = min(current_value, self.resolution - 1)
        return current_value

    def on_change(self, callback):
        self._callback = callback
        return self

    async def _task(self):
        current_value = self.value()
        if current_value != self._last_value:
            print(f'PotentionMeter \'{self.gpio_number}\' changed {self._last_value} to {current_value}. ')
            self._last_value = current_value
            if self._callback:
                self._callback(current_value)
