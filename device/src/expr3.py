# Raspberry Pi Pico W で MAX98357A

import asyncio

from component.tact_switch import TactSwitch
from component.led import Led

tact_switch_gpio_number = 20
led_gpio_number         = 9

tact_switch = TactSwitch(tact_switch_gpio_number)
led         = Led(led_gpio_number)

def handle_click():
    global count, angle
    led.flash()

tact_switch.on_click(handle_click)

# =====

print("mcu-sample start")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    led.off()
    print("mcu-sample exit")
