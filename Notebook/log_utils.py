# log_utils.py — Utilidad compartida para loguear el output de consola de cada script
import sys
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).parent / "logs"


class _Tee:
    """Escribe simultáneamente en varios streams (ej: consola + archivo)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


def setup_logging(script_name: str | None = None) -> Path:
    """Redirige stdout/stderr para que todo el output de consola también quede en un log.

    Llamar al inicio del script. Genera logs/<script>_<timestamp>.log
    """
    LOGS_DIR.mkdir(exist_ok=True)
    if script_name is None:
        script_name = Path(sys.argv[0]).stem or "script"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"{script_name}_{timestamp}.log"
    log_file = open(log_path, "w", encoding="utf-8")

    sys.stdout = _Tee(sys.stdout, log_file)
    sys.stderr = _Tee(sys.stderr, log_file)

    print(f"=== Log iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"Script: {script_name}\n")

    return log_path
