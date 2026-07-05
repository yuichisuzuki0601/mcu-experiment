# Raspberry Pi Pico W で MAX98357A

import asyncio

from component.tact_switch import TactSwitch
from component.pico.board_led import PicoBoardLed
from component.led import Led

from machine import Pin, I2S
import struct
from array import array

tact_switch_gpio_number = 20
led_gpio_number         = 1

pico_board_led = PicoBoardLed().on()
tact_switch    = TactSwitch(tact_switch_gpio_number)
led            = Led(led_gpio_number)

sck_pin     = Pin(2)   # BCLK
ws_pin      = Pin(3)   # LRC
sd_pin      = Pin(4)   # DIN
sd_mode_pin = Pin(5, Pin.OUT, value=1)  # MAX98357A SD (HIGH=active)

audio = I2S(
    0,
    sck = sck_pin,
    ws = ws_pin,
    sd = sd_pin,
    mode = I2S.TX,
    bits = 16,
    format = I2S.MONO,
    rate = 44100,
    ibuf = 20000,
)

VOLUME_LEVEL = 2 # 1(小) 〜 10(大)
wav_file = "sound-001.wav"
#wav_file = "sound-neko.wav"

def sound():
    sd_mode_pin.on()
    audio.write(bytearray(512))

    with open(wav_file, "rb") as f:
        f.read(12)

        channels = 2
        data_size = 0

        while True:
            chunk_id = f.read(4)
            if len(chunk_id) < 4:
                break
            chunk_size = struct.unpack('<I', f.read(4))[0]

            if chunk_id == b'fmt ':
                fmt = f.read(16)
                channels = struct.unpack('<H', fmt[2:4])[0]
                remain = chunk_size - 16
                if remain > 0:
                    f.read(remain)
            elif chunk_id == b'data':
                data_size = chunk_size
                break
            else:
                f.read(chunk_size)
                if chunk_size % 2:
                    f.read(1)

        scale = VOLUME_LEVEL * 256 // 10
        buffer = bytearray(512)

        while data_size > 0:
            to_read = min(512, data_size)
            num_read = f.readinto(buffer, to_read)
            if num_read == 0:
                break
            data_size -= num_read

            if channels == 2:
                num_read -= num_read % 4
                a = array('h', buffer[:num_read])
                n = len(a)
                j = 0
                for i in range(0, n, 2):
                    s = (a[i] * scale) // 256
                    if s < -32768: s = -32768
                    if s > 32767: s = 32767
                    a[j] = s
                    j += 1
                audio.write(a[:j])
            else:
                num_read -= num_read % 2
                a = array('h', buffer[:num_read])
                for i in range(len(a)):
                    s = (a[i] * scale) // 256
                    if s < -32768: s = -32768
                    if s > 32767: s = 32767
                    a[i] = s
                audio.write(a)

    audio.write(bytearray(4096))
    sd_mode_pin.off()

def handle_click():
    led.flash()
    sound()

tact_switch.on_click(handle_click)

# =====

print("mcu-sample start")
# 起動時に1回デモ再生
sound()

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    sd_mode_pin.off()
    audio.deinit()
    led.off()
    pico_board_led.off()
    print("mcu-sample exit")
