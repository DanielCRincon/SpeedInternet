"""Safe adapter for the user-installed official Ookla Speedtest CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class SpeedMetrics:
    download_mbps: float
    upload_mbps: float
    server_name: str
    server_location: str


def _find_speedtest() -> str:
    """Find an explicitly configured binary or the official Winget installation."""
    configured_path = os.environ.get("OOKLA_SPEEDTEST_EXE")
    if configured_path and Path(configured_path).is_file():
        return configured_path

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        packages = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        candidates = sorted(packages.glob("Ookla.Speedtest.CLI_*/speedtest.exe"))
        if candidates:
            return str(candidates[-1])

    raise RuntimeError(
        "No se encontro Speedtest by Ookla instalado por Winget. "
        "Instalalo con: winget install --id Ookla.Speedtest.CLI --exact"
    )


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