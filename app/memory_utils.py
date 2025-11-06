# memory_utils.py - Background utilities to reduce memory pressure

from typing import Optional
import threading
import time
import gc
import os

# psutil is optional; if present we'll log memory usage more precisely
try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optional dep
    psutil = None  # type: ignore


def _get_rss_bytes() -> Optional[int]:
    """Return current process RSS in bytes if psutil is available, else None."""
    if psutil is None:
        return None
    try:
        process = psutil.Process(os.getpid())
        return int(process.memory_info().rss)
    except Exception:
        return None


def start_memory_cleanup(interval_seconds: int = 300) -> None:
    """Start a background thread that periodically runs gc.collect().

    - interval_seconds: seconds between cleanup cycles (default 5 minutes)
    - Logs memory usage before/after if psutil is available
    """

    def _loop() -> None:
        while True:
            time.sleep(max(5, int(interval_seconds)))
            before = _get_rss_bytes()
            try:
                # Full collection; useful for long-lived processes
                unreachable = gc.collect()
                after = _get_rss_bytes()
                if before is not None and after is not None:
                    delta = after - before
                    sign = "+" if delta >= 0 else ""
                    print(
                        f"Memory cleanup: gc.collect() reclaimed={unreachable} objects; RSS change={sign}{delta} bytes at {time.ctime()}"
                    )
                else:
                    print(
                        f"Memory cleanup: gc.collect() reclaimed={unreachable} objects at {time.ctime()}"
                    )
            except Exception as e:
                print(f"Memory cleanup error at {time.ctime()}: {e}")

    threading.Thread(target=_loop, daemon=True).start()
    print(
        f"Memory cleanup background process started (gc.collect() every {interval_seconds} seconds)"
    )


def trigger_memory_cleanup_now() -> None:
    """Run an immediate gc.collect(), logging memory if possible."""
    before = _get_rss_bytes()
    try:
        unreachable = gc.collect()
        after = _get_rss_bytes()
        if before is not None and after is not None:
            delta = after - before
            sign = "+" if delta >= 0 else ""
            print(
                f"Manual memory cleanup: gc.collect() reclaimed={unreachable} objects; RSS change={sign}{delta} bytes at {time.ctime()}"
            )
        else:
            print(
                f"Manual memory cleanup: gc.collect() reclaimed={unreachable} objects at {time.ctime()}"
            )
    except Exception as e:
        print(f"Manual memory cleanup error at {time.ctime()}: {e}")


