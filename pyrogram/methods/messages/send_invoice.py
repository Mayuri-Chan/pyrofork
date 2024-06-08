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

from pyrogram import types, raw, utils
from typing import Union, List

class SendInvoice:
    async def send_invoice(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        title: str,
        description: str,
        currency: str,
        prices: List["types.LabeledPrice"],
        provider: str = None,
        provider_data: str = None,
        photo_url: str = None,
        photo_size: int = None,
        photo_mime_type: str = None,
        start_parameter: str = None,
        extended_media: "types.InputMedia" = None,
        reply_to_message_id: int = None,
        message_thread_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
    ):
        """Use this method to send invoices.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target private chat or username of the target private chat.

            title (``str``):
                Product name.

            description (``str``):
                Product description.

            currency (``str``):
                Three-letter ISO 4217 currency code.

            prices (List of :obj:`~pyrogram.types.LabeledPrice`):
                Price with label.

            provider (``str``, *optional*):
                Payment provider.

            provider_data (``str``, *optional*):
                Provider data in json format.

            photo_url (``str``, *optional*):
                Photo URL.

            photo_size (``int``, *optional*):
                Photo size.

            photo_mime_type (``str``, *optional*):
                Photo MIME type.

            start_parameter (``str``, *optional*):
                Unique bot deep-linking parameter that can be used to generate this invoice.

            extended_media (:obj:`~pyrogram.types.InputMedia`, *optional*):
                Additional media.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        Example:
            .. code-block:: python

                app.send_invoice(chat_id, types.InputMediaInvoice(
                    title="Product Name",
                    description="Product Description",
                    currency="USD",
                    prices=[types.LabeledPrice("Product", 1000)],
                    provider="Stripe",
                    provider_data="{}"
                ))
        """

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
            quote_text=quote_text,
            quote_entities=quote_entities
        )

        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaInvoice(
                    title=title,
                    description=description,
                    invoice=raw.types.Invoice(
                        currency=currency,
                        prices=[price.write() for price in prices]
                    ),
                    payload=f"{(title)}".encode(),
                    provider=provider,
                    provider_data=raw.types.DataJSON(data=provider_data if provider_data else "{}"),
                    photo=raw.types.InputWebDocument(
                        url=photo_url,
                        size=photo_size or 0,
                        mime_type=photo_mime_type or "image/jpeg",
                        attributes=[]
                    ) if photo_url else None,
                    start_param=start_parameter,
                    extended_media=extended_media
                ),
                random_id=self.rnd_id(),
                reply_to=reply_to,
                message=""
            )
        )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage
                )
            ):
                return types.Message._parse(
                    self,
                    i.message,
                    users={i.id: i for i in r.users},
                    chats={i.id: i for i in r.chats}
                )
