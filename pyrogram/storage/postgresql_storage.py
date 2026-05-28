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

import asyncio
import asyncpg
import inspect
import time
from typing import List, Tuple, Any

from pyrogram.storage.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BYTEA,
    date      INTEGER NOT NULL,
    user_id   BIGINT,
    is_bot    INTEGER
);

CREATE TABLE IF NOT EXISTS peers
(
    id             BIGINT PRIMARY KEY,
    access_hash    BIGINT,
    type           VARCHAR NOT NULL,
    username       TEXT,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()))
);

CREATE TABLE IF NOT EXISTS update_state
(
    id   BIGINT PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE IF NOT EXISTS version
(
    number INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS usernames
(
    id             TEXT PRIMARY KEY,
    peer_id        BIGINT NOT NULL,
    last_update_on INTEGER NOT NULL DEFAULT (EXTRACT(EPOCH FROM NOW()))
);

CREATE TABLE IF NOT EXISTS auth_keys
(
    dc_id     INTEGER PRIMARY KEY,
    auth_key  BYTEA
);

CREATE TABLE IF NOT EXISTS dc_options
(
    id       SERIAL PRIMARY KEY,
    dc_id    INTEGER,
    address  TEXT,
    port     INTEGER,
    is_ipv6  BOOLEAN,
    is_media BOOLEAN,
    is_default_ip BOOLEAN,
    UNIQUE(dc_id, is_ipv6, is_media)
);
"""


class PostgreSQLStorage(Storage):
    """
    Initializes a new session using PostgreSQL via asyncpg.

    Parameters:
        - name (`str`):
            The session name. (Not directly used as DB name, but kept for compatibility).

        - database_url (`str`):
            PostgreSQL connection url, e.g.: *"postgresql://user:password@host:port/database"*.

        - remove_peers (`bool`, *optional*):
            Flag to remove data in the peers collection. If set to True, 
            the data related to peers will be removed everytime client logs out. 
            If set to False, the data will not be removed.
    """
    VERSION = 5
    USERNAME_TTL = 8 * 60 * 60

    def __init__(
        self,
        name: str,
        database_url: str,
        remove_peers: bool = False
    ):
        super().__init__(name)
        self.database_url = database_url
        self._remove_peers = remove_peers
        self.lock = asyncio.Lock()

    async def open(self):
        self.conn = await asyncpg.create_pool(self.database_url)
        async with self.lock:
            # Check if tables already exist
            table_exists = await self.conn.fetchval(
                "SELECT 1 FROM information_schema.tables WHERE table_name = 'version'"
            )

            if not table_exists:
                await self.conn.execute(SCHEMA)
                await self.conn.execute("INSERT INTO version (number) VALUES ($1)", self.VERSION)
            else:
                try:
                    await self.conn.execute("ALTER TABLE peers ALTER COLUMN type TYPE VARCHAR")
                except Exception:
                    pass
                try:
                    await self.conn.execute("""
                        CREATE TABLE IF NOT EXISTS auth_keys
                        (
                            dc_id     INTEGER PRIMARY KEY,
                            auth_key  BYTEA
                        );
                        CREATE TABLE IF NOT EXISTS dc_options
                        (
                            id       SERIAL PRIMARY KEY,
                            dc_id    INTEGER,
                            address  TEXT,
                            port     INTEGER,
                            is_ipv6  BOOLEAN,
                            is_media BOOLEAN,
                            is_default_ip BOOLEAN,
                            UNIQUE(dc_id, is_ipv6, is_media)
                        );
                    """)
                except Exception:
                    pass

            # Check session
            session = await self.conn.fetchval("SELECT dc_id FROM sessions")
            if session is None:
                await self.conn.execute(
                    "INSERT INTO sessions (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                    2, None, None, b"", 0, None, None
                )

    async def save(self):
        await self.date(int(time.time()))

    async def close(self):
        # We don't close the pool/conn here, as it's passed from outside
        pass

    async def delete(self):
        try:
            await self.conn.execute("DELETE FROM sessions")
            if self._remove_peers:
                await self.conn.execute("DELETE FROM peers")
                await self.conn.execute("DELETE FROM usernames")
        except Exception:
            return

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        if not peers:
            return
        
        s = int(time.time())
        # Use ON CONFLICT DO UPDATE
        query = """
            INSERT INTO peers (id, access_hash, type, username, phone_number, last_update_on)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (id) DO UPDATE SET
                access_hash = EXCLUDED.access_hash,
                type = EXCLUDED.type,
                username = EXCLUDED.username,
                phone_number = EXCLUDED.phone_number,
                last_update_on = EXCLUDED.last_update_on
        """
        async with self.lock:
            for peer in peers:
                await self.conn.execute(query, peer[0], peer[1], peer[2], peer[3], peer[4], s)

    async def update_usernames(self, usernames: List[Tuple[int, str]]):
        if not usernames:
            return
            
        s = int(time.time())
        delete_query = "DELETE FROM usernames WHERE peer_id = $1"
        insert_query = """
            INSERT INTO usernames (peer_id, id, last_update_on)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO UPDATE SET
                peer_id = EXCLUDED.peer_id,
                last_update_on = EXCLUDED.last_update_on
        """
        async with self.lock:
            for user in usernames:
                await self.conn.execute(delete_query, user[0])
                await self.conn.execute(insert_query, user[0], user[1], s)

    async def update_state(self, value: Tuple[int, int, int, int, int] = object):
        if value == object:
            states = await self.conn.fetch("SELECT id, pts, qts, date, seq FROM update_state")
            return [tuple(state) for state in states] if states else None
        else:
            if isinstance(value, int):
                await self.conn.execute("DELETE FROM update_state WHERE id = $1", value)
            else:
                query = """
                    INSERT INTO update_state (id, pts, qts, date, seq)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (id) DO UPDATE SET
                        pts = EXCLUDED.pts,
                        qts = EXCLUDED.qts,
                        date = EXCLUDED.date,
                        seq = EXCLUDED.seq
                """
                await self.conn.execute(query, value[0], value[1], value[2], value[3], value[4])

    async def remove_state(self, chat_id):
        await self.conn.execute("DELETE FROM update_state WHERE id = $1", chat_id)

    async def get_peer_by_id(self, peer_id: int):
        try:
            _id = int(peer_id)
        except ValueError:
            raise KeyError(f"ID not found: {peer_id}")

        r = await self.conn.fetchrow(
            "SELECT id, access_hash, type FROM peers WHERE id = $1", _id
        )

        if not r:
            raise KeyError(f"ID not found: {peer_id}")

        return get_input_peer(r['id'], r['access_hash'], r['type'])

    async def get_peer_by_username(self, username: str):
        r = await self.conn.fetchrow(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = $1 ORDER BY last_update_on DESC",
            username
        )

        if r is None:
            r2 = await self.conn.fetchrow(
                "SELECT peer_id, last_update_on FROM usernames WHERE id = $1 ORDER BY last_update_on DESC",
                username
            )
            if r2 is None:
                raise KeyError(f"Username not found: {username}")
            if abs(time.time() - r2['last_update_on']) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {username}")
            r = await self.conn.fetchrow(
                "SELECT id, access_hash, type, last_update_on FROM peers WHERE id = $1 ORDER BY last_update_on DESC",
                r2['peer_id']
            )
            if r is None:
                raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r['last_update_on']) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(r['id'], r['access_hash'], r['type'])

    async def get_peer_by_phone_number(self, phone_number: str):
        r = await self.conn.fetchrow(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = $1", phone_number
        )

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(r['id'], r['access_hash'], r['type'])

    async def update_dc_address(
        self,
        value: Tuple[int, str, int, bool, bool, bool] = object
    ):
        if value == object:
            return
        
        query = """
            INSERT INTO dc_options (dc_id, address, port, is_ipv6, is_media, is_default_ip)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (dc_id, is_ipv6, is_media) DO UPDATE SET
                address = EXCLUDED.address,
                port = EXCLUDED.port,
                is_default_ip = EXCLUDED.is_default_ip
        """
        await self.conn.execute(query, value[0], value[1], value[2], value[3], value[4], value[5])

    async def get_dc_address(
        self,
        dc_id: int,
        is_ipv6: bool,
        media: bool = False
    ):
        if dc_id in [1, 3, 5] and media:
            media = False
        r = await self.conn.fetchrow(
            "SELECT address, port, is_default_ip FROM dc_options WHERE dc_id = $1 AND is_ipv6 = $2 AND is_media = $3",
            dc_id, is_ipv6, media
        )
        if r is None:
            return None
        return r['address'], r['port'], r['is_default_ip']

    async def _get(self):
        attr = inspect.stack()[2].function
        return await self.conn.fetchval(f"SELECT {attr} FROM sessions")

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function
        await self.conn.execute(f"UPDATE sessions SET {attr} = $1", value)

    async def _accessor(self, value: Any = object):
        return await self._get() if value == object else await self._set(value)

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def get_auth_key(self, dc_id: int):
        r = await self.conn.fetchval(
            "SELECT auth_key FROM auth_keys WHERE dc_id = $1",
            dc_id
        )
        return r

    async def set_auth_key(self, dc_id: int, auth_key: bytes):
        query = """
            INSERT INTO auth_keys (dc_id, auth_key)
            VALUES ($1, $2)
            ON CONFLICT (dc_id) DO UPDATE SET
                auth_key = EXCLUDED.auth_key
        """
        await self.conn.execute(query, dc_id, auth_key)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)
