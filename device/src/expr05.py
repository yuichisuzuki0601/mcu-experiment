# スライム(一部)

from component.pico.board_led import PicoBoardLed
from component.oled import Oled

def start(
    tact_switch,
    toggle_switch,
    potention_meter,
    rotary_encoder,
    pico_board_led: PicoBoardLed,
    led_red,
    led_yellow,
    led_blue,
    led_green,
    oled: Oled,
    seven_segment,
):
    text = 'なんと スライムが おきあがり なかまに なりたそうに こちらをみている！ なかまにしてあげますか？     いいえ     スライムは さびしそうに さっていった！'
    scale = 2

    # INITIALIZATION
    pico_board_led.on()
    oled.marquee(text, scale)
