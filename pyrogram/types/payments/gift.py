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
from typing import List, Optional, Union

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class Gift(Object):
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

        name (``str``, *optional*):
            Name of the star gift.
            For unique gifts only.

        title (``str``, *optional*):
            Title of the star gift.
            For unique gifts only.

        collectible_id (``int``, *optional*):
            Collectible number of the star gift.
            For unique gifts only.

        attributes (List of :obj:`~pyrogram.types.GiftAttribute`, *optional*):
            Attributes of the star gift.
            For unique gifts only.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the star gift was received.

        first_sale_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the star gift was first purchased.

        last_sale_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the star gift was last purchased.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            User who sent the star gift.

        owner (:obj:`~pyrogram.types.Chat`, *optional*):
            Current gift owner.

        owner_name (``str``, *optional*):
            Name of the user who received the star gift.

        owner_address (``str``, *optional*):
            Address of the gift owner in TON blockchain.

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

        can_export_at (:py:obj:`~datetime.datetime`, *optional*):
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

        is_birthday (``bool``, *optional*):
            True, if the gift is a birthday gift.

        raw (:obj:`~pyrogram.raw.base.StarGift`, *optional*):
            The raw object as received from the server.
            
        link (``str``, *property*):
            A link to the gift.
            For unique gifts only.
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
        owner: Optional["types.Chat"] = None,
        owner_name: Optional[str] = None,
        owner_address: Optional[str] = None,
        price: Optional[int] = None,
        convert_price: Optional[int] = None,
        upgrade_price: Optional[int] = None,
        transfer_price: Optional[int] = None,
        upgrade_message_id: Optional[int] = None,
        name: Optional[str] = None,
        title: Optional[str] = None,
        collectible_id: Optional[int] = None,
        attributes: Optional[List["types.GiftAttribute"]] = None,
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
        is_birthday: Optional[bool] = None,
        raw: Optional["raw.base.StarGift"] = None
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
        self.owner = owner
        self.owner_name = owner_name
        self.owner_address = owner_address
        self.price = price
        self.convert_price = convert_price
        self.upgrade_price = upgrade_price
        self.transfer_price = transfer_price
        self.upgrade_message_id = upgrade_message_id
        self.name = name
        self.title = title
        self.collectible_id = collectible_id
        self.attributes = attributes
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
        self.is_birthday = is_birthday
        self.raw = raw

    @staticmethod
    async def _parse(client, gift, users={}, chats={}):
        if isinstance(gift, raw.types.StarGift):
            return await Gift._parse_regular(client, gift)
        elif isinstance(gift, raw.types.StarGiftUnique):
            return await Gift._parse_unique(client, gift, users, chats)
        elif isinstance(gift, raw.types.StarGiftSaved):
            return await Gift._parse_saved(client, gift, users, chats)
    
    @staticmethod
    async def _parse_regular(
        client,
        star_gift: "raw.types.StarGift",
    ) -> "Gift":
        doc = star_gift.sticker
        attributes = {type(i): i for i in doc.attributes}

        return Gift(
            id=star_gift.id,
            sticker=await types.Sticker._parse(client, doc, attributes),
            price=star_gift.stars,
            convert_price=star_gift.convert_stars,
            upgrade_price=getattr(star_gift, "upgrade_stars", None),
            available_amount=getattr(star_gift, "availability_remains", None),
            total_amount=getattr(star_gift, "availability_total", None),
            is_limited=getattr(star_gift, "limited", None),
            is_sold_out=getattr(star_gift, "sold_out", None),
            is_birthday=getattr(star_gift, "birthday", None),
            first_sale_date=utils.timestamp_to_datetime(getattr(star_gift, "first_sale_date", None)),
            last_sale_date=utils.timestamp_to_datetime(getattr(star_gift, "last_sale_date", None)),
            raw=star_gift,
            client=client
        )

    @staticmethod
    async def _parse_unique(
        client,
        star_gift: "raw.types.StarGiftUnique",
        users: dict = {},
        chats: dict = {}
    ) -> "Gift":
        owner_id = utils.get_raw_peer_id(getattr(star_gift, "owner_id", None))
        return Gift(
            id=star_gift.id,
            name=star_gift.slug,
            title=star_gift.title,
            collectible_id=star_gift.num,
            attributes=types.List(
                [await types.GiftAttribute._parse(client, attr, users, chats) for attr in star_gift.attributes]
            ) or None,
            available_amount=getattr(star_gift, "availability_issued", None),
            total_amount=getattr(star_gift, "availability_total", None),
            owner=types.Chat._parse_chat(client, users.get(owner_id) or chats.get(owner_id)),
            owner_name=getattr(star_gift, "owner_name", None),
            owner_address=getattr(star_gift, "owner_address", None),
            is_upgraded=True,
            raw=star_gift,
            client=client
        )

    @staticmethod
    async def _parse_saved(
        client,
        saved_gift: "raw.types.SavedStarGift",
        users: dict = {},
        chats: dict = {}
    ) -> "Gift":
        caption, caption_entities = (
            utils.parse_text_with_entities(
                client, getattr(saved_gift, "message", None), users
            )
        ).values()

        if isinstance(saved_gift.gift, raw.types.StarGift):
            parsed_gift = await Gift._parse_regular(client, saved_gift.gift)
        elif isinstance(saved_gift.gift, raw.types.StarGiftUnique):
            parsed_gift = await Gift._parse_unique(client, saved_gift.gift, users, chats)
        parsed_gift.date = utils.timestamp_to_datetime(saved_gift.date)
        parsed_gift.is_name_hidden = getattr(saved_gift, "name_hidden", None)
        parsed_gift.is_saved = not saved_gift.unsaved if getattr(saved_gift, "unsaved", None) else None
        parsed_gift.is_refunded = getattr(saved_gift, "refunded", None)
        parsed_gift.can_upgrade = getattr(saved_gift, "can_upgrade", None)
        parsed_gift.from_user = types.User._parse(client, users.get(utils.get_raw_peer_id(saved_gift.from_id), None))
        parsed_gift.caption = caption
        parsed_gift.caption_entities = caption_entities
        parsed_gift.message_id = getattr(saved_gift, "msg_id", None)
        parsed_gift.saved_id = getattr(saved_gift, "saved_id", None)
        parsed_gift.convert_price = getattr(saved_gift, "convert_stars", None)
        parsed_gift.upgrade_price = getattr(saved_gift, "upgrade_stars", None)
        parsed_gift.transfer_price = getattr(saved_gift, "transfer_stars", None)
        parsed_gift.can_export_at = utils.timestamp_to_datetime(getattr(saved_gift, "can_export_at", None))

        return parsed_gift


    @staticmethod
    async def _parse_action(
        client,
        message: "raw.base.Message",
        users: dict = {},
        chats: dict = {}
    ) -> "Gift":
        action = message.action  # type: raw.types.MessageActionStarGift

        if isinstance(action, raw.types.MessageActionStarGift):
            parsed_gift = await Gift._parse_regular(client, action.gift)

            caption, caption_entities = (
                utils.parse_text_with_entities(
                    client, getattr(action, "message", None), users
                )
            ).values()

            parsed_gift.is_name_hidden = getattr(action, "name_hidden", None)
            parsed_gift.is_saved = getattr(action, "saved", None)
            parsed_gift.is_converted = getattr(action, "converted", None)
            parsed_gift.is_upgraded = getattr(action, "upgraded", None)
            parsed_gift.is_refunded = getattr(action, "refunded", None)
            parsed_gift.can_upgrade = getattr(action, "can_upgrade", None)
            parsed_gift.caption = caption
            parsed_gift.caption_entities = caption_entities
            parsed_gift.convert_price = getattr(action, "convert_stars", None)
            parsed_gift.upgrade_price = getattr(action, "upgrade_stars", None)
            parsed_gift.message_id = getattr(action, "saved_id", message.id)
            parsed_gift.upgrade_message_id = getattr(action, "upgrade_msg_id", None)
        elif isinstance(action, raw.types.MessageActionStarGiftUnique):
            parsed_gift = await Gift._parse_unique(client, action.gift, users, chats)

            parsed_gift.is_upgraded = getattr(action, "upgrade", None)
            parsed_gift.is_transferred = getattr(action, "transferred", None)
            parsed_gift.is_saved = getattr(action, "saved", None)
            parsed_gift.is_refunded = getattr(action, "refunded", None)
            parsed_gift.can_export_at = utils.timestamp_to_datetime(getattr(action, "can_export_at", None))
            parsed_gift.transfer_price = getattr(action, "transfer_stars", None)
            parsed_gift.message_id = getattr(action, "saved_id", None)
            parsed_gift.upgrade_message_id = message.id

        parsed_gift.date = utils.timestamp_to_datetime(message.date)

        return parsed_gift

    @property
    def link(self) -> Optional[str]:
        if not self.name:
            return None
        return f"https://t.me/nft/{self.name}"
    
    async def show(self) -> bool:
        """Bound method *show* of :obj:`~pyrogram.types.Gift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.show_gift(
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await gift.show()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.show_gift(
            message_id=self.message_id
        )

    async def hide(self) -> bool:
        """Bound method *hide* of :obj:`~pyrogram.types.Gift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.hide_gift(
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await gift.hide()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.hide_gift(
            message_id=self.message_id
        )

    async def convert(self) -> bool:
        """Bound method *convert* of :obj:`~pyrogram.types.Gift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.convert_gift(
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await gift.convert()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.convert_gift(
            message_id=self.message_id
        )

    async def upgrade(self) -> bool:
        """Bound method *upgrade* of :obj:`~pyrogram.types.Gift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.upgrade_gift(
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await gift.upgrade()

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.upgrade_gift(
            message_id=self.message_id
        )

    async def transfer(self, to_chat_id: Union[int, str]) -> bool:
        """Bound method *transfer* of :obj:`~pyrogram.types.Gift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.transfer_gift(
                message_id=message_id,
                to_chat_id=to_chat_id
            )

        Example:
            .. code-block:: python

                await gift.transfer(to_chat_id=123)

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self._client.transfer_gift(
            message_id=self.message_id,
            to_chat_id=to_chat_id
    )

    async def wear(self) -> bool:
        """Bound method *wear* of :obj:`~pyrogram.types.Gift`.
       
        .. note::
        
            This works for upgraded gifts only.
       
        Use as a shortcut for:
        
        .. code-block:: python
        
            await client.set_emoji_status(types.EmojiStatus(gift_id=123))
        
        Example:
            .. code-block:: python
            
                await star_gift.wear()
                
        Returns:
            ``bool``: On success, True is returned.
        """
        return self._client.set_emoji_status(
            emoji_status=types.EmojiStatus(
                gift_id=self.id
            )
        )
