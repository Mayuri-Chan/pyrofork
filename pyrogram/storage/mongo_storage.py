#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022 Animesh Murmu <https://github.com/animeshxd>
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
import inspect
import time
from typing import List, Tuple, Any

from .dummy_client import DummyMongoClient
from pymongo import MongoClient, UpdateOne, DeleteMany
from pyrogram.storage.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer


class MongoStorage(Storage):
    """
    Initializes a new session.

    Parameters:
        - name (`str`):
            The session name used for database name.

        - connection (`obj`):
            Mongodb connections object.
            ~async_pymongo.AsyncClient or ~motor.motor_asyncio.AsyncIOMotorClient object

        - remove_peers (`bool`, *optional*):
            Flag to remove data in the peers collection. If set to True, 
            the data related to peers will be removed everytime client log out. 
            If set to False or None, the data will not be removed.

    Example:
        import async_pymongo

        conn = async_pymongo.AsyncClient("mongodb://...")
        bot_db = conn["my_bot"]
        session = MongoStorage("my_session", connection=conn, remove_peers=True)
    """
    lock: asyncio.Lock
    USERNAME_TTL = 8 * 60 * 60

    def __init__(
        self,
        name: str,
        connection: DummyMongoClient,
        remove_peers: bool = False
    ):
        super().__init__(name=name)
        database = None

        if isinstance(connection, DummyMongoClient):
            if isinstance(connection, MongoClient):
                raise Exception("Pymongo MongoClient object is not supported! please use async mongodb driver such as async_pymongo and motor.")
            database = connection[name]
        else:
            raise Exception("Wrong connection object type! please pass valid connection object to connection parameter!")

        self.lock = asyncio.Lock()
        self.database = database
        self._peer = database['peers']
        self._session = database['session']
        self._usernames = database['usernames']
        self._states = database['update_state']
        self._dc_options = database['dc_options']
        self._remove_peers = remove_peers

    async def open(self):
        """

        dc_id     INTEGER PRIMARY KEY,
        api_id    INTEGER,
        test_mode INTEGER,
        auth_key  BLOB,
        date      INTEGER NOT NULL,
        user_id   INTEGER,
        is_bot    INTEGER
        """
        if await self._session.find_one({'_id': 0}, {}):
            return
        await self._session.insert_one(
            {
                '_id': 0,
                'dc_id': 2,
                'api_id': None,
                'test_mode': None,
                'auth_key': b'',
                'date': 0,
                'user_id': 0,
                'is_bot': 0,

            }
        )

    async def save(self):
        pass

    async def close(self):
        pass

    async def delete(self):
        try:
            await self._session.delete_one({'_id': 0})
            if self._remove_peers:
                await self._peer.remove({})
        except Exception as _:
            return

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        """(id, access_hash, type, username, phone_number)"""
        s = int(time.time())
        bulk = [
            UpdateOne(
                {'_id': i[0]},
                {'$set': {
                    'access_hash': i[1], 
                    'type': i[2], 
                    'username': i[3], 
                    'phone_number': i[4],
                    'last_update_on': s
                }},
                upsert=True
            ) for i in peers
        ]
        if not bulk:
            return
        await self._peer.bulk_write(
            bulk
        )

    async def update_usernames(self, usernames: List[Tuple[int, str]]):
        s = int(time.time())
        bulk_delete = [
            DeleteMany(
                {'peer_id': i[0]}
            ) for i in usernames
        ]
        bulk = [
            UpdateOne(
                {'_id': i[1]},
                {'$set': {
                    'peer_id': i[0],
                    'last_update_on': s
                }},
                upsert=True
            ) for i in usernames
        ]
        if not bulk:
            return
        await self._usernames.bulk_write(
            bulk_delete
        )
        await self._usernames.bulk_write(
            bulk
        )

    async def update_state(self, value: Tuple[int, int, int, int, int] = object):
        if value == object:
            states = [[state['_id'],state['pts'],state['qts'],state['date'],state['seq']] async for state in self._states.find()]
            return states if len(states) > 0 else None
        else:
            if isinstance(value, int):
                await self._states.delete_one({'_id': value})
            else:
                await self._states.update_one({'_id': value[0]}, {'$set': {'pts': value[1], 'qts': value[2], 'date': value[3], 'seq': value[4]}}, upsert=True)

    async def remove_state(self, chat_id):
        await self._states.delete_one({'_id': chat_id})

    async def get_peer_by_id(self, peer_id: int):
        # id, access_hash, type
        r = await self._peer.find_one({'_id': peer_id}, {'_id': 1, 'access_hash': 1, 'type': 1})
        if not r:
            raise KeyError(f"ID not found: {peer_id}")
        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_username(self, username: str):
        # id, access_hash, type, last_update_on,
        r = await self._peer.find_one({'username': username},
                                      {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})

        if r is None:
            r2 = await self._usernames.find_one({'_id': username},
                                          {'peer_id': 1, 'last_update_on': 1})
            if r2 is None:
                raise KeyError(f"Username not found: {username}")
            if abs(time.time() - r2['last_update_on']) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {username}")
            r = await self._peer.find_one({'_id': r2['peer_id']},
                                          {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})
            if r is None:
                raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r['last_update_on']) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_phone_number(self, phone_number: str):

        #  _id, access_hash, type,
        r = await self._peer.find_one({'phone_number': phone_number},
                                      {'_id': 1, 'access_hash': 1, 'type': 1})

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def update_dc_address(
        self,
        value: Tuple[int, str, int, bool, bool, bool] = object
    ):
        """
        Updates or inserts a data center address.

        Parameters:
            value (Tuple[int, str, int, bool, bool]): A tuple containing:
                - dc_id (int): Data center ID.
                - address (str): Address of the data center.
                - port (int): Port of the data center.
                - is_ipv6 (bool): Whether the address is IPv6.
                - is_test (bool): Whether it is a test data center.
                - is_media (bool): Whether it is a media data center.
                - is_default_ip (bool): Whether it is the dc IP address provided by library.
        """
        if value == object:
            return

        await self._dc_options.update_one(
            {"$and": [
                {'dc_id': value[0]},
                {'is_ipv6': value[3]},
                {'is_test': value[4]},
                {'is_media': value[5]}
            ]},
            {'$set': {'address': value[1], 'port': value[2], 'is_default_ip': value[6]}},
            upsert=True
        )

    async def get_dc_address(
        self,
        dc_id: int,
        is_ipv6: bool,
        test_mode: bool = False,
        media: bool = False
    ) -> Tuple[str, int]:
        if dc_id in [1,3,5] and media:
            media = False
        if dc_id in [4,5] and test_mode:
            test_mode = False
        r = await self._dc_options.find_one(
            {'dc_id': dc_id, 'is_ipv6': is_ipv6, 'is_test': test_mode, 'is_media': media},
            {'address': 1, 'port': 1, 'is_default_ip': 1}
        )
        if r is None:
            return None
        return r['address'], r['port'], r['is_default_ip']

    async def _get(self):
        attr = inspect.stack()[2].function
        d = await self._session.find_one({'_id': 0}, {attr: 1})
        if not d:
            return
        return d[attr]

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function
        await self._session.update_one({'_id': 0}, {'$set': {attr: value}}, upsert=True)

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

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)
