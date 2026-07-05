from array import array
from machine import Pin, I2S

from util.audio_file import WavFile

class Max98753a():
    VOLUME_LEVEL      = 1    # 1(小) 〜 10(大)
    READ_BUFFER_SIZE  = 1024 # ファイルから一度に読むバイト数
    I2S_BUFFER_SIZE   = 4096 # I2S 内部リングバッファ（兼、終了時の無音書き込みサイズ）

    def __init__(self, lrc_gpio_number: int, bclk_gpio_number: int, din_gpio_number: int):
        self.lrc_gpio_number  = lrc_gpio_number
        self.bclk_gpio_number = bclk_gpio_number
        self.din_gpio_number  = din_gpio_number
        self._sck_pin         = Pin(bclk_gpio_number)
        self._ws_pin          = Pin(lrc_gpio_number)
        self._sd_pin          = Pin(din_gpio_number)

    def sound(self, wav_file: WavFile):
        audio = I2S(
            0,
            sck    = self._sck_pin,
            ws     = self._ws_pin,
            sd     = self._sd_pin,
            mode   = I2S.TX,
            bits   = wav_file.bits_per_sample,
            format = I2S.STEREO if wav_file.num_channels == 2 else I2S.MONO,
            rate   = wav_file.sample_rate,
            ibuf   = Max98753a.I2S_BUFFER_SIZE,
        )
        with open(wav_file.file_path, 'rb') as file:
            file.seek(44)
            buffer = bytearray(Max98753a.READ_BUFFER_SIZE)
            remaining_size = wav_file.data_size
            while remaining_size > 0:
                read_size = file.readinto(buffer, min(Max98753a.READ_BUFFER_SIZE, remaining_size))
                if read_size == 0:
                    break
                remaining_size -= read_size
                read_size -= read_size % 2
                audio.write(array('h', buffer[:read_size]))
        audio.write(bytearray(Max98753a.I2S_BUFFER_SIZE))
