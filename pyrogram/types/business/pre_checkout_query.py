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


import pyrogram
from pyrogram import raw, types
from typing import Dict
from ..object import Object
from ..update import Update


class PreCheckoutQuery(Object, Update):
    """An incoming pre-checkout query from a buy button in an inline keyboard.

    Parameters:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`~pyrogram.types.User`):
            User who sent the query.

        currency (``str``):
            Three-letter ISO 4217 currency code.

        total_amount (``int``):
            Total price in the smallest units of the currency.

        payload (``str``):
            Bot specified invoice payload.

        shipping_option_id (``str``, *optional*):
            Identifier of the shipping option chosen by the user.

        payment_info (:obj:`~pyrogram.types.PaymentInfo`, *optional*):
            Payment information provided by the user.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        from_user: "types.User",
        currency: str,
        total_amount: int,
        payload: str,
        shipping_option_id: str = None,
        payment_info: "types.PaymentInfo" = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.payload = payload
        self.shipping_option_id = shipping_option_id
        self.payment_info = payment_info

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        pre_checkout_query: "raw.types.UpdateBotPrecheckoutQuery",
        users: Dict[int, "raw.types.User"] = None
    ) -> "PreCheckoutQuery":
        # Try to decode pre-checkout query payload into string. If that fails, fallback to bytes instead of decoding by
        # ignoring/replacing errors, this way, button clicks will still work.
        try:
            payload = pre_checkout_query.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = pre_checkout_query.payload

        return PreCheckoutQuery(
            id=str(pre_checkout_query.query_id),
            from_user=types.User._parse(client, users[pre_checkout_query.user_id]),
            currency=pre_checkout_query.currency,
            total_amount=pre_checkout_query.total_amount,
            payload=payload,
            shipping_option_id=pre_checkout_query.shipping_option_id,
            payment_info=types.PaymentInfo(
                name=pre_checkout_query.info.name,
                phone_number=pre_checkout_query.info.phone,
                email=pre_checkout_query.info.email,
                shipping_address=types.ShippingAddress._parse(pre_checkout_query.info.shipping_address)
            ) if pre_checkout_query.info else None,
            client=client
        )

    async def answer(self, success: bool = None, error: str = None):
        """Bound method *answer* of :obj:`~pyrogram.types.PreCheckoutQuery`.

        Use this method as a shortcut for:

        .. code-block:: python

            await client.answer_pre_checkout_query(
                pre_checkout_query.id,
                success=True
            )

        Example:
            .. code-block:: python

                await pre_checkout_query.answer(success=True)

        Parameters:
            success (``bool`` *optional*):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.

            error (``bool`` *optional*):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.
        """
        return await self._client.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            success=success,
            error=error
        )
