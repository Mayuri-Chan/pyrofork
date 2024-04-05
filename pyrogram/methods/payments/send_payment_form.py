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

import re
from typing import Union, List

import pyrogram
from pyrogram import raw, types


class SendPaymentForm:
    async def send_payment_form(
        self: "pyrogram.Client", *,
        chat_id: Union[int, str] = None,
        message_id: int = None,
        invoice_link: str = None
    ) -> List[Union["types.Photo", "types.Video"]]:
        """Pay an invoice.

        .. note::

            For now only stars invoices are supported.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                of the target channel/supergroup (in the format @username).

            message_id (``int``):
                Pass a message identifier or to get the invoice from message.

            invoice_link (``str``):
                Pass a invoice link in form of a *t.me/$...* link or slug itself to pay this invoice.

        Returns:
            List of :obj:`~pyrogram.types.Photo` | :obj:`~pyrogram.types.Video`: On success, the list of bought photos and videos is returned.

        Example:
            .. code-block:: python

                # Pay invoice from message
                app.send_payment_form(chat_id=chat_id, message_id=123)

                # Pay invoice form from link
                app.send_payment_form(invoice_link="https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk")
        """
        if not any((all((chat_id, message_id)), invoice_link)):
            raise ValueError("You should pass at least one parameter to this method.")

        form = None
        invoice = None

        if message_id:
            invoice = raw.types.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        elif invoice_link:
            match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/\$)([\w-]+)$", invoice_link)

            if match:
                slug = match.group(1)
            else:
                slug = invoice_link

            invoice = raw.types.InputInvoiceSlug(
                slug=slug
            )

        form = await self.get_payment_form(chat_id=chat_id, message_id=message_id, invoice_link=invoice_link)

        # if form.invoice.currency == "XTR":
        r = await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.id,
                invoice=invoice
            )
        )
        # TODO: Add support for regular invoices (credentials)
        # else:
        #     r = await self.invoke(
        #         raw.functions.payments.SendPaymentForm(
        #             form_id=form.id,
        #             invoice=invoice,
        #             credentials=raw.types.InputPaymentCredentials(data=raw.types.DataJSON(data={}))
        #         )
        #     )

        medias = []

        if isinstance(r, raw.types.payments.PaymentResult):
            for i in r.updates.updates:
                if isinstance(i, raw.types.UpdateMessageExtendedMedia):
                    for ext_media in i.extended_media:
                        media = ext_media.media

                        if isinstance(media, raw.types.MessageMediaPhoto):
                            medias.append(types.Photo._parse(self, media.photo))
                        elif isinstance(media, raw.types.MessageMediaDocument):
                            doc = media.document

                            attributes = {type(i): i for i in doc.attributes}

                            file_name = getattr(
                                attributes.get(
                                    raw.types.DocumentAttributeFilename, None
                                ), "file_name", None
                            )

                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            medias.append(types.Video._parse(self, doc, video_attributes, file_name))

                    return types.List(medias)
        # elif isinstance(r, raw.types.payments.PaymentVerificationNeeded):
