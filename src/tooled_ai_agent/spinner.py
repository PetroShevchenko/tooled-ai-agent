"""Animated "agent is thinking" indicator."""

import itertools
import sys
import threading
import time

from .colors import GRAY, RESET

class Spinner:
    FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, text: str = "Thinking") -> None:
        self.text = text
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def __enter__(self) -> "Spinner":
        if sys.stdout.isatty():            # We do not write the animation to a file/pipe
            self._thread = threading.Thread(target=self._spin, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join()
            sys.stdout.write("\r\033[K")    # delete spinner row
            sys.stdout.flush()

    def _spin(self) -> None:
        start = time.monotonic()
        for frame in itertools.cycle(self.FRAMES):
            elapsed = time.monotonic() - start
            sys.stdout.write(f"\r{GRAY}{frame} {self.text}… ({elapsed:.0f}s){RESET}")
            sys.stdout.flush()
            if self._stop.wait(0.1):        # frame every 0.1 s
                break
