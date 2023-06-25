from pyrogram.utils import run_sync
from sqlite3 import Cursor
from threading import Thread

class AsyncCursor(Thread):
    def __init__(self, cursor: Cursor):
        super().__init__()
        self.cursor = cursor

    async def fetchone(self):
        return await run_sync(self.cursor.fetchone)
