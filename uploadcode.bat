esptool --port COM4 erase_flash

esptool --port COM4 --baud 460800 write_flash 0 ESP32_GENERIC_S3-20250911-v1.26.1.bin

ampy --port COM4 put SRC/carro.py


