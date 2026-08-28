"""Safe adapter for the user-installed official Ookla Speedtest CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class SpeedMetrics:
    download_mbps: float
    upload_mbps: float
    server_name: str
    server_location: str


def _find_speedtest() -> str:
    executable = shutil.which("speedtest.exe") or shutil.which("speedtest")
    if not executable:
        raise RuntimeError(
            "No se encontro Speedtest by Ookla. Instalalo manualmente desde "
            "https://www.speedtest.net/apps/cli y vuelve a ejecutar el programa."
        )
    return executable


def measure_speed() -> SpeedMetrics:
    """Run the official local CLI; this program never downloads executables."""
    executable = _find_speedtest()
    try:
        result = subprocess.run(
            [
                executable,
                "--accept-license",
                "--accept-gdpr",
                "--format=json",
                "--progress=no",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"No fue posible ejecutar Speedtest by Ookla: {error}") from error

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "sin detalle disponible"
        raise RuntimeError(f"Speedtest by Ookla fallo: {detail}")

    try:
        payload = json.loads(result.stdout)
        return SpeedMetrics(
            download_mbps=payload["download"]["bandwidth"] * 8 / 1_000_000,
            upload_mbps=payload["upload"]["bandwidth"] * 8 / 1_000_000,
            server_name=payload["server"]["name"],
            server_location=payload["server"]["location"],
        )
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("Speedtest by Ookla devolvio una respuesta no valida.") from error