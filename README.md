## Proyecto: Carro Robot ESP32-S3 controlado por Bluetooth

Este proyecto permite controlar un carro robot basado en ESP32-S3 usando Bluetooth Low Energy (BLE).
El control se realiza desde esta página web:

https://ai.studio/apps/drive/1Tx6DSF5-fUQnsCF_Ufs3YaURe3OeP7iy?fullscreenApplet=true

El firmware MicroPython que corre en la placa está en `SRC/main.py` y expone un servicio BLE tipo UART para recibir comandos de movimiento.

---

## 1. Requisitos en el PC

En tu PC (Windows) necesitas Python y las herramientas para flashear y subir el código:

```powershell
pip install -r requeriments.txt
```

Paquetes clave:
- `esptool`: para flashear el firmware MicroPython en el ESP32-S3.
- `adafruit-ampy`: para subir `SRC/main.py` a la placa.
- `pyserial`: para manejar el puerto serie.

---

## 2. Configurar el puerto y la versión de firmware

Edita el archivo `uploadcode.bat` y ajusta:

- `COM4` → por el puerto serie de tu ESP32-S3.
- `ESP32_GENERIC_S3-20250809-v1.26.0.bin` → por el nombre del binario de MicroPython que uses (si es diferente).

Ejemplo de `uploadcode.bat`:

```bat
esptool --port COM4 erase_flash

esptool --port COM4 --baud 460800 write_flash 0 ESP32_GENERIC_S3-20250809-v1.26.0.bin

ampy --port COM4 put SRC/main.py
```

---

## 3. Flashear y subir el código

1. Conecta la placa ESP32-S3 por USB.
2. Asegúrate de que el puerto en `uploadcode.bat` es correcto.
3. Desde PowerShell, en la carpeta del proyecto, ejecuta:

```powershell
uploadcode.bat
```

Esto hará:
- Borrar la flash de la placa.
- Grabar el firmware MicroPython.
- Subir `SRC/main.py` a la raíz del sistema de archivos de la placa.

---

## 4. Cómo funciona el código

El archivo `SRC/main.py` hace lo siguiente:

- Configura 4 motores con PWM (pines `PIN_PWM_M1..M4` y pines de dirección `PIN_Mx_INy`).
- Crea un servicio BLE UART con nombre `ESP32-S3-Carro` usando la clase `BLEUART`.
- Espera comandos de texto por BLE y los procesa en la función `procesar_comando`.

Comandos soportados (enviados como texto ASCII):

- `F` → Avanzar (Forward).
- `B` → Retroceder (Backward).
- `L` → Girar a la izquierda sobre su eje.
- `R` → Girar a la derecha sobre su eje.
- `S` → Stop (detener todos los motores).
- `VXXX` → Cambiar velocidad, donde `XXX` es un número entre 0 y 255.
	- Ejemplo: `V200` cambia la velocidad a 200.

El valor de velocidad por defecto es `150`.

---

## 5. Uso con la página web de control

1. Enciende el ESP32-S3 con el código ya cargado.
2. Asegúrate de que el Bluetooth de tu dispositivo (PC o móvil) está activado.
3. Abre la página:

	 https://ai.studio/apps/drive/1Tx6DSF5-fUQnsCF_Ufs3YaURe3OeP7iy?fullscreenApplet=true

4. Busca el dispositivo BLE con nombre `ESP32-S3-Carro` y conéctate.
5. Usa los controles de la página (botones/direcciones) para enviar comandos:
	 - Adelante, atrás, izquierda, derecha, parar y ajustar velocidad.

La página actúa como un cliente BLE UART, enviando las letras/comandos que el código interpreta para mover el carro.

---

## 6. Notas y recomendaciones

- Verifica que el mapeo de pines (`PIN_PWM_Mx`, `PIN_Mx_INy`) coincide con tu cableado real de los drivers de motor.
- Si cambias pines en el hardware, también debes actualizar los valores en `SRC/main.py`.
- Si el carro no responde, comprueba:
	- Que el dispositivo BLE `ESP32-S3-Carro` esté visible y conectado.
	- Que la alimentación de los motores (batería/fuente) sea suficiente.
	- Que los comandos que envía la página coincidan con los listados arriba.


