from array import array
from machine import Pin, I2S

from util.audio_file import WaveFile

class Max98753a():
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

    def play(self, wav_file: WaveFile, volume: int = MAX_VOLUME // 2):
        volume = max(0, min(Max98753a.MAX_VOLUME, volume))
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
                read_size -= read_size % 2 # ほぼ発生しないはずだがファイル末尾で奇数のデータがあった場合に無視する
                samples = array('h', buffer[:read_size])
                for i in range(len(samples)):
                    samples[i] = samples[i] * volume // Max98753a.MAX_VOLUME # 音量調節
                audio.write(samples)
        audio.write(bytearray(Max98753a.I2S_BUFFER_SIZE)) # 無音を書き込んでクリップ音防止
