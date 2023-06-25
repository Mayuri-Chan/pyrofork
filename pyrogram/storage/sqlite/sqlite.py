import sqlite3
from .cursor import AsyncCursor
from pathlib import Path
from pyrogram.utils import run_sync
from threading import Thread
from typing import Union

class AsyncSqlite(Thread):
    def __init__(self, database: Union[str, Path], *args, **kwargs):
        super().__init__()
        self.connection = sqlite3.connect(database, *args, **kwargs)

    async def commit(self):
        return await run_sync(self.connection.commit)
    
    async def close(self):
        return await run_sync(self.connection.close)

    async def execute(self, *args, **kwargs):
        r = await run_sync(self.connection.execute, *args, **kwargs)
        return AsyncCursor(r)
    
    async def executemany(self, *args, **kwargs):
        r = await run_sync(self.connection.executemany, *args, **kwargs)
        return AsyncCursor(r)
    
    async def executescript(self, *args, **kwargs):
        r = await run_sync(self.connection.executescript, *args, **kwargs)
