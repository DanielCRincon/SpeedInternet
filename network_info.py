"""Funciones para identificar la conexión de red usada por Windows."""

from __future__ import annotations

import socket
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class NetworkConnection:
    """Datos básicos de la interfaz que está usando la ruta de salida."""

    interface: str
    connection_type: str
    local_ip: str


def _get_outbound_ip() -> str:
    """Obtiene la IP elegida por Windows para una ruta de salida, sin enviar datos."""
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


def get_active_connection() -> NetworkConnection:
    """Relaciona la IP de la ruta de salida con una interfaz activa de psutil."""
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
            return NetworkConnection(interface, _connection_type(interface), outbound_ip)

    raise RuntimeError("No se pudo asociar la IP de salida a una interfaz activa.")
