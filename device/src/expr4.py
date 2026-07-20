import asyncio

from component.tact_switch     import TactSwitch
from component.toggle_switch   import ToggleSwitch
from component.potention_meter import PotentionMeter
from component.rotary_encoder  import RotaryEncoder
from component.pico.board_led  import PicoBoardLed
from component.led             import Led
from component.oled            import Oled
from component.seven_segment   import SevenSegment74hc595

from util.runner import Runner

# INPUT
tact_switch     = TactSwitch(28)
toggle_switch   = ToggleSwitch(0)
potention_meter = PotentionMeter(26)
rotary_encoder  = RotaryEncoder(17, 16)

# OUTPUT
pico_board_led  = PicoBoardLed().on()
led_red         = Led(19)
led_yellow      = Led(20)
led_blue        = Led(21)
led_green       = Led(22)
oled            = Oled(5, 4)
seven_segment   = SevenSegment74hc595(3, 2, 6)

# GLOBAL VARIABLES
message = 'でんたく'
scale   = 2
number  = 0
dot     = toggle_switch.is_on()

# =====

def handle_tact_switch_push():
    result = potention_meter.value() + number if not dot else potention_meter.value() * number
    oled.clear().write_middle(str(result), scale).emit()
    async def task():
        await asyncio.sleep(3)
        oled.clear().write_middle(message, scale).emit()
    Runner(task).run()

tact_switch.on_push(handle_tact_switch_push)

def handle_toggle_switch_change(is_on):
    global dot
    dot = is_on
    seven_segment.show(number, dot)
    async def task():
        operator = '+' if not dot else 'x'
        oled.clear().write_middle(operator, scale).emit()
        await asyncio.sleep(3)
        oled.clear().write_middle(message, scale).emit()
    Runner(task).run()

toggle_switch.on_change(handle_toggle_switch_change)

def handle_potention_meter_change(value):
    for bit, led in enumerate((led_green, led_blue, led_yellow, led_red)):
        led.on() if value & (1 << bit) else led.off()

potention_meter.on_change(handle_potention_meter_change)

def handle_rotary_encoder_rotate(clockwise: bool):
    global number
    number = (number - 1 if not clockwise else number + 1) % 16
    seven_segment.show(number, dot)

rotary_encoder.on_rotate(handle_rotary_encoder_rotate)

# =====

print("mcu-sample start")

oled.write_middle(message, scale).emit()
seven_segment.show(number, dot)

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    pico_board_led.off()
    led_red.off()
    led_yellow.off()
    led_blue.off()
    led_green.off()
    oled.clear().emit()
    seven_segment.off()
    print("mcu-sample exit")
