#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

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
