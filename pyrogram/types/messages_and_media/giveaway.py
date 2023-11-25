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

import pyrogram

from datetime import datetime
from pyrogram import raw, types, utils
from ..object import Object
from typing import List


class Giveaway(Object):
    """A giveaway.

    Parameters:
        channel_ids (List of ``int``):
            List Unique identifier of the channel(s) which host the giveaway.

        quantity (``int``):
            Quantity of the giveaway prize.

        months (``int``):
            How long the telegram premium last (in month).

        expire_date (:py:obj:`~datetime.datetime`):
            Date the giveaway winner(s) will be choosen.

        new_subscribers (``bool``):
            True, if the giveaway only for new subscribers.

        countries_iso2 (List of ``str``, *optional*):
            List of ISO country codes which eligible to join the giveaway.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        channel_ids: List[int],
        quantity: int,
        months: int,
        expire_date: datetime,
        new_subscribers : bool,
        countries_iso2: List[str] = None
    ):
        super().__init__(client)

        self.channel_ids = channel_ids
        self.quantity = quantity
        self.months = months
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.countries_iso2 = countries_iso2

    @staticmethod
    def _parse(client, message: "raw.types.Message") -> "Giveaway":
        giveaway: "raw.types.MessageMediaGiveaway" = message.media
        channel_ids = []
        for raw_channel_id in giveaway.channels:
            channel_id = utils.get_channel_id(raw_channel_id)
            channel_ids.append(channel_id)

        return Giveaway(
            channel_ids=channel_ids,
            quantity=giveaway.quantity,
            months=giveaway.months,
            expire_date=utils.timestamp_to_datetime(giveaway.until_date),
            new_subscribers=giveaway.only_new_subscribers,
            countries_iso2=giveaway.countries_iso2 if len(giveaway.countries_iso2) > 0 else None,
            client=client
        )
