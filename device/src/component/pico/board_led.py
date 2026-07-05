from component.led import Led

class PicoBoardLed(Led):

    def __init__(self):
        super().__init__('LED')
