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
import pyrogram

from datetime import datetime
from pyrogram import raw, types, utils
from pyrogram.errors import FloodWait
from ..object import Object
from typing import List


class Giveaway(Object):
    """A giveaway.

    Parameters:
        chats (List of :obj:`~pyrogram.types.Chat`):
            List of channel(s) which host the giveaway.

        quantity (``int``):
            Quantity of the giveaway prize.

        months (``int``, *optional*):
            How long the telegram premium last (in month).

        stars (``int``, *optional*):
            How many stars the giveaway winner(s) get.

        expire_date (:py:obj:`~datetime.datetime`):
            Date the giveaway winner(s) will be choosen.

        new_subscribers (``bool``):
            True, if the giveaway only for new subscribers.

        additional_price (``str``, *optional*):
            Additional prize for the giveaway winner(s).

        allowed_countries (List of ``str``, *optional*):
            List of ISO country codes which eligible to join the giveaway.

        private_channel_ids (List of ``int``, *optional*):
            List of Unique channel identifier of private channel which host the giveaway.

        is_winners_hidden (``bool``):
            True, if the giveaway winners are hidden.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chats: List["types.Chat"],
        quantity: int,
        expire_date: datetime,
        new_subscribers : bool,
        months: int = None,
        stars: int = None,
        additional_price: str = None,
        allowed_countries: List[str] = None,
        private_channel_ids: List[int] = None,
        is_winners_hidden: bool = None
    ):
        super().__init__(client)

        self.chats = chats
        self.quantity = quantity
        self.months = months
        self.stars = stars
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.additional_price = additional_price
        self.allowed_countries = allowed_countries
        self.private_channel_ids = private_channel_ids
        self.is_winners_hidden = is_winners_hidden

    @staticmethod
    async def _parse(client, message: "raw.types.Message") -> "Giveaway":
        giveaway: "raw.types.MessageMediaGiveaway" = message.media
        chats = []
        private_ids = []
        for raw_chat_id in giveaway.channels:
            chat_id = utils.get_channel_id(raw_chat_id)
            try:
                chat = await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(chat_id)]
                    )
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                private_ids.append(chat_id)
            else:
                chats.append(types.Chat._parse_chat(client, chat.chats[0]))

        return Giveaway(
            chats=chats,
            quantity=giveaway.quantity,
            months=giveaway.months,
            stars=giveaway.stars,
            expire_date=utils.timestamp_to_datetime(giveaway.until_date),
            new_subscribers=giveaway.only_new_subscribers,
            additional_price=giveaway.prize_description,
            allowed_countries=giveaway.countries_iso2 if len(giveaway.countries_iso2) > 0 else None,
            private_channel_ids=private_ids if len(private_ids) > 0 else None,
            is_winners_hidden=not giveaway.winners_are_visible,
            client=client
        )
