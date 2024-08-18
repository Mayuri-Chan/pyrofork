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

from ..object import Object
from pyrogram import types, utils


class GiftCode(Object):
    """A service message about a gift code.

    parameters:
        months (``int``):
            How long the telegram premium last (in month).

        slug (``str``):
            The slug of the gift code.

        is_giveaway (``bool``, *optional*):
            True, if the gift code is from a giveaway.

        is_unclaimed (``bool``, *optional*):
            True, if the gift code is unclaimed.

        boosted_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The chat that the gift code boost.

        currency (``str``, *optional*):
            The currency of the gift code.

        amount (``int``, *optional*):
            The amount of the gift code.

        crypto_currency (``str``, *optional*):
            The crypto currency of the gift code.

        crypto_amount (``int``, *optional*):
            The crypto amount of the gift code.
    """

    def __init__(
        self,
        months: int,
        slug: str,
        is_giveaway: bool = None,
        is_unclaimed: bool = None,
        boosted_chat: "types.Chat" = None,
        currency: str = None,
        amount: int = None,
        crypto_currency: str = None,
        crypto_amount: int = None
    ):
        super().__init__()
        self.months = months
        self.slug = slug
        self.is_giveaway = is_giveaway
        self.is_unclaimed = is_unclaimed
        self.boosted_chat = boosted_chat
        self.currency = currency
        self.amount = amount
        self.crypto_currency = crypto_currency
        self.crypto_amount = crypto_amount

    @staticmethod
    def _parse(client: "pyrogram.Client", gift_code: "types.GiftCode", chats: dict,) -> "GiftCode":
        boosted_chat = None
        boosted_chat_raw = chats.get(utils.get_raw_peer_id(gift_code.boost_peer), None)
        if boosted_chat_raw:
            boosted_chat = types.Chat._parse_channel_chat(client, boosted_chat_raw)

        return GiftCode(
            months=gift_code.months,
            slug=gift_code.slug,
            is_giveaway=gift_code.via_giveaway,
            is_unclaimed=gift_code.unclaimed,
            boosted_chat=boosted_chat,
            currency=gift_code.currency,
            amount=gift_code.amount,
            crypto_currency=gift_code.crypto_currency,
            crypto_amount=gift_code.crypto_amount
        )
