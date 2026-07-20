# Raspberry Pi Pico W で 74HC595, MAX98357A

import asyncio

from component.tact_switch import TactSwitch
from component.potention_meter import PotentionMeter
from component.pico.board_led import PicoBoardLed
from component.led import Led
from component.seven_segment import SevenSegment74hc595
from component.audio_amp import AudioAmpMax98753a
from util.audio_file import WaveFile

tact_switch_gpio_number     = 16
potention_meter_gpio_number = 26
led_gpio_number             = 1
seven_segment_gpio_numbers  = (6, 7, 8)
audio_amp_gpio_numbers      = (5, 4, 3)

pico_board_led  = PicoBoardLed().on()
tact_switch     = TactSwitch(tact_switch_gpio_number)
led             = Led(led_gpio_number)
seven_segment   = SevenSegment74hc595(*seven_segment_gpio_numbers)
audio_amp       = AudioAmpMax98753a(*audio_amp_gpio_numbers)
potention_meter = PotentionMeter(potention_meter_gpio_number)

wav_file_coin = WaveFile('wav/mario-coin.wav').print_detail()
wav_file_pipe = WaveFile('wav/mario-pipe.wav').print_detail()

number = 0

def handle_click():
    global number
    led.flash()
    number = (number + 1) % 16
    
    audio_amp.play(wav_file_coin, 50)

tact_switch.on_push(handle_click)

def handle_read(v):
    seven_segment.show(v, True)

potention_meter.on_change(handle_read)

seven_segment.show(number)

# =====

print("mcu-sample start")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    seven_segment.off()
    led.off()
    pico_board_led.off()
    print("mcu-sample exit")
