from component.led import Led

class Esp32C6BoardLed(Led):

    def __init__(self):
        super().__init__(15)

    def on(self):
        print(f'Led \'esp32c6 board led\' emitted.')
        super().off()
        return self

    def off(self):
        super().on()
        return self
