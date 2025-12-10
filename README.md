
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






## Proyecto: Carro Robot ESP32-S3 controlado por Bluetooth

Esta sección describe el **software en MicroPython** que corre en el ESP32-S3, definido en `SRC/main.py`.
El carro se controla desde la siguiente página web (cliente BLE UART):

https://6937cc04e718eb102e289199--cute-pothos-cb6f4b.netlify.app/

El ESP32 expone un servicio BLE tipo UART y recibe comandos de texto para mover el motor de **tracción** y el de **dirección**.

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

## 1. Configurar el puerto y la versión de firmware

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

## 2. Flashear y subir el código

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

## 3. Cómo funciona el código (`SRC/main.py`)

Resumen del comportamiento principal del script actual:

- Define pines de **tracción**: `PIN_TRACCION_A` y `PIN_TRACCION_B`.
- Define pines de **dirección**: `PIN_DIRECCION_A` y `PIN_DIRECCION_B`.
- Configura una frecuencia PWM común `PWM_FREQ = 1000` Hz.
- Implementa la clase `BLEUART`, que crea un servicio BLE UART y anuncia el dispositivo.
- Implementa la clase `Motor`, que usa **dos pines PWM por motor** (A y B) para controlar **sentido** y **velocidad** sin necesitar un pin `EN` extra:
  - Adelante: A con PWM, B en 0.
  - Atrás: A en 0, B con PWM.
  - Stop: ambos en 0.
- Crea dos instancias de `Motor`:
  - `motor_traccion`: controla el motor que mueve el carrito hacia adelante/atrás.
  - `motor_direccion`: controla el motor que gira las llantas.
- Define velocidades base:
  - `velocidad_traccion_val = 200` (tracción).
  - `velocidad_giro_val = 255` (dirección, máxima fuerza).
- Registra la función `procesar_comando` como callback BLE para procesar los comandos recibidos.

### Comandos soportados

Todos los comandos llegan como texto (caracteres) vía BLE UART.

**Movimientos simples**

- `F` → Avanzar recto.
  - La tracción se mueve hacia adelante (`motor_traccion.mover(velocidad_traccion_val)`).
  - La dirección se centra/detiene (`motor_direccion.stop()`).
- `B` → Retroceder recto.
- `L` → Girar a la izquierda (mueve solo el motor de dirección en un sentido).
- `R` → Girar a la derecha (mueve solo el motor de dirección en el sentido contrario).
- `S` → Detener todo (tracción y dirección en stop).

**Movimientos combinados (avance/retroceso + giro)**

Estos comandos permiten que el carrito avance o retroceda **mientras gira**:

- `G` → Avanzar y girar (sentido de giro depende del cableado del motor de dirección).
- `I` → Avanzar y girar hacia el lado opuesto a `G`.
- `H` → Retroceder y girar (mismo sentido que `G`).
- `J` → Retroceder y girar hacia el lado opuesto a `H`.

**Ajuste de velocidad de tracción**

- `VXXX` o `vXXX` → Ajusta `velocidad_traccion_val` a un valor entre 0 y 255.
  - Ejemplo: `V180` pone la velocidad de tracción en 180.

Presets rápidos (según el código):

- `0` → `velocidad_traccion_val = 0` (parado).
- `1` → `velocidad_traccion_val = 25` (muy lento).
- `9` → `velocidad_traccion_val = 250` (muy rápido).
- `q` → `velocidad_traccion_val = 255` (máxima velocidad).

---

## 4. Uso con la página web de control

1. Enciende el ESP32-S3 con el código ya cargado.
2. Activa el Bluetooth de tu dispositivo (PC o móvil).
3. Abre la página web de control:

   https://6937cc04e718eb102e289199--cute-pothos-cb6f4b.netlify.app/

4. Busca el dispositivo BLE con nombre **`ESP32-S3-Carro-Piton`** y conéctate.
5. Usa los controles de la página (botones/direcciones/slider) para enviar comandos:
   - Adelante (`F`), atrás (`B`), girar (`L`, `R`), detener (`S`).
   - Combinados (`G`, `I`, `H`, `J`) para curvas hacia adelante o hacia atrás.
   - Slider o campos numéricos para enviar `VXXX` y cambiar la velocidad de tracción.

La página actúa como un cliente BLE UART: envía los caracteres y el ESP32 ejecuta la lógica de `procesar_comando` para mover el carrito.

---

##  Notas y recomendaciones

- Verifica que el mapeo de pines (`PIN_TRACCION_A`, `PIN_TRACCION_B`, `PIN_DIRECCION_A`, `PIN_DIRECCION_B`) coincide con el cableado real hacia el driver L298N (IN1..IN4).
- Asegúrate de compartir **tierra común (GND)** entre fuente de motores, L298N y ESP32, como se muestra en el diagrama.
- Si el sentido de giro no coincide (
  por ejemplo, `L` gira hacia la derecha), intercambia los cables A/B del motor de dirección o invierte el signo en el código.
- Si el carrito no responde:
  - Revisa que el dispositivo BLE `ESP32-S3-Carro-Piton` esté visible y conectado.
  - Comprueba la alimentación de los motores (batería/fuente) y del ESP32.
  - Verifica que la página esté enviando los comandos descritos arriba.

# Excelente README 
