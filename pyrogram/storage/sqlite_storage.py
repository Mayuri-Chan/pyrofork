#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import inspect
import sqlite3
import time
from typing import List, Tuple, Any

from pyrogram import raw
from .storage import Storage
from .. import utils

# language=SQLite
SCHEMA = """
CREATE TABLE sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BLOB,
    date      INTEGER NOT NULL,
    user_id   INTEGER,
    is_bot    INTEGER
);

CREATE TABLE peers
(
    id             INTEGER PRIMARY KEY,
    access_hash    INTEGER,
    type           INTEGER NOT NULL,
    username       TEXT,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE version
(
    number INTEGER PRIMARY KEY
);

CREATE INDEX idx_peers_id ON peers (id);
CREATE INDEX idx_peers_username ON peers (username);
CREATE INDEX idx_peers_phone_number ON peers (phone_number);

CREATE TRIGGER trg_peers_last_update_on
    AFTER UPDATE
    ON peers
BEGIN
    UPDATE peers
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


UNAME_SCHEMA = """
CREATE TABLE IF NOT EXISTS usernames
(
    id             TEXT PRIMARY KEY,
    peer_id        INTEGER NOT NULL,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TRIGGER IF NOT EXISTS trg_usernames_last_update_on
    AFTER UPDATE
    ON usernames
BEGIN
    UPDATE usernames
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


UPDATE_DC_SCHEMA = """
CREATE TABLE dc_options
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    dc_id    INTEGER,
    address  TEXT,
    port     INTEGER,
    is_ipv6  BOOLEAN,
    is_media BOOLEAN,
    is_default_ip BOOLEAN,
    UNIQUE(dc_id, is_ipv6, is_media)
);
"""


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(
            user_id=peer_id,
            access_hash=access_hash
        )

    if peer_type == "group":
        return raw.types.InputPeerChat(
            chat_id=-peer_id
        )

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash
        )

    raise ValueError(f"Invalid peer type: {peer_type}")


