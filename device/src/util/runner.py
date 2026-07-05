import asyncio

class Runner:
    # 監視の反応の機敏さと電池持ちのトレードオフなため調節する
    # 0だと最も電池食うが反応は良い。100だと入力系統がモッサリしてしまった。
    _LOOP_WAIT_MS = 10

    def __init__(self, func):
        self._func = func
        self._task = None

    # TODO なんか汎用そうに見えてasync関数しか渡せない
    async def _execute(self):
        res = await self._func()
        if res is not None and hasattr(res, '__await__'):
            await res

    def run(self):
        if self._task is None:
            self._task = asyncio.create_task(self._execute())

    def loop(self):
        if self._task is None:
            async def coro():
                while True:
                    await self._execute()
                    await asyncio.sleep_ms(Runner._LOOP_WAIT_MS)
            self._task = asyncio.create_task(coro())

    def stop(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
