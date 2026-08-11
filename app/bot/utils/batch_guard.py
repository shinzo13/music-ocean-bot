from contextlib import asynccontextmanager

from app.config.settings import settings


class BatchBusy(Exception):
    pass


class UserBatchBusy(BatchBusy):
    pass


class BatchGuard:
    """Keeps entity downloads to one per user and a few bot-wide at a time."""

    def __init__(self, max_concurrent: int):
        self._max = max_concurrent
        self._running = 0
        self._active: set[int] = set()

    @property
    def running(self) -> int:
        return self._running

    @asynccontextmanager
    async def reserve(self, user_id: int):
        # no awaits between the checks and the bookkeeping, so a single event
        # loop cannot slip a second batch through
        if user_id in self._active:
            raise UserBatchBusy
        if self._running >= self._max:
            raise BatchBusy
        self._active.add(user_id)
        self._running += 1
        try:
            yield
        finally:
            self._running -= 1
            self._active.discard(user_id)


batch_guard = BatchGuard(settings.limits.max_concurrent_batches)
