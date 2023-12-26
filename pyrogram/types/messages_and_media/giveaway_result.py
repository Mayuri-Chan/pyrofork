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


class GiveawayResult(Object):
    """A giveaway result.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Channel which host the giveaway.

        giveaway_message (:obj:`~pyrogram.types.Message`):
            The original giveaway message.

        quantity (``int``):
            Quantity of the giveaway prize.

        unclaimed_quantity (``int``):
            Quantity of unclaimed giveaway prize.

        winners (List of :obj:`~pyrogram.types.User`):
            The giveaway winners.

        months (``int``):
            How long the telegram premium last (in month).

        expire_date (:py:obj:`~datetime.datetime`):
            Date the giveaway winner(s) choosen.

        new_subscribers (``bool``, *optional*):
            True, if the giveaway only for new subscribers.

        is_refunded (``bool``, *optional*):
            True, if the giveaway was refunded.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        giveaway_message: "types.Message",
        quantity: int,
        unclaimed_quantity: int,
        winners: List["types.User"],
        months: int,
        expire_date: datetime,
        new_subscribers : bool,
        is_refunded: bool = None
    ):
        super().__init__(client)

        self.chat = chat
        self.giveaway_message = giveaway_message
        self.quantity = quantity
        self.unclaimed_quantity = unclaimed_quantity
        self.winners = winners
        self.months = months
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.is_refunded = is_refunded

    @staticmethod
    async def _parse(client, message: "raw.types.Message") -> "GiveawayResult":
        giveaway_result: "raw.types.MessageMediaGiveawayResults" = message.media
        chat_id = utils.get_channel_id(giveaway_result.channel_id)
        chat = await client.invoke(
            raw.functions.channels.GetChannels(
                id=[await client.resolve_peer(chat_id)]
            )
        )
        chat = types.Chat._parse_chat(client, chat.chats[0])
        giveaway_message = await client.get_messages(chat_id, giveaway_result.launch_msg_id)
        winners = []
        for winner in giveaway_result.winners:
            winners.append(await client.get_users(winner))

        return GiveawayResult(
            chat=chat,
            giveaway_message=giveaway_message,
            quantity=giveaway_result.winners_count,
            unclaimed_quantity=giveaway_result.unclaimed_count,
            winners=winners,
            months=giveaway_result.months,
            expire_date=utils.timestamp_to_datetime(giveaway_result.until_date),
            new_subscribers=giveaway_result.only_new_subscribers,
            is_refunded=giveaway_result.refunded,
            client=client
        )
