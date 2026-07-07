# Raspberry Pi Pico W で MAX98357A

import asyncio

from component.tact_switch import TactSwitch
from component.pico.board_led import PicoBoardLed
from component.led import Led
from component.audio_amp import Max98753a
from util.audio_file import WaveFile

tact_switch_gpio_number = 20
led_gpio_number         = 1
audio_amp_gpio_numbers  = (3, 2, 4)

pico_board_led = PicoBoardLed().on()
tact_switch    = TactSwitch(tact_switch_gpio_number)
led            = Led(led_gpio_number)
audio_amp      = Max98753a(*audio_amp_gpio_numbers)

wav_file_coin = WaveFile('mario-coin.wav').print_detail()
wav_file_pipe = WaveFile('mario-pipe.wav').print_detail()

bool = False

def handle_click():
    global bool
    led.flash()
    if not bool:
        audio_amp.play(wav_file_coin, 5)
    else:
        audio_amp.play(wav_file_pipe, 5)
    bool = not bool

tact_switch.on_click(handle_click)

# =====

print("mcu-sample start")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    led.off()
    pico_board_led.off()
    print("mcu-sample exit")
