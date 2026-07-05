# Raspberry Pi Pico W で MAX98357A

import asyncio

from component.tact_switch import TactSwitch
from component.pico.board_led import PicoBoardLed
from component.led import Led
from component.audio_amp import Max98753a
from util.audio_file import WavFile

tact_switch_gpio_number = 20
led_gpio_number         = 1
audio_amp_gpio_numbers = (3, 2, 4)

pico_board_led = PicoBoardLed().on()
tact_switch    = TactSwitch(tact_switch_gpio_number)
led            = Led(led_gpio_number)
audio_amp      = Max98753a(*audio_amp_gpio_numbers)

wav_file_path = "sound-mono-data.wav"
#wav_file_path = "sound-stereo-data.wav"
#wav_file_path = "sound-neko.wav"

wav_file = WavFile(wav_file_path).print_detail()

def handle_click():
    led.flash()
    audio_amp.sound(wav_file)

tact_switch.on_click(handle_click)

# =====

print("mcu-sample start")
# 起動時に1回デモ再生
audio_amp.sound(wav_file)

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    led.off()
    pico_board_led.off()
    print("mcu-sample exit")
