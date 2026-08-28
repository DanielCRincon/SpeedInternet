"""Punto de entrada de consola para el MVP Network Speed Test."""

from __future__ import annotations

from datetime import datetime

from measurements import measure_quality, measure_speed
from network_info import get_active_connection


def _format_ms(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.1f} ms"


def _format_mbps(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.2f} Mbps"


def main() -> int:
    print("## Network Speed Test\n")
    print(f"Test time: {datetime.now():%Y-%m-%d %H:%M}")

    try:
        connection = get_active_connection()
        print(f"Interface: {connection.interface} ({connection.connection_type})")
        print(f"Local IP: {connection.local_ip}")
    except RuntimeError as error:
        print(f"Network information: N/A ({error})")

    try:
        quality = measure_quality()
        print(f"Ping: {_format_ms(quality.ping_ms)}")
        print(f"Jitter: {_format_ms(quality.jitter_ms)}")
        print(f"Packet loss: {quality.packet_loss_percent:.1f} %")
    except RuntimeError as error:
        print(f"Quality test: N/A ({error})")

    print("\nMeasuring download and upload speed. This may take a moment...")
    try:
        speed = measure_speed()
        print(f"Download: {_format_mbps(speed.download_mbps)}")
        print(f"Upload: {_format_mbps(speed.upload_mbps)}")
    except RuntimeError as error:
        print(f"Speed test: N/A ({error})")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
