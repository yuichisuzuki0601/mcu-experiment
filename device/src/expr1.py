# xiao で wifi post

import asyncio
import os

from component.tact_switch import TactSwitch
from component.rotary_encoder import RotaryEncoder
from component.esp32c6.board_led import Esp32C6BoardLed
from component.led import Led
from component.oled import Oled
from component.icon import ICONS
from component.buzzer import Buzzer
from component.servo_motor import ServoMotor
from component.wifi import Wifi
from util import timestamp
from util.runner import Runner
from util.storage import Storage

board = os.uname().machine

if board == 'Generic ESP32 module with ESP32':
    tact_switch_gpio_number     = 27
    rotary_encoder_gpio_numbers = None
    led_gpio_number             = 19
    oled_gpio_numbers           = None
    buzzer_gpio_number          = None
    servo_motor_gpio_number     = None
elif board == 'ESP32C6 module with ESP32C6':
    tact_switch_gpio_number     = 20
    rotary_encoder_gpio_numbers = (1, 2)
    esp32c6_board_led           = Esp32C6BoardLed().on()
    led_gpio_number             = 0
    oled_gpio_numbers           = (23, 22)
    buzzer_gpio_number          = 21
    servo_motor_gpio_number     = 16
elif board == 'Raspberry Pi Pico W with RP2040':
    tact_switch_gpio_number     = 20
    rotary_encoder_gpio_numbers = None
    led_gpio_number             = 9
    oled_gpio_numbers           = None
    buzzer_gpio_number          = None
    servo_motor_gpio_number     = None
else:
    raise RuntimeError(f'unknown board: {str(board)}')

storage = Storage()

count = int(storage.get_state('count'))
angle = 0

tact_switch    = TactSwitch(tact_switch_gpio_number)
rotary_encoder = RotaryEncoder(*rotary_encoder_gpio_numbers)
led            = Led(led_gpio_number)
oled           = Oled(*oled_gpio_numbers).write_middle('こんにちは！', scale = 2).emit()
buzzer         = Buzzer(buzzer_gpio_number)
servo_motor    = ServoMotor(servo_motor_gpio_number, angle).set_angle(180)
wifi           = Wifi(storage.get_config('wifi.ssid'), storage.get_config('wifi.password')).connect()

def write_status():
    if wifi and wifi.is_connected():
        return oled.clear().write_icon('wifi', x = Oled.WIDTH - ICONS['wifi'].width)
    else:
        return oled.clear()

async def update_clock():
    (write_status()
    .write_center(timestamp.get_jst_date(), 8 * 3)
    .write_center(timestamp.get_jst_time(), 8 * 4)
    .emit())

update_clock_runner = Runner(update_clock)

def update_oled():
    global count
    if count != 0:
        update_clock_runner.stop()
        write_status().write_middle(f'{str(count)}', scale = 4).emit()
    else:
        update_clock_runner.loop()

def handle_click():
    global count, angle
    led.flash()
    if count == 0:
        return
    if wifi:
        def on_success(status, _, body):
            print(f'{status} {body}')
            async def task():
                global count, angle
                if status == 200:
                    write_status().write_middle(f'{status} OK', scale = 2).emit()
                    # TODO 成功beep音はBuzzerに実装する
                    buzzer.beep(2000, 100)
                else:
                    write_status().write_middle(f'{status}', scale = 2).emit()
                    # TODO 失敗beep音はBuzzerに実装する
                    buzzer.beep(200, 100)
                    await asyncio.sleep_ms(200)
                    buzzer.beep(200, 200)
                    await asyncio.sleep_ms(200)
                count = 1
                storage.set_state('count', str(count))
                angle = 0
                servo_motor.set_angle(angle)
                await asyncio.sleep(1)
                update_oled()
            Runner(task).run()

        def on_error(error):
            print(error)
            write_status().write_middle(f'{error}').emit()
            async def task():
                # TODO 失敗beep音はBuzzerに実装する
                buzzer.beep(200, 100)
                await asyncio.sleep_ms(200)
                buzzer.beep(200, 200)
                await asyncio.sleep(1)
                update_oled()
            Runner(task).run()

        origin = storage.get_config('server.origin')
        wifi.post(
            url = f'{origin}', 
            req_headers = {
                'x-space-code': storage.get_config('space_id')
            }, 
            req_body = {
                'barcode': '4962485101213',
                'count': count
            },
            on_success = on_success,
            on_error = on_error)
    else:
        count = 1
        storage.set_state('count', str(count))
        update_oled()
        buzzer.beep(2000, 100)
        angle = 0
        servo_motor.set_angle(angle)

tact_switch.on_click(handle_click)

def handle_rotate(clockwise: bool):
    global count, angle
    STEP_ANGLE = 30
    if clockwise:
        count += 1
        buzzer.beep(4000, 100)
        if angle != 180:
            angle += STEP_ANGLE
    else:
        if count != 0:
            count -= 1
            buzzer.beep(2000, 100)
        if angle != 0:
            angle -= STEP_ANGLE
    storage.set_state('count', str(count))
    led.flash()
    update_oled()
    servo_motor.set_angle(angle)

rotary_encoder.on_rotate(handle_rotate)

# =====

print("mcu-sample start")
update_oled()

# 実験タスク
async def test_task():
    pass
# Runner(test_task).loop()

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    if esp32c6_board_led != None:
        esp32c6_board_led.off()
    led.off()
    oled.clear().emit()
    buzzer.off()
    servo_motor.set_angle(180)
    print("mcu-sample exit")
