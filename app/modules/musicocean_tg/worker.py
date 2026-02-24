import asyncio
import time
from collections import deque
from typing import Optional

from aiogram import Bot
from asyncio import TimeoutError

from app.config import log

logger = log.get_logger(__name__)


class TelegramWorker(Bot):
    def __init__(
            self,
            token: str,
            max_requests: int = 20,
            window_seconds: int = 60,
            **kwargs
    ):
        super().__init__(token, **kwargs)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.used = deque()
        self._lock = asyncio.Lock()

    def _cleanup_old(self):
        cutoff = time.time() - self.window_seconds
        while self.used and self.used[0] < cutoff:
            self.used.popleft()

    def is_available(self) -> bool:
        self._cleanup_old()
        return len(self.used) < self.max_requests

    def _time_until_available(self) -> float:
        if self.is_available():
            return 0.0
        oldest_request = self.used[0]
        time_until_expires = (oldest_request + self.window_seconds) - time.time()
        return max(0.0, time_until_expires)

    async def _wait_for_slot(self, timeout: Optional[float] = None):
        start_time = time.time()
        while not self.is_available():
            wait_time = self._time_until_available()
            if timeout and (time.time() - start_time + wait_time) > timeout:
                raise TimeoutError("wait_for_slot timeout exceeded")
            await asyncio.sleep(wait_time + 0.01)

    async def _record_request(self):
        async with self._lock:
            self._cleanup_old()
            if len(self.used) >= self.max_requests:
                raise RuntimeError("no request slots available")
            self.used.append(time.time())

    async def send_audio(
            self,
            chat_id,
            audio,
            force: bool = False,
            rate_timeout: Optional[float] = None,
            **kwargs
    ):
        logger.debug(f"sending audio request, {force=}")
        if not force and not self.is_available():
            raise RuntimeError("rate limit exceeded blablabla")

        if not self.is_available():
            logger.debug(f"not available")
            async with self._lock:
                pass
            await self._wait_for_slot(timeout=rate_timeout)
        await self._record_request()

        return await super().send_audio(chat_id, audio, **kwargs)