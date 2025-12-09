import bluetooth
import machine
from machine import Pin, PWM
import time


PIN_TRACCION_A = 15
PIN_TRACCION_B = 16


PIN_DIRECCION_A = 17
PIN_DIRECCION_B = 18


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
        if event == 1: # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Bluetooth: Dispositivo Conectado")
        elif event == 2: # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("Bluetooth: Desconectado")
            self._advertise()
        elif event == 3: # _IRQ_GATTS_WRITE
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
    """
    Controla un motor DC usando 2 pines en modo PWM.
    Esto ahorra el uso de un pin 'Enable' extra.
    """
    def __init__(self, pin_a, pin_b):
        # Inicializamos ambos pines como PWM
        self.pwm_a = PWM(Pin(pin_a), freq=PWM_FREQ)
        self.pwm_b = PWM(Pin(pin_b), freq=PWM_FREQ)
        self.stop()

    def mover(self, velocidad):
        """
        velocidad: Valor entre -255 (atrás) y 255 (adelante).
        """
        velocidad = max(min(velocidad, 255), -255) # Limitar rango
        
        # Convertir escala 0-255 a 0-65535 (u16 de MicroPython)
        duty = int(abs(velocidad) * 65535 / 255)

        if velocidad > 0:
            # Adelante: Pin A con PWM, Pin B en 0
            self.pwm_a.duty_u16(duty)
            self.pwm_b.duty_u16(0)
        elif velocidad < 0:
            # Atrás: Pin A en 0, Pin B con PWM
            self.pwm_a.duty_u16(0)
            self.pwm_b.duty_u16(duty)
        else:
            self.stop()

    def stop(self):
        self.pwm_a.duty_u16(0)
        self.pwm_b.duty_u16(0)




motor_traccion = Motor(PIN_TRACCION_A, PIN_TRACCION_B)


motor_direccion = Motor(PIN_DIRECCION_A, PIN_DIRECCION_B)


velocidad_traccion_val = 200  
velocidad_giro_val = 255      

def procesar_comando(data_bytes):
    global velocidad_traccion_val, velocidad_giro_val

    try:
        texto = data_bytes.decode('utf-8').strip().upper()

    except:
        return

    if not texto:
        return


    
    # AVANZAR
    if texto == 'F':
        motor_traccion.mover(velocidad_traccion_val)
        motor_direccion.stop() 

    # RETROCEDER
    elif texto == 'B':
        motor_traccion.mover(-velocidad_traccion_val)
        motor_direccion.stop()

    # IZQUIERDA
    elif texto == 'L':
        motor_direccion.mover(velocidad_giro_val)


    # DERECHA
    elif texto == 'R':
        motor_direccion.mover(-velocidad_giro_val)

    # DETENER TODO
    elif texto == 'S':
        motor_traccion.stop()
        motor_direccion.stop()
        

    
    elif texto == 'G': 
        motor_traccion.mover(velocidad_traccion_val)
        motor_direccion.mover(velocidad_giro_val)
        
    elif texto == 'I': 
        motor_traccion.mover(velocidad_traccion_val)
        motor_direccion.mover(-velocidad_giro_val)
        
    elif texto == 'H': 
        motor_traccion.mover(-velocidad_traccion_val)
        motor_direccion.mover(velocidad_giro_val)
        
    elif texto == 'J': 
        motor_traccion.mover(-velocidad_traccion_val)
        motor_direccion.mover(-velocidad_giro_val)

    elif texto.startswith('V') or texto.startswith('v'):
        try:
            val_str = texto[1:]
            nueva_vel = int(val_str)
            if 0 <= nueva_vel <= 255:
                velocidad_traccion_val = nueva_vel
                print(f"Velocidad ajustada: {velocidad_traccion_val}")
        except:
            pass
    
    elif texto == '0': velocidad_traccion_val = 0
    elif texto == '1': velocidad_traccion_val = 25
    elif texto == '9': velocidad_traccion_val = 250
    elif texto == 'q': velocidad_traccion_val = 255

print("Iniciando:")
ble = BLEUART(name="ESP32-S3-Carro-Piton")
ble.set_rx_handler(procesar_comando)

while True:
    time.sleep_ms(100)