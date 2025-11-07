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
    - Performs aggressive cleanup in production
    """

    def _loop() -> None:
        while True:
            time.sleep(max(5, int(interval_seconds)))
            before = _get_rss_bytes()
            try:
                # Set threshold to be more aggressive about collecting generation 0
                # This helps catch objects that are accumulating but not yet in cycles
                collected = 0
                for generation in range(3):
                    count = gc.collect(generation)
                    collected += count
                
                after = _get_rss_bytes()
                if before is not None and after is not None:
                    delta = after - before
                    mb_before = before / (1024 * 1024)
                    mb_after = after / (1024 * 1024)
                    sign = "+" if delta >= 0 else ""
                    print(
                        f"Memory cleanup: gc.collect() reclaimed={collected} objects; "
                        f"Memory: {mb_before:.1f}MB -> {mb_after:.1f}MB ({sign}{abs(delta)/(1024*1024):.1f}MB) at {time.ctime()}"
                    )
                else:
                    print(
                        f"Memory cleanup: gc.collect() reclaimed={collected} objects at {time.ctime()}"
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
        collected = 0
        for generation in range(3):
            count = gc.collect(generation)
            collected += count
        after = _get_rss_bytes()
        if before is not None and after is not None:
            delta = after - before
            mb_before = before / (1024 * 1024)
            mb_after = after / (1024 * 1024)
            sign = "+" if delta >= 0 else ""
            print(
                f"Manual memory cleanup: gc.collect() reclaimed={collected} objects; "
                f"Memory: {mb_before:.1f}MB -> {mb_after:.1f}MB ({sign}{abs(delta)/(1024*1024):.1f}MB) at {time.ctime()}"
            )
        else:
            print(
                f"Manual memory cleanup: gc.collect() reclaimed={collected} objects at {time.ctime()}"
            )
    except Exception as e:
        print(f"Manual memory cleanup error at {time.ctime()}: {e}")


def cleanup_dataframe(df) -> None:
    """Helper to explicitly delete a DataFrame and trigger immediate cleanup if large."""
    if df is not None:
        try:
            del df
            # Force collection if DataFrame was large (rough heuristic)
            gc.collect(0)  # Only generation 0 for speed
        except Exception:
            pass  # Ignore errors during cleanup
