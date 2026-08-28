# Network Speed Test (Windows MVP)

Aplicacion de consola para Windows 10 y Windows 11 que muestra un diagnostico puntual de la conexion actual: interfaz activa, tipo de conexion, IP local, ping, jitter, perdida de paquetes y velocidades de descarga y subida.

## Arquitectura

- `speed_test.py`: punto de entrada y presentacion de resultados.
- `network_info.py`: identifica la interfaz activa y la IP usada para salir a Internet.
- `measurements.py`: ejecuta ping de Windows y calcula ping, jitter y perdida.
- `speedtest_runner.py`: integra el cliente oficial Speedtest by Ookla ya instalado en el equipo.

La separacion deja preparada la aplicacion para comparar Ethernet, Wi-Fi, Windows host y maquinas virtuales en una etapa posterior, sin incluir aun base de datos ni historial.

## Dependencias y seguridad

- [psutil](https://github.com/giampaolo/psutil): libreria Python open source para consultar interfaces de red; no modifica configuraciones.
- [Speedtest CLI de Ookla](https://www.speedtest.net/apps/cli): cliente oficial, gratuito, para obtener una medicion de Internet comparable a Speedtest.net.

El programa no descarga ejecutables. Solo ejecuta `speedtest.exe` si tu lo instalaste previamente desde la fuente oficial y esta disponible en `PATH`. Tambien usa el comando `ping` incluido en Windows. No requiere permisos de administrador y no modifica Windows, DNS, firewall ni la configuracion de red.

La prueba de ancho de banda transfiere datos reales hacia un servidor publico seleccionado por Ookla. El resultado muestra el servidor usado para facilitar comparaciones justas.

## Instalacion

Requiere Windows 10/11 de 64 bits y Python 3.10 o superior.

1. Instala Speedtest CLI oficial de Ookla mediante `winget`:

```powershell
winget install --id Ookla.Speedtest.CLI --exact
```

Revisa y acepta los terminos que muestre el instalador. Despues comprueba la instalacion:

```powershell
speedtest --version
```

2. Instala la dependencia Python del proyecto:

```powershell
python -m pip install -r requirements.txt
```

Opcionalmente puedes usar un entorno virtual. Si `python -m venv .venv` funciona en tu equipo, activalo antes de instalar dependencias. No es obligatorio para ejecutar este MVP.

## Ejecucion

```powershell
python speed_test.py
```

En la primera ejecucion, el cliente oficial de Ookla puede solicitar la aceptacion de su licencia y terminos de privacidad. El programa los envia como opciones explicitas al ejecutar el cliente; usalo solo si aceptas esos terminos.

## Prueba y lectura de resultados

1. Cierra descargas, copias en la nube, streaming y VPN si quieres medir la capacidad de tu conexion.
2. Ejecuta `python speed_test.py` dos o tres veces, dejando un minuto entre pruebas.
3. Compara pruebas realizadas con el mismo servidor mostrado en `Speed test server`.

Ping bajo, jitter bajo y perdida de `0 %` normalmente indican una conexion estable. Las velocidades dependen del servidor, la hora, otros dispositivos y la red del proveedor. Para una comparacion con Speedtest.net, intenta usar el mismo servidor y hacer ambas pruebas en minutos cercanos.

## Seguridad del repositorio

El repositorio publico contiene solo codigo fuente y documentacion. No debes publicar contrasenas, tokens, claves privadas, archivos `.env` ni configuraciones locales. Antes de subir cambios, revisa `git status`. Protege tu cuenta GitHub con MFA o passkey y activa las alertas de Dependabot.

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
Speed test server: Example ISP (Bogota)
```