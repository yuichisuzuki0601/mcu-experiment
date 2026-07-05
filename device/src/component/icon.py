class Icon:

    def __init__(self, data):
        self.data = data

    @property
    def size(self):
        return (len(bin(max(self.data))) - 2, len(self.data))

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

ICONS = {
    'slime': Icon((
        0b0000000100000000,
        0b0000001010000000,
        0b0000001010000000,
        0b0000001010000000,
        0b0000010001000000,
        0b0001100000110000,
        0b0010000000001000,
        0b0100000000000100,
        0b1000010001000010,
        0b1000101010100010,
        0b1000010001000010,
        0b1000100000100010,
        0b0100011111000100,
        0b0011000000011000,
        0b0000111111100000,
        0b0000000000000000
    )),
    'wifi': Icon((
        0x007f80,
        0x01ffe0,
        0x07fff8,
        0x0fc0fc,
        0x1f003e,
        0x3c3f0f,
        0x38ffc7,
        0x11ffe2,
        0x03e1f0,
        0x078078,
        0x071e38,
        0x023f10,
        0x007f80,
        0x00f3c0,
        0x006180,
        0x000c00,
        0x001e00,
        0x001e00,
        0x000c00,
    ))
}
