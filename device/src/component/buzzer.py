from machine import Pin, PWM

import asyncio

from util.runner import Runner

class Buzzer:

    def __init__(self, gpio_number: int):
        self.gpio_number = gpio_number
        self.pin = Pin(gpio_number, Pin.OUT)
        self._pwm = PWM(self.pin)
        self._pwm.duty_u16(0)
        self._is_sounding = False

    def on(self, freq: int):
        self._pwm.freq(freq)
        self._pwm.duty_u16(32768)
        self._is_sounding = True
        print(f'Buzzer \'{self.gpio_number}\' sounded {freq} Hz.')
        return self

    def off(self):
        self._pwm.duty_u16(0)
        self._is_sounding = False
        return self

    def beep(self, freq: int, duration_ms: int):
        if self._is_sounding:
            return
        async def coro():
            self.on(freq)
            await asyncio.sleep_ms(duration_ms)
            self.off()
        Runner(coro).run()
        return self
