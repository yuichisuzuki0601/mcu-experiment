# xiao で スライム

import asyncio

from component.esp32c6.board_led import Esp32C6BoardLed
from component.oled import Oled
from component.icon import ICONS
from component.buzzer import Buzzer
from component.servo_motor import ServoMotor
from util.storage import Storage

oled_gpio_numbers       = (23, 22)
buzzer_gpio_number      = 21
servo_motor_gpio_number = 16

storage = Storage()

count = int(storage.get_state('count'))
angle = 0

esp32c6_board_led = Esp32C6BoardLed().on()
oled              = Oled(*oled_gpio_numbers).write_middle('こんにちは！', scale = 2).emit()
buzzer            = Buzzer(buzzer_gpio_number)
servo_motor       = ServoMotor(servo_motor_gpio_number, angle).set_angle(180)

# =====

print("mcu-sample start")

servo_motor.set_angle(0)
text = 'なんと スライムが おきあがり なかまに なりたそうに こちらをみている！ なかまにしてあげますか？     いいえ     スライムは さびしそうに さっていった！'
scale = 4

async def handle_marquee_end():
    s_x = Oled.WIDTH  // 2 - ICONS['slime'].width  // 2 * scale
    s_y = Oled.HEIGHT // 2 - ICONS['slime'].height // 2 * scale
    oled.clear().write_icon('slime', s_x, s_y, scale).emit()
    # TODO 失敗beep音はBuzzerに実装する
    buzzer.beep(200, 100)
    await asyncio.sleep_ms(200)
    buzzer.beep(200, 200)
    await asyncio.sleep_ms(800)
    servo_motor.set_angle(180)
    await asyncio.sleep(10)
    servo_motor.set_angle(0)

oled.marquee(text, scale, handle_marquee_end)

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    if esp32c6_board_led != None:
        esp32c6_board_led.off()
    oled.clear().emit()
    buzzer.off()
    servo_motor.set_angle(180)
    print("mcu-sample exit")
