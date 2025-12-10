
<p align="center">
  <img src="assets/carrito.png" alt="Carrito ESP32 + L298N" width="260">
</p>

<h1 align="center">CARRITO BLUETOOTH</h1>

<p align="center">
  Carrito controlado con ESP32, driver L298N y un celular vía Bluetooth.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plataforma-ESP32-1565c0?style=for-the-badge&logo=espressif&logoColor=white">
  <img src="https://img.shields.io/badge/Lenguaje-MicroPython-0d47a1?style=for-the-badge">
  <img src="https://img.shields.io/badge/Driver-L298N-42a5f5?style=for-the-badge">
</p>

---

<!-- COLABORADORES (BADGES) -->
<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Julio%20César%20Maldonado%20Acuña-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Roberto%20Emiliano%20Ortiz%20Cumpian-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Ricardo%20Martin%20Pugliesse%20Macias-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Felipe%20Pinzon%20Segura-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Gael%20Sebastian%20Castillo%20Salazar-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Alexis%20Manuel%20Muñoz%20Aguilar-collaborator-1565c0?style=flat-square&labelColor=0d47a1&logo=github&logoColor=white">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Grupo-IM%20--%202-1e88e5?style=flat-square&labelColor=0d47a1">
  </a>
</p>

---

## 👥 Integrantes

> **Proyecto desarrollado por el equipo:**

- Julio César Maldonado Acuña - 2530001
- Roberto Emiliano Ortiz Cumpian - 2530167 
- Ricardo Martin Pugliesse Macias - 2530033
- Felipe Pinzon Segura  - 2530495
- Gael Sebastian Castillo Salazar - 2530240
- Alexis Manuel Muñoz Aguilar - 2530562

**Grupo:** IM  1- 2  

---

## Descripción 📖

Este proyecto consiste en la construcción y programación de un **carrito controlado por un ESP32**, utilizando un módulo **L298N** para manejar dos motores DC:

- Un motor de **tracción** para avanzar y retroceder.  
- Un motor de **dirección** para girar las llantas.

El movimiento se controla desde un **teléfono celular** mediante **Bluetooth (BLE tipo UART)**.  
El ESP32 recibe comandos simples (por ejemplo `F`, `B`, `L`, `R`, `S`) y ajusta la velocidad y sentido de los motores usando **PWM**.

El software está desarrollado en **MicroPython**, aprovechando:

- Módulos de **Bluetooth BLE** para la comunicación con el celular.  
- **PWM** por hardware para el control de los motores a través del L298N.  

Este README funciona como **introducción** al resto de la documentación del proyecto:
código, esquemas eléctricos, pruebas y conclusiones.

---

## Hardware utilizado ⚙️

| Componente                  | Función                                         |
|----------------------------|-------------------------------------------------|
| ESP32 S3                   | Control principal / procesamiento               |
| Driver L298N               | Control de dos motores DC (puente H doble)     |
| 2 Motores DC               | Tracción y dirección del carrito               |
| Pack 6×AA NiMH (7.2–8 V)   | Fuente de energía para los motores             |
| Pilas 9v                   | Alimentación de ESP32 S3                       |
| Regulador de Voltaje 7805  | Regulación de alimentación de ESP32 S3         |
| Celular con app BLE (UART) | Envío de comandos de movimiento                |
| Chasis de carrito          | Soporte estructural de todos los componentes   |
| Cables jumper / protoboard | Conexiones eléctricas                          |

---

## Arquitectura del sistema 🧠

```text
          CELULAR
        (App BLE UART)
               |
           Bluetooth
               |
        +------v-------+
        |    ESP32     |
        | MicroPython  |
        +---+-------+--+
            |       |
      PWM Tracción  PWM Dirección
            |       |
       +----v-------v----+
       |      L298N      |
       |  Puente H x2    |
       +----+-------+----+
            |       |
      Motor Tracción   Motor Dirección
         (DC)              (DC)

     Pack baterías (6xAA NiMH)
          +Vmot  y  GND
               |
           L298N GND
               |
           ESP32 GND
        (tierra común)

---

## Licencia 📜
Copyright (c) 2025 Julio





## Proyecto: Carro Robot ESP32-S3 controlado por Bluetooth

Este proyecto permite controlar un carro robot basado en ESP32-S3 usando Bluetooth Low Energy (BLE).
El control se realiza desde esta página web:

https://6937cc04e718eb102e289199--cute-pothos-cb6f4b.netlify.app/

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

	https://6937cc04e718eb102e289199--cute-pothos-cb6f4b.netlify.app/

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


