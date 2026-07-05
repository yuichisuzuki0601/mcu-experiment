from machine import Pin, PWM

class ServoMotor:
    FREQ   = 50    #[Hz]
    MIN_US = 500   #[μs]
    MAX_US = 2_500 #[μs]

    def __init__(self, gpio_number: int, default_angle: float = 0, reverse: bool = False):
        self.gpio_number = gpio_number
        self.reverse = reverse
        self._pwm = PWM(Pin(gpio_number, Pin.OUT))
        self._pwm.freq(ServoMotor.FREQ)
        self._pwm.duty_u16(0)
        self.set_angle(default_angle)

    def set_angle(self, angle: float):
        real_angle = round(angle * 2) / 2
        real_angle = max(0, min(180, real_angle))
        if not self.reverse:
            real_angle = 180 - real_angle
        target_us = ServoMotor.MIN_US + (real_angle / 180) * (ServoMotor.MAX_US - ServoMotor.MIN_US)
        self._pwm.duty_u16(65535 * round(target_us) // (1_000_000 // ServoMotor.FREQ))
        print(f'ServoMotor \'{self.gpio_number}\' moved to {angle} degrees.')
        return self
