import asyncio

import pytest

from app.bot.utils.batch_guard import BatchBusy, BatchGuard, UserBatchBusy


@pytest.mark.asyncio
async def test_second_batch_of_same_user_is_rejected():
    guard = BatchGuard(max_concurrent=3)
    async with guard.reserve(1):
        with pytest.raises(UserBatchBusy):
            async with guard.reserve(1):
                pass


@pytest.mark.asyncio
async def test_slot_frees_up_after_the_batch():
    guard = BatchGuard(max_concurrent=1)
    async with guard.reserve(1):
        pass
    async with guard.reserve(1):
        assert guard.running == 1
    assert guard.running == 0


@pytest.mark.asyncio
async def test_bot_wide_limit_rejects_extra_users():
    guard = BatchGuard(max_concurrent=2)
    async with guard.reserve(1), guard.reserve(2):
        with pytest.raises(BatchBusy):
            async with guard.reserve(3):
                pass


@pytest.mark.asyncio
async def test_slot_released_when_batch_raises():
    guard = BatchGuard(max_concurrent=1)
    with pytest.raises(RuntimeError):
        async with guard.reserve(1):
            raise RuntimeError
    assert guard.running == 0
    async with guard.reserve(1):
        pass


@pytest.mark.asyncio
async def test_concurrent_reservations_do_not_exceed_the_limit():
    guard = BatchGuard(max_concurrent=2)
    rejected = 0

    async def run(user_id: int):
        nonlocal rejected
        try:
            async with guard.reserve(user_id):
                await asyncio.sleep(0.05)
        except BatchBusy:
            rejected += 1

    await asyncio.gather(*(run(i) for i in range(5)))
    assert rejected == 3
    assert guard.running == 0
