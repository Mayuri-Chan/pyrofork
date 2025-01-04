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

from datetime import datetime
from typing import Optional, List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from ..object import Object


class StarGift(Object):
    """A star gift.

    Parameters:
        id (``int``):
            Unique star gift identifier.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Information about the star gift sticker.

        caption (``str``, *optional*):
            Text message.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        message_id (``int``, *optional*):
            Unique message identifier.

        upgrade_message_id (``int``, *optional*):
            Unique message identifier.
            For unique gifts only.

        title (``str``, *optional*):
            Title of the star gift.
            For unique gifts only.

        number (``int``, *optional*):
            Collectible number of the star gift.
            For unique gifts only.

        model (:obj:`~pyrogram.types.StarGiftAttribute`, *optional*):
            Information about the star gift model.
            For unique gifts only.

        backdrop (:obj:`~pyrogram.types.StarGiftAttribute`, *optional*):
            Information about the star gift backdrop.
            For unique gifts only.

        symbol (:obj:`~pyrogram.types.StarGiftAttribute`, *optional*):
            Information about the star gift symbol.
            For unique gifts only.

        date (``datetime``, *optional*):
            Date when the star gift was received.

        first_sale_date (``datetime``, *optional*):
            Date when the star gift was first purchased.

        last_sale_date (``datetime``, *optional*):
            Date when the star gift was last purchased.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            User who sent the star gift.

        price (``int``, *optional*):
            Price of this gift in stars.

        convert_price (``int``, *optional*):
            The number of stars you get if you convert this gift.

        upgrade_price (``int``, *optional*):
            The number of stars you need to upgrade this gift.

        transfer_price (``int``, *optional*):
            The number of stars you need to transfer this gift.

        available_amount (``int``, *optional*):
            The number of gifts available for purchase.
            Returned only if is_limited is True.

        total_amount (``int``, *optional*):
            Total amount of gifts.
            Returned only if is_limited is True.

        can_upgrade (``bool``, *optional*):
            True, if the gift can be upgraded.

        can_export_at (``datetime``, *optional*):
            Date when the gift can be exported via blockchain.

        is_limited (``bool``, *optional*):
            True, if the number of gifts is limited.

        is_name_hidden (``bool``, *optional*):
            True, if the sender's name is hidden.

        is_saved (``bool``, *optional*):
            True, if the star gift is saved in profile.

        is_sold_out (``bool``, *optional*):
            True, if the star gift is sold out.

        is_converted (``bool``, *optional*):
            True, if the gift was converted to Telegram Stars.
            Only for the receiver of the gift.

        is_upgraded (``bool``, *optional*):
            True, if the gift was upgraded.

        is_refunded (``bool``, *optional*):
            True, if the gift was refunded.

        is_transferred (``bool``, *optional*):
            True, if the gift was transferred.

        is_unique (``bool``, *optional*):
            True, if the gift is unique.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        sticker: "types.Sticker" = None,
        caption: Optional[str] = None,
        caption_entities: List["types.MessageEntity"] = None,
        message_id: Optional[int] = None,
        date: Optional[datetime] = None,
        first_sale_date: Optional[datetime] = None,
        last_sale_date: Optional[datetime] = None,
        from_user: Optional["types.User"] = None,
        price: Optional[int] = None,
        convert_price: Optional[int] = None,
        upgrade_price: Optional[int] = None,
        transfer_price: Optional[int] = None,
        upgrade_message_id: Optional[int] = None,
        title: Optional[str] = None,
        number: Optional[int] = None,
        model: Optional["types.StarGiftAttribute"] = None,
        backdrop: Optional["types.StarGiftAttribute"] = None,
        symbol: Optional["types.StarGiftAttribute"] = None,
        available_amount: Optional[int] = None,
        total_amount: Optional[int] = None,
        can_upgrade: Optional[bool] = None,
        can_export_at: Optional[datetime] = None,
        is_limited: Optional[bool] = None,
        is_name_hidden: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        is_sold_out: Optional[bool] = None,
        is_converted: Optional[bool] = None,
        is_upgraded: Optional[bool] = None,
        is_refunded: Optional[bool] = None,
        is_transferred: Optional[bool] = None,
        is_unique: Optional[bool] = None
    ):
        super().__init__(client)

        self.id = id
        self.sticker = sticker
        self.caption = caption
        self.caption_entities = caption_entities
        self.message_id = message_id
        self.date = date
        self.first_sale_date = first_sale_date
        self.last_sale_date = last_sale_date
        self.from_user = from_user
        self.price = price
        self.convert_price = convert_price
        self.upgrade_price = upgrade_price
        self.transfer_price = transfer_price
        self.upgrade_message_id = upgrade_message_id
        self.title = title
        self.number = number
        self.model = model
        self.backdrop = backdrop
        self.symbol = symbol
        self.available_amount = available_amount
        self.total_amount = total_amount
        self.can_upgrade = can_upgrade
        self.can_export_at = can_export_at
        self.is_limited = is_limited
        self.is_name_hidden = is_name_hidden
        self.is_saved = is_saved
        self.is_sold_out = is_sold_out
        self.is_converted = is_converted
        self.is_upgraded = is_upgraded
        self.is_refunded = is_refunded
        self.is_transferred = is_transferred
        self.is_unique = is_unique

    @staticmethod
    async def _parse(
        client,
        star_gift: "raw.types.StarGift",
    ) -> "StarGift":
        doc = star_gift.sticker
        attributes = {type(i): i for i in doc.attributes}

        return StarGift(
            id=star_gift.id,
            sticker=await types.Sticker._parse(client, doc, attributes),
            price=star_gift.stars,
            convert_price=star_gift.convert_stars,
            available_amount=getattr(star_gift, "availability_remains", None),
            total_amount=getattr(star_gift, "availability_total", None),
            is_limited=getattr(star_gift, "limited", None),
            first_sale_date=utils.timestamp_to_datetime(getattr(star_gift, "first_sale_date", None)),
            last_sale_date=utils.timestamp_to_datetime(getattr(star_gift, "last_sale_date", None)),
            is_sold_out=getattr(star_gift, "sold_out", None),
            client=client
        )

    @staticmethod
    async def _parse_user_star_gift(
        client,
        user_star_gift: "raw.types.UserStarGift",
        users: dict
    ) -> "StarGift":
        caption, caption_entities = (
            utils.parse_text_with_entities(
                client, getattr(user_star_gift, "message", None), users
            )
        ).values()


        if isinstance(user_star_gift.gift, raw.types.StarGift):
            doc = user_star_gift.gift.sticker
            attributes = {type(i): i for i in doc.attributes}

            return StarGift(
                id=user_star_gift.gift.id,
                sticker=await types.Sticker._parse(client, doc, attributes),
                price=user_star_gift.gift.stars,
                convert_price=user_star_gift.gift.convert_stars,
                available_amount=getattr(user_star_gift.gift, "availability_remains", None),
                total_amount=getattr(user_star_gift.gift, "availability_total", None),
                date=utils.timestamp_to_datetime(user_star_gift.date),
                is_limited=getattr(user_star_gift.gift, "limited", None),
                is_name_hidden=getattr(user_star_gift, "name_hidden", None),
                is_saved=not user_star_gift.unsaved if getattr(user_star_gift, "unsaved", None) else None,
                is_refunded=getattr(user_star_gift, "refunded", None),
                can_upgrade=getattr(user_star_gift, "can_upgrade", None),
                can_export_at=utils.timestamp_to_datetime(getattr(user_star_gift, "can_export_at", None)),
                upgrade_price=getattr(user_star_gift, "upgrade_stars", None),
                transfer_price=getattr(user_star_gift, "transfer_stars", None),
                from_user=types.User._parse(client, users.get(user_star_gift.from_id)) if getattr(user_star_gift, "from_id", None) else None,
                message_id=getattr(user_star_gift, "msg_id", None),
                caption=caption,
                caption_entities=caption_entities,
                client=client
            )
        elif isinstance(user_star_gift.gift, raw.types.StarGiftUnique):
            gift = user_star_gift.gift
            attributes = {type(i): i for i in gift.attributes}

            model = None
            backdrop = None
            symbol = None

            for key, value in attributes.items():
                if isinstance(key, raw.types.StarGiftAttributeModel):
                    model = await types.StarGiftAttribute._parse(client, value)
                elif isinstance(key, raw.types.StarGiftAttributeBackdrop):
                    backdrop = await types.StarGiftAttribute._parse(client, value)
                elif isinstance(key, raw.types.StarGiftAttributePattern):
                    symbol = await types.StarGiftAttribute._parse(client, value)

            return StarGift(
                id=user_star_gift.gift.id,
                available_amount=getattr(user_star_gift.gift, "availability_issued", None),
                total_amount=getattr(user_star_gift.gift, "availability_total", None),
                date=utils.timestamp_to_datetime(user_star_gift.date),
                model=model,
                backdrop=backdrop,
                symbol=symbol,
                title=gift.title,
                number=gift.num,
                is_unique=True,
                is_name_hidden=getattr(user_star_gift, "name_hidden", None),
                is_saved=not user_star_gift.unsaved if getattr(user_star_gift, "unsaved", None) else None,
                is_refunded=getattr(user_star_gift, "refunded", None),
                can_upgrade=getattr(user_star_gift, "can_upgrade", None),
                can_export_at=utils.timestamp_to_datetime(getattr(user_star_gift, "can_export_at", None)),
                upgrade_price=getattr(user_star_gift, "upgrade_stars", None),
                transfer_price=getattr(user_star_gift, "transfer_stars", None),
                from_user=types.User._parse(client, users.get(user_star_gift.from_id)) if getattr(user_star_gift, "from_id", None) else None,
                message_id=getattr(user_star_gift, "msg_id", None),
                caption=caption,
                caption_entities=caption_entities,
                client=client
            )

    @staticmethod
    async def _parse_action(
        client,
        message: "raw.base.Message",
        users: dict
    ) -> "StarGift":
        action = message.action  # type: raw.types.MessageActionStarGift

        caption, caption_entities = (
            utils.parse_text_with_entities(
                client, getattr(action, "message", None), users
            )
        ).values()

        if isinstance(action, raw.types.MessageActionStarGift):
            doc = action.gift.sticker
            attributes = {type(i): i for i in doc.attributes}

            return StarGift(
                id=action.gift.id,
                sticker=await types.Sticker._parse(client, doc, attributes),
                price=action.gift.stars,
                convert_price=action.gift.convert_stars,
                available_amount=getattr(action.gift, "availability_remains", None),
                total_amount=getattr(action.gift, "availability_total", None),
                date=utils.timestamp_to_datetime(message.date),
                can_upgrade=getattr(action, "can_upgrade", None),
                is_limited=getattr(action.gift, "limited", None),
                is_name_hidden=getattr(action, "name_hidden", None),
                is_saved=getattr(action, "saved", None),
                is_converted=getattr(action, "converted", None),
                is_upgraded=getattr(action, "upgraded", None),
                is_refunded=getattr(action, "refunded", None),
                from_user=types.User._parse(client, users.get(utils.get_raw_peer_id(message.peer_id))),
                message_id=message.id,
                upgrade_message_id=getattr(action, "upgrade_msg_id", None),
                upgrade_price=getattr(action, "upgrade_stars", None),
                caption=caption,
                caption_entities=caption_entities,
                client=client
            )
        elif isinstance(action, raw.types.MessageActionStarGiftUnique):
            gift = action.gift
            attributes = {type(i): i for i in gift.attributes}

            model = None
            backdrop = None
            symbol = None

            for key, value in attributes.items():
                if isinstance(key, raw.types.StarGiftAttributeModel):
                    model = await types.StarGiftAttribute._parse(client, value)
                elif isinstance(key, raw.types.StarGiftAttributeBackdrop):
                    backdrop = await types.StarGiftAttribute._parse(client, value)
                elif isinstance(key, raw.types.StarGiftAttributePattern):
                    symbol = await types.StarGiftAttribute._parse(client, value)

            return StarGift(
                id=action.gift.id,
                available_amount=getattr(action.gift, "availability_issued", None),
                total_amount=getattr(action.gift, "availability_total", None),
                date=utils.timestamp_to_datetime(message.date),
                is_unique=True,
                from_user=types.User._parse(client, users.get(utils.get_raw_peer_id(message.peer_id))),
                message_id=message.id,
                caption=caption,
                caption_entities=caption_entities,
                title=gift.title,
                number=gift.num,
                model=model,
                backdrop=backdrop,
                symbol=symbol,
                is_upgraded=getattr(action, "upgrade", None),
                is_transferred=getattr(action, "transferred", None),
                is_saved=getattr(action, "saved", None),
                is_refunded=getattr(action, "refunded", None),
                can_export_at=utils.timestamp_to_datetime(getattr(action, "can_export_at", None)),
                transfer_price=getattr(action, "transfer_stars", None),
                client=client
            )

    async def show(self) -> bool:
        """Bound method *show* of :obj:`~pyrogram.types.StarGift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.show_star_gift(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await star_gift.show()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.show_star_gift(
            chat_id=self.from_user.id,
            message_id=self.message_id
        )

    async def hide(self) -> bool:
        """Bound method *hide* of :obj:`~pyrogram.types.StarGift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.hide_star_gift(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await star_gift.hide()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.hide_star_gift(
            chat_id=self.from_user.id,
            message_id=self.message_id
    )
