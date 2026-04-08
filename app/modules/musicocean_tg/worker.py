import asyncio
import time
from collections import deque
from typing import Optional

from aiogram import Bot
from asyncio import TimeoutError

from app.config import log

logger = log.get_logger(__name__)


class TelegramWorker(Bot):
    def __init__(self, token: str, max_requests: int = 20, window_seconds: int = 60, **kwargs):
        super().__init__(token, **kwargs)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._used = deque()
        self._lock = asyncio.Lock()

    def _cleanup_old(self):
        cutoff = time.time() - self.window_seconds
        while self._used and self._used[0] < cutoff:
            self._used.popleft()

    def _time_until_available(self) -> float:
        self._cleanup_old()
        if len(self._used) < self.max_requests:
            return 0.0
        return max(0.0, self._used[0] + self.window_seconds - time.time())

    async def try_acquire(self) -> bool:
        async with self._lock:
            self._cleanup_old()
            if len(self._used) < self.max_requests:
                self._used.append(time.time())
                return True
            return False

    async def wait_and_acquire(self, timeout: Optional[float] = None):
        start = time.time()
        while True:
            async with self._lock:
                self._cleanup_old()
                if len(self._used) < self.max_requests:
                    self._used.append(time.time())
                    return
            wait = self._time_until_available()
            if timeout and (time.time() - start + wait) > timeout:
                raise TimeoutError("wait_and_acquire timeout exceeded")
            await asyncio.sleep(wait + 0.01)