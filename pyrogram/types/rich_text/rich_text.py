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

import re
from typing import Optional, List, Union
from datetime import datetime

import pyrogram
from pyrogram import enums, raw, utils
from ..object import Object


class RichText(Object):
    """A rich text formatted block.

    Parameters:
        style (:obj:`~pyrogram.enums.RichTextStyle`):
            The format style applied to the text.

        text (:obj:`~pyrogram.types.RichText` | ``str``, *optional*):
            The inner text content.

        url (``str``, *optional*):
            The URL for linked text.

        webpage_id (``int``, *optional*):
            The webpage identifier for URLs.

        email (``str``, *optional*):
            Email address for email links.

        texts (List of :obj:`~pyrogram.types.RichText`, *optional*):
            A list of nested rich text elements (e.g. for concats).

        phone (``str``, *optional*):
            Phone number.

        document_id (``int``, *optional*):
            Document identifier.

        width (``int``, *optional*):
            Width of inline media/images.

        height (``int``, *optional*):
            Height of inline media/images.

        name (``str``, *optional*):
            Anchor name.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        style: "enums.RichTextStyle",
        text: Optional[Union["RichText", str]] = None,
        url: Optional[str] = None,
        webpage_id: Optional[int] = None,
        email: Optional[str] = None,
        texts: Optional[List["RichText"]] = None,
        phone: Optional[str] = None,
        document_id: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        name: Optional[str] = None,
        date: Optional[datetime] = None,
        is_relative: Optional[bool] = None,
        is_short_time: Optional[bool] = None,
        is_long_time: Optional[bool] = None,
        is_short_date: Optional[bool] = None,
        is_long_date: Optional[bool] = None,
        is_day_of_week: Optional[bool] = None,
        alt: Optional[str] = None,
        source: Optional[str] = None,
    ):
        super().__init__(client)
        self.style = style
        self.text = text
        self.url = url
        self.webpage_id = webpage_id
        self.email = email
        self.texts = texts
        self.phone = phone
        self.document_id = document_id
        self.width = width
        self.height = height
        self.name = name
        self.date = date
        self.is_relative = is_relative
        self.is_short_time = is_short_time
        self.is_long_time = is_long_time
        self.is_short_date = is_short_date
        self.is_long_date = is_long_date
        self.is_day_of_week = is_day_of_week
        self.alt = alt
        self.source = source

    @staticmethod
    def _parse(client: "pyrogram.Client", rich_text: "raw.base.RichText") -> Optional["RichText"]:
        if not rich_text:
            return None

        if isinstance(rich_text, str):
            return RichText(style=enums.RichTextStyle.PLAIN, text=rich_text, client=client)

        if isinstance(rich_text, raw.types.TextEmpty):
            return RichText(
                client=client,
                style=enums.RichTextStyle.EMPTY
            )

        class_name = type(rich_text).__name__
        stripped_name = class_name.replace("Text", "")
        snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', stripped_name).upper()
        try:
            style = getattr(enums.RichTextStyle, snake_case_name)
        except AttributeError:
            client.log.warning("Unknown RichText type: %s", type(rich_text))
            return RichText(
                client=client,
                style=enums.RichTextStyle.UNSUPPORTED
            )

        text = getattr(rich_text, "text", None)
        if text is not None:
            if isinstance(text, str):
                parsed_text = text
            else:
                parsed_text = RichText._parse(client, text)
        else:
            parsed_text = None

        return RichText(
            client=client,
            style=style,
            text=parsed_text,
            url=getattr(rich_text, "url", None),
            webpage_id=getattr(rich_text, "webpage_id", None),
            email=getattr(rich_text, "email", None),
            texts=[RichText._parse(client, t) for t in getattr(rich_text, "texts", [])] if getattr(rich_text, "texts", None) else None,
            phone=getattr(rich_text, "phone", None),
            document_id=getattr(rich_text, "document_id", None),
            width=getattr(rich_text, "w", None),
            height=getattr(rich_text, "h", None),
            name=getattr(rich_text, "name", None),
            date=utils.timestamp_to_datetime(getattr(rich_text, "date", None)) if getattr(rich_text, "date", None) else None,
            is_relative=getattr(rich_text, "relative", None),
            is_short_time=getattr(rich_text, "short_time", None),
            is_long_time=getattr(rich_text, "long_time", None),
            is_short_date=getattr(rich_text, "short_date", None),
            is_long_date=getattr(rich_text, "long_date", None),
            is_day_of_week=getattr(rich_text, "day_of_week", None),
            alt=getattr(rich_text, "alt", None),
            source=getattr(rich_text, "source", None)
        )
