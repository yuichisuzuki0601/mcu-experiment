import struct

class WavFile():
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'rb') as file:
            header               = file.read(44)
            self.chunk_id        = header[0:4].decode('ascii')
            self.file_size       = struct.unpack('<I', header[4:8])[0]
            self.format          = header[8:12].decode('ascii')
            self.fmt_id          = header[12:16].decode('ascii')
            self.fmt_size        = struct.unpack('<I', header[16:20])[0]
            self.audio_fmt       = struct.unpack('<H', header[20:22])[0]
            self.num_channels    = struct.unpack('<H', header[22:24])[0]
            self.sample_rate     = struct.unpack('<I', header[24:28])[0]
            self.byte_rate       = struct.unpack('<I', header[28:32])[0]
            self.block_align     = struct.unpack('<H', header[32:34])[0]
            self.bits_per_sample = struct.unpack('<H', header[34:36])[0]
            self.data_id         = header[36:40].decode('ascii')
            self.data_size       = struct.unpack('<I', header[40:44])[0]

    def print_detail(self):
        print(f'file_path       = {self.file_path}')
        print(f'chunk_id        = {self.chunk_id}')
        print(f'file_size       = {self.file_size}')
        print(f'format          = {self.format}')
        print(f'fmt_id          = {self.fmt_id}')
        print(f'fmt_size        = {self.fmt_size}')
        print(f'audio_fmt       = {self.audio_fmt} (1 = PCM)')
        print(f'num_channels    = {self.num_channels}ch')
        print(f'sample_rate     = {self.sample_rate}Hz')
        print(f'byte_rate       = {self.byte_rate}')
        print(f'block_align     = {self.block_align}')
        print(f'bits_per_sample = {self.bits_per_sample}bit')
        print(f'data_id         = {self.data_id}')
        print(f'data_size       = {self.data_size}')
        return self
