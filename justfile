BACKEND_DIR := 'backend'
DEVICE_DIR := 'device'
USB_PORT := `ls /dev/cu.usb* /dev/cu.SLAB_USBtoUART 2>/dev/null | head -n 1`
MISAKI_FONT_PATH := 'https://raw.githubusercontent.com/Tamakichi/pico_MicroPython_misakifont/master/misakifont'

_default:
    @just --list --unsorted

# esp32のファームウェアを削除します
[group('firmware')]
firmware-nuke-esp32:
    #!/bin/sh
    esptool --port {{ USB_PORT }} erase-flash

# esp32へファームウェアを書き込みます
[group('firmware')]
firmware-flash-esp32:
    #!/bin/sh
    esptool --chip esp32 --port {{ USB_PORT }} --baud 921600 write-flash -z 0x1000 {{ DEVICE_DIR }}/firmware/ESP32_GENERIC-20260406-v1.28.0.bin

# esp32c6へファームウェアを書き込みます
[group('firmware')]
firmware-flash-esp32c6:
    #!/bin/sh
    esptool --chip esp32c6 --port {{ USB_PORT }} --baud 460800 --before default-reset --after hard-reset write-flash --flash-mode dio --flash-size detect --flash-freq 80m 0x0 {{ DEVICE_DIR }}/firmware/ESP32C6_MicroPython.bin

# TODO picoの初期化も

# backendを起動します
[group('backend')]
backend-start:
    #!/bin/sh
    cd {{ BACKEND_DIR }}
    ./mvnw spring-boot:run

# deviceに必要なライブラリをインストールします
[group('device')]
device-install-lib:
    #!/bin/sh
    cd {{ DEVICE_DIR }}
    rm -rf ./src/lib
    mpremote mip install aiohttp ssd1306
    mpremote cp -r :lib ./src/lib
    mkdir -p ./src/lib/font/misakifont
    curl -L {{ MISAKI_FONT_PATH }}/__init__.py       -o ./src/lib/font/misakifont/__init__.py
    curl -L {{ MISAKI_FONT_PATH }}/misakifont.py     -o ./src/lib/font/misakifont/misakifont.py
    curl -L {{ MISAKI_FONT_PATH }}/misakifontdata.py -o ./src/lib/font/misakifont/misakifontdata.py
    curl -L {{ MISAKI_FONT_PATH }}/tma_jp_utl.py     -o ./src/lib/font/misakifont/tma_jp_utl.py

# deviceのファイルを一覧します
[group('device')]
device-ls dir=':':
    #!/bin/sh
    mpremote ls {{ dir }}

# deviceから全てのファイルを削除します
[group('device')]
device-delete-all:
    #!/bin/sh
    mpremote rm -r :

# deviceにソースを適用してプログラムを実行します
[group('device')]
device-start:
    #!/bin/sh
    # いちいち全消ししなくてもファイルが残っても動作に支障ないのでアップロード速度を優先する
    # mpremote ls : | awk '$NF != ".storage" && $NF != "" {print $NF}' | while read -r item; do
    #   mpremote rm -r :/$item
    # done
    if ! mpremote ls : | grep -q "\.storage"; then
      mpremote cp {{ DEVICE_DIR }}/.storage :.
    fi
    mpremote cp -r {{ DEVICE_DIR }}/src/. :.
    mpremote exec --no-follow 'import main' && mpremote repl
