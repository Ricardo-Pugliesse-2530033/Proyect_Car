import ubluetooth
import machine
from machine import Pin, PWM
import time

# ============================================================================
# 1. CONFIGURACIÓN DE PINES (Hardware)
# ============================================================================

# Pines PWM (Velocidad - ENA/ENB)
PIN_PWM_M1 = 4   # Delantero Izquierdo
PIN_PWM_M2 = 16  # Delantero Derecho
PIN_PWM_M3 = 17  # Trasero Izquierdo
PIN_PWM_M4 = 18  # Trasero Derecho

# Pines de Dirección (IN1, IN2, IN3, IN4)
# Puente H #1 (Delanteros)
PIN_M1_IN1 = 25
PIN_M1_IN2 = 26
PIN_M2_IN3 = 27
PIN_M2_IN4 = 14

# Puente H #2 (Traseros)
PIN_M3_IN1 = 32
PIN_M3_IN2 = 33
PIN_M4_IN3 = 12
PIN_M4_IN4 = 13

# Frecuencia PWM (1kHz es estándar para motores DC)
PWM_FREQ = 1000 


# ============================================================================
# Esta clase crea un servicio BLE que actúa como un puerto serial.

_UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX =   ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX =   ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

class BLEUART:
    def __init__(self, name="ESP32-Carro"):
        self._ble = ubluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((
            (_UART_UUID, ((_UART_TX, ubluetooth.FLAG_NOTIFY), (_UART_RX, ubluetooth.FLAG_WRITE),)),
        ))
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        self._advertise(name)

    def _irq(self, event, data):
        # Eventos de conexión y desconexión
        if event == 1: # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Bluetooth: Dispositivo Conectado")
        elif event == 2: # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            print("Bluetooth: Desconectado")
            self._advertise()
        elif event == 3: # _IRQ_GATTS_WRITE
            conn_handle, value_handle = data
            if value_handle == self._handle_rx:
                received = self._ble.gatts_read(self._handle_rx)
                if self._handler:
                    self._handler(received)

    def _advertise(self, name="ESP32-Carro"):
        name = bytes(name, 'UTF-8')
        # Formato de publicidad BLE simple
        payload = bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self._ble.gap_advertise(100, payload)

    def set_rx_handler(self, handler):
        self._handler = handler

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

# ============================================================================
# 3. CLASE MOTOR
# ============================================================================
class Motor:
    def __init__(self, pin_in1, pin_in2, pin_pwm):
        self.in1 = Pin(pin_in1, Pin.OUT)
        self.in2 = Pin(pin_in2, Pin.OUT)
        self.pwm = PWM(Pin(pin_pwm), freq=PWM_FREQ)
        self.pwm.duty_u16(0) # Iniciar detenido

    def mover(self, velocidad):
        """
        velocidad: Valor entre -255 (atrás max) y 255 (adelante max). 0 es stop.
        """
        # Convertir rango 0-255 a 0-65535 (MicroPython u16)
        duty = int(abs(velocidad) * 65535 / 255)
        
        # Limitar duty cycle
        if duty > 65535: duty = 65535
        
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

# ============================================================================
# 4. PROGRAMA PRINCIPAL
# ============================================================================

# Inicializar Motores
# M1: Delantero Izquierdo
motor_m1 = Motor(PIN_M1_IN1, PIN_M1_IN2, PIN_PWM_M1)
# M2: Delantero Derecho
motor_m2 = Motor(PIN_M2_IN3, PIN_M2_IN4, PIN_PWM_M2)
# M3: Trasero Izquierdo
motor_m3 = Motor(PIN_M3_IN1, PIN_M3_IN2, PIN_PWM_M3)
# M4: Trasero Derecho
motor_m4 = Motor(PIN_M4_IN3, PIN_M4_IN4, PIN_PWM_M4)

# Variable global de velocidad (0 a 255)
velocidad_actual = 150 
cmd_buffer = ""

def procesar_comando(data_bytes):
    global velocidad_actual, cmd_buffer
    
    try:
        texto = data_bytes.decode('utf-8').strip().upper()
        print("Comando recibido:", texto)
    except:
        return

    # Manejar comandos que llegan fragmentados o completos
    if not texto: return
    
    # 1. Control de Dirección (F, B, L, R, S)
    if texto == 'F': # Adelante
        print(f"Avanzando a velocidad {velocidad_actual}")
        motor_m1.mover(velocidad_actual)
        motor_m2.mover(velocidad_actual)
        motor_m3.mover(velocidad_actual)
        motor_m4.mover(velocidad_actual)
        
    elif texto == 'B': # Atrás
        print(f"Retrocediendo a velocidad {velocidad_actual}")
        motor_m1.mover(-velocidad_actual)
        motor_m2.mover(-velocidad_actual)
        motor_m3.mover(-velocidad_actual)
        motor_m4.mover(-velocidad_actual)

    elif texto == 'L': # Giro Izquierda (Sobre su eje)
        # Izquierdos atrás, Derechos adelante
        motor_m1.mover(-velocidad_actual)
        motor_m3.mover(-velocidad_actual)
        motor_m2.mover(velocidad_actual)
        motor_m4.mover(velocidad_actual)

    elif texto == 'R': # Giro Derecha (Sobre su eje)
        # Izquierdos adelante, Derechos atrás
        motor_m1.mover(velocidad_actual)
        motor_m3.mover(velocidad_actual)
        motor_m2.mover(-velocidad_actual)
        motor_m4.mover(-velocidad_actual)

    elif texto == 'S': # Stop
        print("Deteniendo")
        motor_m1.stop()
        motor_m2.stop()
        motor_m3.stop()
        motor_m4.stop()

    # 2. Control de Velocidad Global (Ej: V200, V100)
    elif texto.startswith('V'):
        try:
            val_str = texto[1:] # Quitar la V
            nueva_vel = int(val_str)
            if 0 <= nueva_vel <= 255:
                velocidad_actual = nueva_vel
                print(f"Velocidad actualizada a: {velocidad_actual}")
        except ValueError:
            print("Error en formato de velocidad")

    # 3. Control Individual (Ej: 1V255 para motor 1) - Opcional
    elif 'V' in texto and len(texto) > 2 and texto[0].isdigit():
        try:
            motor_idx = int(texto[0])
            val_str = texto.split('V')[1]
            vel = int(val_str)
            
            if motor_idx == 1: motor_m1.mover(vel)
            if motor_idx == 2: motor_m2.mover(vel)
            if motor_idx == 3: motor_m3.mover(vel)
            if motor_idx == 4: motor_m4.mover(vel)
        except:
            pass

# Inicio del Sistema
print("Iniciando Carro Robot ESP32...")
ble = BLEUART(name="ESP32-Carro")
ble.set_rx_handler(procesar_comando)

# Loop principal (el trabajo pesado lo hacen las interrupciones BLE)
while True:
    time.sleep_ms(100)