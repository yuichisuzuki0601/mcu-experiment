from array import array
from machine import Pin, I2S

from util.audio_file import WaveFile

class AudioAmpMax98753a():
    MAX_VOLUME       = 100
    READ_BUFFER_SIZE = 1024 # ファイルから一度に読むバイト数
    I2S_BUFFER_SIZE  = 4096 # I2S 内部リングバッファサイズ 兼 終了時の無音書き込みサイズ

    def __init__(self, lrc_gpio_number: int, bclk_gpio_number: int, din_gpio_number: int):
        self.lrc_gpio_number  = lrc_gpio_number
        self.bclk_gpio_number = bclk_gpio_number
        self.din_gpio_number  = din_gpio_number
        self._sck_pin         = Pin(bclk_gpio_number)
        self._ws_pin          = Pin(lrc_gpio_number)
        self._sd_pin          = Pin(din_gpio_number)

    def play(self, wave_file: WaveFile, volume: int = MAX_VOLUME // 2):
        volume = max(0, min(AudioAmpMax98753a.MAX_VOLUME, volume))
        audio = I2S(
            0,
            sck    = self._sck_pin,
            ws     = self._ws_pin,
            sd     = self._sd_pin,
            mode   = I2S.TX,
            bits   = wave_file.bits_per_sample,
            format = I2S.STEREO if wave_file.num_channels == 2 else I2S.MONO,
            rate   = wave_file.sample_rate,
            ibuf   = AudioAmpMax98753a.I2S_BUFFER_SIZE,
        )
        with wave_file:
            buffer = bytearray(AudioAmpMax98753a.READ_BUFFER_SIZE)
            while True:
                read_size = wave_file.readinto(buffer)
                if not read_size:
                    break
                read_size -= read_size % 2 # ほぼ発生しないはずだがファイル末尾で奇数のデータがあった場合に無視する
                samples = array('h', buffer[:read_size])
                for i in range(len(samples)):
                    samples[i] = samples[i] * volume // AudioAmpMax98753a.MAX_VOLUME # 音量調節
                audio.write(samples)
        audio.write(bytearray(AudioAmpMax98753a.I2S_BUFFER_SIZE)) # 無音を書き込んでクリップ音防止
        print(f'AudioAmpMax98753a \'{(self.lrc_gpio_number, self.bclk_gpio_number, self.din_gpio_number)}\' played.')
