import bluetooth
import machine
from machine import Pin, PWM
import time

PIN_PWM_M1 = 4
print("\n--- Problem 3: Average of numbers with while and sentinel ---")
SENTINEL_VALUE = -1.0
total_sum = 0.0
count = 0

while True:
	number_text = input("Enter a number or -1 to finish: ").strip()
	try:
		number = float(number_text)
	except ValueError:
		print("Error: invalid input")
		continue
	if number == SENTINEL_VALUE:
		break
	total_sum += number
	count += 1

if count == 0:
	print("Error: no data")
else:
	average_value = total_sum / count
	print(f"Count: {count}")
	print(f"Average: {average_value}")


PIN_PWM_M2 = 5
PIN_PWM_M3 = 6
PIN_PWM_M4 = 7

PIN_M1_IN1 = 15
PIN_M1_IN2 = 16
PIN_M2_IN3 = 17
PIN_M2_IN4 = 18

PIN_M3_IN1 = 8
PIN_M3_IN2 = 10
PIN_M4_IN3 = 11
PIN_M4_IN4 = 12

PWM_FREQ = 1000

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")


class BLEUART:
    def __init__(self, name="ESP32-S3-Carro"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((
            (_UART_UUID, ((_UART_TX, bluetooth.FLAG_NOTIFY),
                          (_UART_RX, bluetooth.FLAG_WRITE),)),
        ))
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        self._advertise(name)

    def _irq(self, event, data):
        if event == 1:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("S3 Bluetooth: Dispositivo Conectado")
        elif event == 2:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("S3 Bluetooth: Desconectado")
            self._advertise()
        elif event == 3:
            conn_handle, value_handle = data
            if value_handle == self._handle_rx:
                received = self._ble.gatts_read(self._handle_rx)
                if self._handler:
                    self._handler(received)

    def _advertise(self, name="ESP32-S3-Carro"):
        name = bytes(name, 'UTF-8')
        payload = bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self._ble.gap_advertise(100, payload)

    def set_rx_handler(self, handler):
        self._handler = handler

    def send(self, data):
        for conn_handle in self._connections:
            try:
                self._ble.gatts_notify(conn_handle, self._handle_tx, data)
            except:
                pass

class Motor:
    def __init__(self, pin_in1, pin_in2, pin_pwm):
        self.in1 = Pin(pin_in1, Pin.OUT)
        self.in2 = Pin(pin_in2, Pin.OUT)
        self.pwm = PWM(Pin(pin_pwm), freq=PWM_FREQ)
        self.pwm.duty_u16(0)

    def mover(self, velocidad):
        """
        velocidad: Valor entre -255 (atrás max) y 255 (adelante max).
        """
        duty = int(abs(velocidad) * 65535 / 255)

        if duty > 65535:
            duty = 65535

        self.pwm.duty_u16(duty)

        if velocidad > 0:
            self.in1.value(1)
            self.in2.value(0)
        elif velocidad < 0:
            self.in1.value(0)
            self.in2.value(1)
        else:
            self.stop()

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.duty_u16(0)

motor_m1 = Motor(PIN_M1_IN1, PIN_M1_IN2, PIN_PWM_M1)
motor_m2 = Motor(PIN_M2_IN3, PIN_M2_IN4, PIN_PWM_M2)
motor_m3 = Motor(PIN_M3_IN1, PIN_M3_IN2, PIN_PWM_M3)
motor_m4 = Motor(PIN_M4_IN3, PIN_M4_IN4, PIN_PWM_M4)

velocidad_actual = 150


def procesar_comando(data_bytes):
    global velocidad_actual

    try:
        texto = data_bytes.decode('utf-8').strip().upper()
        print("Cmd:", texto)
    except:
        return

    if not texto:
        return

    if texto == 'F':
        motor_m1.mover(velocidad_actual)
        motor_m2.mover(velocidad_actual)
        motor_m3.mover(velocidad_actual)
        motor_m4.mover(velocidad_actual)

    elif texto == 'B':
        motor_m1.mover(-velocidad_actual)
        motor_m2.mover(-velocidad_actual)
        motor_m3.mover(-velocidad_actual)
        motor_m4.mover(-velocidad_actual)

    elif texto == 'L':
        motor_m1.mover(-velocidad_actual)
        motor_m3.mover(-velocidad_actual)
        motor_m2.mover(velocidad_actual)
        motor_m4.mover(velocidad_actual)

    elif texto == 'R':
        motor_m1.mover(velocidad_actual)
        motor_m3.mover(velocidad_actual)
        motor_m2.mover(-velocidad_actual)
        motor_m4.mover(-velocidad_actual)

    elif texto == 'S':
        motor_m1.stop()
        motor_m2.stop()
        motor_m3.stop()
        motor_m4.stop()

    elif texto.startswith('V'):
        try:
            val_str = texto[1:]
            nueva_vel = int(val_str)
            if 0 <= nueva_vel <= 255:
                velocidad_actual = nueva_vel
                print(f"Velocidad: {velocidad_actual}")
        except:
            pass


print("Iniciando Carro Robot ESP32-S3...")
ble = BLEUART(name="ESP32-S3-Carro")
ble.set_rx_handler(procesar_comando)

while True:
    time.sleep_ms(100)