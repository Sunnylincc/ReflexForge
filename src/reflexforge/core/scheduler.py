from __future__ import annotations
import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def gather_limited(tasks: list[Callable[[], Awaitable[T]]], concurrency: int = 4) -> list[T]:
    sem = asyncio.Semaphore(concurrency)

    async def run_one(factory: Callable[[], Awaitable[T]]) -> T:
        async with sem:
            return await factory()

    return await asyncio.gather(*(run_one(t) for t in tasks))
