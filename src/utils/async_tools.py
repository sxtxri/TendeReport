import asyncio
from typing import Any, Coroutine, Iterable


async def shield_with_timeout(coroutine: Coroutine, timeout_in_seconds: int = 5):
    task = asyncio.create_task(coroutine)
    result = await asyncio.wait_for(asyncio.shield(task), timeout=timeout_in_seconds)

    return result


async def run_concurrent(*coroutines: Coroutine) -> Iterable[Any]:
    tasks = [asyncio.create_task(coro) for coro in coroutines]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    exception = next((t.exception() for t in done if t.exception()), None)
    if exception:
        for task in pending:
            task.cancel()
        raise exception

    # Возвращаем из tasks, так как done не гарантирует получение результатов
    #  в ранее указанном порядке
    return (task.result() for task in tasks)
