# でんたく

import asyncio

from util.runner import Runner

def start(
    tact_switch,
    toggle_switch,
    potention_meter,
    rotary_encoder,
    pico_board_led,
    led_red,
    led_yellow,
    led_blue,
    led_green,
    oled,
    seven_segment,
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
        seven_segment.show(number2, dot)

        async def task():
            operator = '+' if not dot else 'x'
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
        seven_segment.show(number2, dot)

    # HANDLER ASSIGNS
    tact_switch.on_push(handle_tact_switch_push)
    toggle_switch.on_change(handle_toggle_switch_change)
    potention_meter.on_change(handle_potention_meter_change)
    rotary_encoder.on_rotate(handle_rotary_encoder_rotate)

    # INITIALIZATION
    pico_board_led.on()
    expose_to_leds()
    oled.write_middle(message, scale).emit()
    seven_segment.show(number2, dot)
