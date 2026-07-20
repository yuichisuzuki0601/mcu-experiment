# でんたく

import asyncio

from component.tact_switch import TactSwitch
from component.toggle_switch import ToggleSwitch
from component.potention_meter import PotentionMeter
from component.rotary_encoder import RotaryEncoder
from component.pico.board_led import PicoBoardLed
from component.led import Led
from component.oled import Oled
from component.seven_segment import SevenSegment74hc595

from util.runner import Runner

def start(
    tact_switch: TactSwitch,
    toggle_switch: ToggleSwitch,
    potention_meter: PotentionMeter,
    rotary_encoder: RotaryEncoder,
    pico_board_led: PicoBoardLed,
    led_red: Led,
    led_yellow: Led,
    led_blue: Led,
    led_green: Led,
    oled: Oled,
    seven_segment: SevenSegment74hc595,
):
    # COMMON VARIABLES
    message = 'でんたく'
    scale   = 2
    number1 = potention_meter.value()
    number2 = 0
    dot     = toggle_switch.is_on()

    # COMMON METHODS
    def expose_to_leds():
        for bit, led in enumerate((led_green, led_blue, led_yellow, led_red)):
            led.on() if number1 & (1 << bit) else led.off()

    # HANDLERS
    def handle_tact_switch_push():
        result = number1 + number2 if not dot else number1 * number2
        oled.clear().write_middle(str(result), scale).emit()

        async def task():
            await asyncio.sleep(3)
            oled.clear().write_middle(message, scale).emit()

        Runner(task).run()

    def handle_toggle_switch_change(is_on):
        nonlocal dot
        dot = is_on
        seven_segment.display(number2, dot)

        async def task():
            operator = 'たしざん' if not dot else 'かけざん'
            oled.clear().write_middle(operator, scale).emit()
            await asyncio.sleep(1)
            oled.clear().write_middle(message, scale).emit()

        Runner(task).run()

    def handle_potention_meter_change(value):
        nonlocal number1
        number1 = value
        expose_to_leds()

    def handle_rotary_encoder_rotate(clockwise: bool):
        nonlocal number2
        number2 = (number2 - 1 if not clockwise else number2 + 1) % 16
        seven_segment.display(number2, dot)

    # HANDLER ASSIGNS
    tact_switch.on_push(handle_tact_switch_push)
    toggle_switch.on_change(handle_toggle_switch_change)
    potention_meter.on_change(handle_potention_meter_change)
    rotary_encoder.on_rotate(handle_rotary_encoder_rotate)

    # INITIALIZATION
    pico_board_led.on()
    expose_to_leds()
    oled.write_middle(message, scale).emit()
    seven_segment.display(number2, dot)
