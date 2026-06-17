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

from typing import Optional, List, Union

import pyrogram
from pyrogram import enums, raw
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

    @staticmethod
    def _parse(client: "pyrogram.Client", rich_text: "raw.base.RichText") -> Optional["RichText"]:
        if not rich_text:
            return None

        if isinstance(rich_text, raw.types.TextPlain):
            return RichText(style=enums.RichTextStyle.PLAIN, text=rich_text.text, client=client)
        elif isinstance(rich_text, raw.types.TextBold):
            return RichText(style=enums.RichTextStyle.BOLD, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextItalic):
            return RichText(style=enums.RichTextStyle.ITALIC, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextUnderline):
            return RichText(style=enums.RichTextStyle.UNDERLINE, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextStrike):
            return RichText(style=enums.RichTextStyle.STRIKE, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextFixed):
            return RichText(style=enums.RichTextStyle.FIXED, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextUrl):
            return RichText(style=enums.RichTextStyle.URL, text=RichText._parse(client, rich_text.text), url=rich_text.url, webpage_id=rich_text.webpage_id, client=client)
        elif isinstance(rich_text, raw.types.TextEmail):
            return RichText(style=enums.RichTextStyle.EMAIL, text=RichText._parse(client, rich_text.text), email=rich_text.email, client=client)
        elif isinstance(rich_text, raw.types.TextConcat):
            return RichText(style=enums.RichTextStyle.CONCAT, texts=[RichText._parse(client, t) for t in rich_text.texts], client=client)
        elif isinstance(rich_text, raw.types.TextSubscript):
            return RichText(style=enums.RichTextStyle.SUBSCRIPT, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextSuperscript):
            return RichText(style=enums.RichTextStyle.SUPERSCRIPT, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextMarked):
            return RichText(style=enums.RichTextStyle.MARKED, text=RichText._parse(client, rich_text.text), client=client)
        elif isinstance(rich_text, raw.types.TextPhone):
            return RichText(style=enums.RichTextStyle.PHONE, text=RichText._parse(client, rich_text.text), phone=rich_text.phone, client=client)
        elif isinstance(rich_text, raw.types.TextImage):
            return RichText(style=enums.RichTextStyle.IMAGE, document_id=rich_text.document_id, width=rich_text.w, height=rich_text.h, client=client)
        elif isinstance(rich_text, raw.types.TextAnchor):
            return RichText(style=enums.RichTextStyle.ANCHOR, text=RichText._parse(client, rich_text.text), name=rich_text.name, client=client)
        elif isinstance(rich_text, raw.types.TextSpoiler):
            return RichText(style=enums.RichTextStyle.SPOILER, text=RichText._parse(client, rich_text.text), client=client)
        return None
