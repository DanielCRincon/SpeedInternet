# Network Speed Test (Windows MVP)

Aplicación de consola para Windows 10 y Windows 11 que muestra un diagnóstico puntual de la conexión actual: interfaz activa, tipo de conexión, IP local, latencia, jitter, pérdida de paquetes y velocidades de descarga y subida.

## Arquitectura

- `speed_test.py`: punto de entrada y presentación clara de resultados en la consola.
- `network_info.py`: identifica la IP elegida por la ruta de salida y la vincula a una interfaz activa.
- `measurements.py`: ejecuta las mediciones de calidad y de velocidad.

Esta separación deja preparada la aplicación para que en una siguiente etapa se guarden y comparen mediciones de Ethernet, Wi-Fi, host Windows o máquina virtual, sin añadir aún historial ni base de datos.

## Dependencias

- [psutil](https://github.com/giampaolo/psutil): consulta las interfaces y su estado mediante APIs del sistema; no modifica la configuración de red.
- [speedtest-cli](https://github.com/sivel/speedtest-cli): cliente open source que elige un servidor público de Speedtest.net/Ookla y realiza las pruebas de descarga y subida. No requiere API key ni descarga ejecutables externos.

El comando estándar `ping` incluido en Windows se usa únicamente para enviar sondas ICMP. El programa no cambia la configuración de red y no requiere permisos de administrador.

## Instalación

Requiere Python 3.10 o superior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno virtual, puede ejecutarse directamente con `.\.venv\Scripts\python.exe` en los comandos siguientes.

## Ejecución

```powershell
python speed_test.py
```

La prueba de ancho de banda transfiere datos reales y puede tardar unos segundos. Sus resultados dependen del servidor público seleccionado, la carga de red y la conexión local.

## Prueba rapida

1. Abre PowerShell dentro de la carpeta del proyecto.
2. Instala las dependencias una sola vez con `python -m pip install -r requirements.txt`.
3. Ejecuta `python speed_test.py`.
4. Espera los resultados de interfaz, IP local, ping, jitter, perdida y velocidades.

Si `python` no se reconoce como comando, instala Python 3.10 o superior desde [python.org](https://www.python.org/downloads/windows/) y marca **Add Python to PATH** durante la instalacion.

## Seguridad y privacidad

El repositorio publico contiene solo codigo fuente y documentacion; no incluye contrasenas, tokens, claves privadas, archivos `.env` ni datos de mediciones.

El programa no requiere permisos de administrador y no modifica Windows, DNS, firewall ni la configuracion de red. Solo consulta datos locales, envia `ping` a `1.1.1.1` y transfiere datos temporales con servidores publicos de Speedtest.net para medir el ancho de banda. Usalo en una conexion donde sea aceptable consumir algunos datos.

Antes de publicar cambios, ejecuta `git status` y evita anadir credenciales, archivos `.env`, claves SSH o configuraciones locales. Activa MFA o una passkey y las alertas de seguridad de Dependabot en GitHub.
## Salida esperada

```text
## Network Speed Test

Test time: 2026-08-28 08:30
Interface: Ethernet (Ethernet)
Local IP: 192.168.1.25
Ping: 15.0 ms
Jitter: 3.0 ms
Packet loss: 0.0 %
Download: 420.00 Mbps
Upload: 95.00 Mbps
```
