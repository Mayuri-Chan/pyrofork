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

from datetime import datetime
from pyrogram import raw, types, utils
from ..object import Object

class StarsTransaction(Object):
    """Contains information about stars transaction.

    Parameters:
        id (``int``):
            Unique transaction identifier.

        stars (``int``):
            Amount of stars in the transaction.

        date (:py:obj:`~datetime.datetime`):
            Date of the transaction.

        chat (:obj:`~pyrogram.types.Chat`):
            Chat where the transaction was made.

        is_refund (``bool``, *optional*):
            True, If the transaction is a refund.

        is_pending (``bool``, *optional*):
            True, If the transaction is pending.

        is_failed (``bool``, *optional*):
            True, If the transaction failed.

        title (``str``, *optional*):
            Title of the transaction.

        description (``str``, *optional*):
            Description of the transaction.

        transaction_date (:py:obj:`~datetime.datetime`, *optional*):
            Date of the transaction.

        transaction_url (``str``, *optional*):
            URL of the transaction.

        payload (``str``, *optional*):
            Payload of the transaction.

        message_id (``int``, *optional*):
            Identifier of the message where the transaction was made.
    """ # TODO photo, extended_media
    def __init__(
        self,
        *,
        id: int,
        stars: int,
        date: datetime,
        chat: "types.Chat",
        is_refund: bool = None,
        is_pending: bool = None,
        is_failed: bool = None,
        title: str = None,
        description: str = None,
        transaction_date: datetime = None,
        transaction_url: str = None,
        payload: str = None,
        message_id: int = None
    ):
        super().__init__()

        self.id = id
        self.stars = stars
        self.date = date
        self.chat = chat
        self.is_refund = is_refund
        self.is_pending = is_pending
        self.is_failed = is_failed
        self.title = title
        self.description = description
        self.transaction_date = transaction_date
        self.transaction_url = transaction_url
        self.payload = payload
        self.message_id = message_id
    
    @staticmethod
    def _parse(
        client,
        transaction: "raw.types.StarsTransaction",
        users: dict
    ) -> "StarsTransaction":
        chat_id = utils.get_raw_peer_id(transaction.peer.peer)
        chat = types.User._parse(client, users.get(chat_id, None))
        try:
            payload = transaction.bot_payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = transaction.bot_payload
        return StarsTransaction(
            id=transaction.id,
            stars=transaction.stars,
            date=utils.timestamp_to_datetime(transaction.date),
            chat=chat,
            is_refund=transaction.refund,
            is_pending=transaction.pending,
            is_failed=transaction.failed,
            title=transaction.title,
            description=transaction.description,
            transaction_date=utils.timestamp_to_datetime(transaction.transaction_date),
            transaction_url=transaction.transaction_url,
            payload=payload,
            message_id=transaction.msg_id
    )
