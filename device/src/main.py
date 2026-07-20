import asyncio

from component.tact_switch     import TactSwitch
from component.toggle_switch   import ToggleSwitch
from component.potention_meter import PotentionMeter
from component.rotary_encoder  import RotaryEncoder
from component.pico.board_led  import PicoBoardLed
from component.led             import Led
from component.oled            import Oled
from component.seven_segment   import SevenSegment74hc595

EXPR_NUMBER = '01'

# INPUT
tact_switch     = TactSwitch(28)
toggle_switch   = ToggleSwitch(0)
potention_meter = PotentionMeter(26)
rotary_encoder  = RotaryEncoder(17, 16)

# OUTPUT
pico_board_led  = PicoBoardLed()
led_red         = Led(19)
led_yellow      = Led(20)
led_blue        = Led(21)
led_green       = Led(22)
oled            = Oled(5, 4)
seven_segment   = SevenSegment74hc595(3, 2, 6)

__import__(f'expr{EXPR_NUMBER}').start(
    tact_switch     = tact_switch,
    toggle_switch   = toggle_switch,
    potention_meter = potention_meter,
    rotary_encoder  = rotary_encoder,
    pico_board_led  = pico_board_led,
    led_red         = led_red,
    led_yellow      = led_yellow,
    led_blue        = led_blue,
    led_green       = led_green,
    oled            = oled,
    seven_segment   = seven_segment,
)

print('mcu-experiment start.')
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
    print('mcu-experiment end.')