class SQLiteStorage(Storage):
    VERSION = 4
    USERNAME_TTL = 8 * 60 * 60
    UPDATE_DC_SCHEMA = globals().get("UPDATE_DC_SCHEMA", "")

    def __init__(self, name: str):
        super().__init__(name)

        self.conn = None  # type: sqlite3.Connection

    def create(self):
        with self.conn:
            self.conn.executescript(SCHEMA)
            self.conn.executescript(UNAME_SCHEMA)
            self.conn.executescript(self.UPDATE_DC_SCHEMA)

            self.conn.execute(
                "INSERT INTO version VALUES (?)",
                (self.VERSION,)
            )

            self.conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                (2, None, None, None, 0, None, None)
            )

    async def open(self):
        raise NotImplementedError

    async def save(self):
        await self.date(int(time.time()))
        self.conn.commit()

    async def close(self):
        self.conn.close()

    async def delete(self):
        raise NotImplementedError

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        self.conn.executemany(
            "REPLACE INTO peers (id, access_hash, type, username, phone_number)"
            "VALUES (?, ?, ?, ?, ?)",
            peers
        )

    async def update_usernames(self, usernames: List[Tuple[int, str]]):
        self.conn.executescript(UNAME_SCHEMA)
        for user in usernames:
            self.conn.execute(
                "DELETE FROM usernames WHERE peer_id=?",
                (user[0],)
            )
        self.conn.executemany(
            "REPLACE INTO usernames (peer_id, id)"
            "VALUES (?, ?)",
            usernames
        )

    async def update_state(self, value: Tuple[int, int, int, int, int] = object):
        if value == object:
            return self.conn.execute(
                "SELECT id, pts, qts, date, seq FROM update_state"
            ).fetchall()
        else:
            with self.conn:
                if isinstance(value, int):
                    self.conn.execute(
                        "DELETE FROM update_state WHERE id = ?",
                        (value,)
                    )
                else:
                    self.conn.execute(
                        "REPLACE INTO update_state (id, pts, qts, date, seq)"
                        "VALUES (?, ?, ?, ?, ?)",
                        value
                    )

    async def remove_state(self, chat_id):
        self.conn.execute(
            "DELETE FROM update_state WHERE id = ?",
            (chat_id,)
        )

    async def get_peer_by_id(self, peer_id: int):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,)
        ).fetchone()

        if r is None:
            raise KeyError(f"ID not found: {peer_id}")

        return get_input_peer(*r)

    async def get_peer_by_username(self, username: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = ?"
            "ORDER BY last_update_on DESC",
            (username,)
        ).fetchone()

        if r is None:
            r2 = self.conn.execute(
                "SELECT peer_id, last_update_on FROM usernames WHERE id = ?"
                "ORDER BY last_update_on DESC",
                (username,)
            ).fetchone()
            if r2 is None:
                raise KeyError(f"Username not found: {username}")
            if abs(time.time() - r2[1]) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {username}")
            r = r = self.conn.execute(
                "SELECT id, access_hash, type, last_update_on FROM peers WHERE id = ?"
                "ORDER BY last_update_on DESC",
                (r2[0],)
            ).fetchone()
            if r is None:
                raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(*r[:3])

    async def get_peer_by_phone_number(self, phone_number: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,)
        ).fetchone()

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(*r)

    async def update_dc_address(
        self,
        value: Tuple[int, str, int, bool, bool, bool, bool] = object
    ):
        """
        Updates or inserts a data center address.

        Parameters:
            value (Tuple[int, str, int, bool, bool, bool]): A tuple containing:
                - dc_id (int): Data center ID.
                - address (str): Address of the data center.
                - port (int): Port of the data center.
                - is_ipv6 (bool): Whether the address is IPv6.
                - is_media (bool): Whether it is a media data center.
                - is_default_ip (bool): Whether it is the dc IP address provided by library.
        """
        if value == object:
            return
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO dc_options (dc_id, address, port, is_ipv6, is_media, is_default_ip)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(dc_id, is_ipv6, is_media)
                DO UPDATE SET address=excluded.address, port=excluded.port
                """,
                value
            )

    async def get_dc_address(
        self,
        dc_id: int,
        is_ipv6: bool,
        media: bool = False
    ) -> Tuple[str, int]:
        """
        Retrieves the address of a data center.

        Parameters:
            dc_id (int): Data center ID.
            is_ipv6 (bool): Whether the address is IPv6.
            media (bool): Whether it is a media data center.

        Returns:
            Tuple[str, int]: A tuple containing the address and port of the data center.
        """
        if dc_id in [1,3,5] and media:
            media = False
        r = self.conn.execute(
            "SELECT address, port, is_default_ip FROM dc_options WHERE dc_id = ? AND is_ipv6 = ? AND is_media = ?",
            (dc_id, is_ipv6, media)
        ).fetchone()

        return r

    def _get(self):
        attr = inspect.stack()[2].function

        return self.conn.execute(
            f"SELECT {attr} FROM sessions"
        ).fetchone()[0]

    def _set(self, value: Any):
        attr = inspect.stack()[2].function

        with self.conn:
            self.conn.execute(
                f"UPDATE sessions SET {attr} = ?",
                (value,)
            )

    def _accessor(self, value: Any = object):
        return self._get() if value == object else self._set(value)

    async def dc_id(self, value: int = object):
        return self._accessor(value)

    async def api_id(self, value: int = object):
        return self._accessor(value)

    async def test_mode(self, value: bool = object):
        return self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return self._accessor(value)

    async def date(self, value: int = object):
        return self._accessor(value)

    async def user_id(self, value: int = object):
        return self._accessor(value)

    async def is_bot(self, value: bool = object):
        return self._accessor(value)

    def version(self, value: int = object):
        if value == object:
            return self.conn.execute(
                "SELECT number FROM version"
            ).fetchone()[0]
        else:
            with self.conn:
                self.conn.execute(
                    "UPDATE version SET number = ?",
                    (value,)
                )
