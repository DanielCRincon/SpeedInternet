"""Functions for identifying the active Windows network connection."""

from __future__ import annotations

import socket
import subprocess
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class NetworkConnection:
    """Basic details for the interface used by the outbound route."""

    interface: str
    connection_type: str
    local_ip: str
    wifi_ssid: str | None = None


def _get_outbound_ip() -> str:
    """Return the IP Windows selects for an outbound route without sending data."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(("1.1.1.1", 80))
        return sock.getsockname()[0]


def _connection_type(interface: str) -> str:
    name = interface.lower()
    if any(word in name for word in ("wi-fi", "wifi", "wireless", "wlan")):
        return "Wi-Fi"
    if any(word in name for word in ("ethernet", "lan", "eth")):
        return "Ethernet"
    return "Unknown"


def _get_wifi_ssid() -> str | None:
    """Return the SSID reported by Windows for the connected Wi-Fi adapter."""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip().lower() == "ssid":
            return value.strip() or None
    return None


def get_active_connection() -> NetworkConnection:
    """Match the outbound IP to an active psutil interface."""
    outbound_ip = _get_outbound_ip()
    addresses = psutil.net_if_addrs()
    statistics = psutil.net_if_stats()

    for interface, interface_addresses in addresses.items():
        is_up = statistics.get(interface) and statistics[interface].isup
        has_outbound_ip = any(
            address.family == socket.AF_INET and address.address == outbound_ip
            for address in interface_addresses
        )
        if is_up and has_outbound_ip:
            connection_type = _connection_type(interface)
            wifi_ssid = _get_wifi_ssid() if connection_type == "Wi-Fi" else None
            return NetworkConnection(interface, connection_type, outbound_ip, wifi_ssid)

    raise RuntimeError("No se pudo asociar la IP de salida a una interfaz activa.")