from machine import Pin
import time

p48 = Pin(48, Pin.OUT)


while True:
    p48.value(1)
    time.sleep(1)
    p48.value(0)
    time.sleep(1)