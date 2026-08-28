"""Quality measurements for an Internet connection."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class QualityMetrics:
    ping_ms: float | None
    jitter_ms: float | None
    packet_loss_percent: float | None


def measure_quality(host: str = "1.1.1.1", count: int = 10) -> QualityMetrics:
    """Run Windows ping and calculate latency, jitter, and packet loss."""
    try:
        result = subprocess.run(
            ["ping", "-n", str(count), "-w", "1500", host],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=(count * 2) + 5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"No fue posible ejecutar ping: {error}") from error

    times = [
        0.5 if value == "<1" else float(value.replace(",", "."))
        for value in re.findall(
            r"(?:time|tiempo)\s*[=<]\s*(<1|\d+(?:[.,]\d+)?)\s*ms",
            result.stdout,
            re.I,
        )
    ]
    received = len(times)
    loss = ((count - received) / count) * 100
    if not times:
        return QualityMetrics(None, None, loss)

    jitter = (
        mean(abs(current - previous) for previous, current in zip(times, times[1:]))
        if len(times) > 1
        else 0.0
    )
    return QualityMetrics(mean(times), jitter, loss)