#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import List, Union

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class CreateInvoiceLink:
    async def create_invoice_link(
        self: "pyrogram.Client",
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: Union["types.LabeledPrice", List["types.LabeledPrice"]],
        provider_token: str = None,
        start_parameter: str = None,
        provider_data: str = None,
        photo_url: str = None,
        photo_size: int = None,
        photo_width: int = None,
        photo_height: int = None,
        need_name: bool = None,
        need_phone_number: bool = None,
        need_email: bool = None,
        need_shipping_address: bool = None,
        send_phone_number_to_provider: bool = None,
        send_email_to_provider: bool = None,
        is_flexible: bool = None
    ) -> str:
        """Use this method to create a link for an invoice.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            title (``str``):
                Product name, 1-32 characters.

            description (``str``):
                Product description, 1-255 characters

            payload (``str`` | ``bytes``):
                Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.

            currency (``str``):
                Three-letter ISO 4217 currency code, see `more on currencies <https://core.telegram.org/bots/payments#supported-currencies>`_. Pass ``XTR`` for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            prices (:obj:`~pyrogram.types.LabeledPrice` | List of :obj:`~pyrogram.types.LabeledPrice`):
                Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in `Telegram Stars <https://t.me/BotNews/90>`_.
                If you add multiple prices, the prices will be added up.
                For stars invoice you can only have one item.

            provider_token (``str``, *optional*):
                Payment provider token, obtained via `@BotFather <https://t.me/botfather>`_. Pass an empty string for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            start_parameter (``str``, *optional*):
                Unique deep-linking parameter. If left empty, **forwarded copies** of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter.

            provider_data (``str``, *optional*):
                JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.

            photo_url (``str``, *optional*):
                URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.

            photo_size (``int``, *optional*):
                Photo size in bytes

            photo_width (``int``, *optional*):
                Photo width

            photo_height (``int``, *optional*):
                Photo height

            need_name (``bool``, *optional*):
                Pass True if you require the user's full name to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_phone_number (``bool``, *optional*):
                Pass True if you require the user's phone number to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_email (``bool``, *optional*):
                Pass True if you require the user's email address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_shipping_address (``bool``, *optional*):
                Pass True if you require the user's shipping address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            send_phone_number_to_provider (``bool``, *optional*):
                Pass True if the user's phone number should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            send_email_to_provider (``bool``, *optional*):
                Pass True if the user's email address should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            is_flexible (``bool``, *optional*):
                Pass True if the final price depends on the shipping method. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        Returns:
            ``str``: On success, the created invoice link is returned.

        """

        is_iterable = not isinstance(prices, types.LabeledPrice)

        rpc = raw.functions.payments.ExportInvoice(
            invoice_media=raw.types.InputMediaInvoice(
                title=title,
                description=description,
                photo=raw.types.InputWebDocument(
                    url=photo_url,
                    mime_type="image/jpg",
                    size=photo_size,
                    attributes=[
                        raw.types.DocumentAttributeImageSize(
                            w=photo_width,
                            h=photo_height
                        )
                    ]
                ) if photo_url else None,
                invoice=raw.types.Invoice(
                    currency=currency,
                    prices=[i.write() for i in prices] if is_iterable else [prices.write()],
                    test=self.test_mode,
                    name_requested=need_name,
                    phone_requested=need_phone_number,
                    email_requested=need_email,
                    shipping_address_requested=need_shipping_address,
                    flexible=is_flexible,
                    phone_to_provider=send_phone_number_to_provider,
                    email_to_provider=send_email_to_provider
                ),
                payload=payload.encode() if isinstance(payload, str) else payload,
                provider=provider_token,
                provider_data=raw.types.DataJSON(
                    data=provider_data if provider_data else "{}"
                ),
                start_param=start_parameter
            )
        )
        r = await self.invoke(rpc)
        return r.url
