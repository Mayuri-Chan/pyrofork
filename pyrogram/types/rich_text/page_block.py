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
from datetime import datetime

import pyrogram
from pyrogram import enums, raw, types
from ..object import Object


class PageBlock(Object):
    """A Telegram Instant View Page Block.

    Parameters:
        page_block_type (:obj:`~pyrogram.enums.PageBlockType`):
            The type of the page block.

        name (``str``, *optional*):
            Name of the anchor.

        text (:obj:`~pyrogram.types.RichText`, *optional*):
            Text content of the block.

        title (:obj:`~pyrogram.types.RichText`, *optional*):
            Title of the block.

        content (:obj:`~pyrogram.types.RichText`, *optional*):
            Content of the block.

        audio_id (``int``, *optional*):
            Audio file identifier.

        photo_id (``int``, *optional*):
            Photo file identifier.

        video_id (``int``, *optional*):
            Video file identifier.

        caption (:obj:`~pyrogram.types.PageCaption`, *optional*):
            Block caption.

        author (``str`` | :obj:`~pyrogram.types.RichText`, *optional*):
            Author name or rich text representation.

        published_date (:py:obj:`~datetime.datetime`, *optional*):
            Published date.

        blocks (List of :obj:`~pyrogram.types.PageBlock`, *optional*):
            Nested blocks.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat details.

        items (List of :obj:`~pyrogram.types.PageBlock` | List of :obj:`~pyrogram.types.OrderedItems` | List of :obj:`~pyrogram.types.PageBlockList`, *optional*):
            List items.

        cover (:obj:`~pyrogram.types.PageBlock`, *optional*):
            Cover block.

        url (``str``, *optional*):
            URL.

        html (``str``, *optional*):
            HTML code.

        poster_photo_id (``int``, *optional*):
            Poster photo file identifier.

        width (``int``, *optional*):
            Block width.

        height (``int``, *optional*):
            Block height.

        webpage_id (``int``, *optional*):
            Webpage identifier.

        author_photo_id (``int``, *optional*):
            Author photo identifier.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date.

        zoom (``int``, *optional*):
            Map zoom level.

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Location coordinates.

        source (``str``, *optional*):
            Source text.

        start (``int``, *optional*):
            Start index.

        order_type (``str``, *optional*):
            List order type.

        language (``str``, *optional*):
            Language code.

        articles (List of :obj:`~pyrogram.types.RelatedArticle`, *optional*):
            Related articles.

        rows (List of :obj:`~pyrogram.types.TableRow`, *optional*):
            Table rows.

        is_open (``bool``, *optional*):
            Whether the block is open by default.

        is_full_width (``bool``, *optional*):
            Whether the block is displayed in full width.

        is_allow_scrolling (``bool``, *optional*):
            Whether scrolling is allowed.

        is_reversed (``bool``, *optional*):
            Whether list items are in reversed order.

        is_spoiler (``bool``, *optional*):
            Whether content is hidden under spoiler.

        is_bordered (``bool``, *optional*):
            Whether table has borders.

        is_stripped (``bool``, *optional*):
            Whether table rows have stripped background.

        is_autoplay (``bool``, *optional*):
            Whether media autoplay is enabled.

        is_loop (``bool``, *optional*):
            Whether media loop is enabled.
    """

    def __init__(
        self,
        client: "pyrogram.Client",
        page_block_type: "enums.PageBlockType",
        name: Optional[str] = None,
        text: Optional["types.RichText"] = None,
        title: Optional["types.RichText"] = None,
        content: Optional["types.RichText"] = None,
        audio_id: Optional[int] = None,
        photo_id: Optional[int] = None,
        video_id: Optional[int] = None,
        caption: Optional["types.PageCaption"] = None,
        author: Optional[Union["types.RichText", str]] = None,
        published_date: Optional[datetime] = None,
        blocks: Optional[List["types.PageBlock"]] = None,
        chat: Optional["types.Chat"] = None,
        items: Optional[
            Union[
                List["types.PageBlock"],
                List["types.OrderedItems"],
                List["types.PageBlockList"]
            ]
        ] = None,
        cover: Optional["types.PageBlock"] = None,
        url: Optional[str] = None,
        html: Optional[str] = None,
        poster_photo_id: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        webpage_id: Optional[int] = None,
        author_photo_id: Optional[int] = None,
        date: Optional[datetime] = None,
        zoom: Optional[int] = None,
        location: Optional["types.Location"] = None,
        source: Optional[str] = None,
        start: Optional[int] = None,
        order_type: Optional[str] = None,
        language: Optional[str] = None,
        articles: Optional[List["types.RelatedArticle"]] = None,
        rows: Optional[List["types.TableRow"]] = None,
        is_open: Optional[bool] = None,
        is_full_width: Optional[bool] = None,
        is_allow_scrolling: Optional[bool] = None,
        is_reversed: Optional[bool] = None,
        is_spoiler: Optional[bool] = None,
        is_bordered: Optional[bool] = None,
        is_stripped: Optional[bool] = None,
        is_autoplay: Optional[bool] = None,
        is_loop: Optional[bool] = None
    ):
        super().__init__(client)

        self.page_block_type = page_block_type
        self.name = name
        self.text = text
        self.title = title
        self.content = content
        self.audio_id = audio_id
        self.photo_id = photo_id
        self.video_id = video_id
        self.caption = caption
        self.author = author
        self.published_date = published_date
        self.blocks = blocks
        self.chat = chat
        self.items = items
        self.cover = cover
        self.url = url
        self.html = html
        self.poster_photo_id = poster_photo_id
        self.width = width
        self.height = height
        self.webpage_id = webpage_id
        self.author_photo_id = author_photo_id
        self.date = date
        self.zoom = zoom
        self.location = location
        self.source = source
        self.start = start
        self.order_type = order_type
        self.language = language
        self.articles = articles
        self.rows = rows
        self.is_open = is_open
        self.is_full_width = is_full_width
        self.is_allow_scrolling = is_allow_scrolling
        self.is_reversed = is_reversed
        self.is_spoiler = is_spoiler
        self.is_bordered = is_bordered
        self.is_stripped = is_stripped
        self.is_autoplay = is_autoplay
        self.is_loop = is_loop

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        page_block: "raw.types.PageBlock"
    ) -> Optional["PageBlock"]:
        author = None
        items = None

        if getattr(page_block, "author", None):
            if isinstance(getattr(page_block, "author", None), str):
                author = getattr(page_block, "author", None)
            else:
                author = types.RichText._parse(client, getattr(page_block, "author", None))
        if getattr(page_block, "items", None):
            items = []
            for item in getattr(page_block, "items", None):
                if isinstance(item, raw.base.PageListOrderedItem):
                    items.append(types.OrderedItems._parse(client, item))
                elif isinstance(item, raw.types.PageListItemText) or isinstance(item, raw.types.PageListItemBlocks):
                    items.append(types.PageBlockList._parse(client, item))
                else:
                    items.append(PageBlock._parse(client, item))
        if isinstance(page_block, raw.types.PageBlockAnchor):
            page_block_type=enums.PageBlockType.ANCHOR
        elif isinstance(page_block, raw.types.PageBlockAudio):
            page_block_type=enums.PageBlockType.AUDIO
        elif isinstance(page_block, raw.types.PageBlockAuthorDate):
            page_block_type=enums.PageBlockType.AUTHOR_DATE
        elif isinstance(page_block, raw.types.PageBlockBlockquote):
            page_block_type=enums.PageBlockType.BLOCKQUOTE
        elif isinstance(page_block, raw.types.PageBlockBlockquoteBlocks):
            page_block_type=enums.PageBlockType.BLOCKQUOTE_BLOCKS
        elif isinstance(page_block, raw.types.PageBlockChannel):
            page_block_type=enums.PageBlockType.CHANNEL
        elif isinstance(page_block, raw.types.PageBlockCollage):
            page_block_type=enums.PageBlockType.COLLAGE
        elif isinstance(page_block, raw.types.PageBlockCover):
            page_block_type=enums.PageBlockType.COVER
        elif isinstance(page_block, raw.types.PageBlockDetails):
            page_block_type=enums.PageBlockType.DETAILS
        elif isinstance(page_block, raw.types.PageBlockDivider):
            page_block_type=enums.PageBlockType.DIVIDER
        elif isinstance(page_block, raw.types.PageBlockEmbed):
            page_block_type=enums.PageBlockType.EMBED
        elif isinstance(page_block, raw.types.PageBlockEmbedPost):
            page_block_type=enums.PageBlockType.EMBED_POST
        elif isinstance(page_block, raw.types.PageBlockFooter):
            page_block_type=enums.PageBlockType.FOOTER
        elif isinstance(page_block, raw.types.PageBlockHeader):
            page_block_type=enums.PageBlockType.HEADER
        elif isinstance(page_block, raw.types.PageBlockHeading1):
            page_block_type=enums.PageBlockType.HEADING1
        elif isinstance(page_block, raw.types.PageBlockHeading2):
            page_block_type=enums.PageBlockType.HEADING2
        elif isinstance(page_block, raw.types.PageBlockHeading3):
            page_block_type=enums.PageBlockType.HEADING3
        elif isinstance(page_block, raw.types.PageBlockHeading4):
            page_block_type=enums.PageBlockType.HEADING4
        elif isinstance(page_block, raw.types.PageBlockHeading5):
            page_block_type=enums.PageBlockType.HEADING5
        elif isinstance(page_block, raw.types.PageBlockHeading6):
            page_block_type=enums.PageBlockType.HEADING6
        elif isinstance(page_block, raw.types.PageBlockKicker):
            page_block_type=enums.PageBlockType.KICKER
        elif isinstance(page_block, raw.types.PageBlockList):
            page_block_type=enums.PageBlockType.LIST
        elif isinstance(page_block, raw.types.PageBlockMap):
            page_block_type=enums.PageBlockType.MAP
        elif isinstance(page_block, raw.types.PageBlockMath):
            page_block_type=enums.PageBlockType.MATH
        elif isinstance(page_block, raw.types.PageBlockOrderedList):
            page_block_type=enums.PageBlockType.ORDERED_LIST
        elif isinstance(page_block, raw.types.PageBlockParagraph):
            page_block_type=enums.PageBlockType.PARAGRAPH
        elif isinstance(page_block, raw.types.PageBlockPhoto):
            page_block_type=enums.PageBlockType.PHOTO
        elif isinstance(page_block, raw.types.PageBlockPreformatted):
            page_block_type=enums.PageBlockType.PREFORMATTED
        elif isinstance(page_block, raw.types.PageBlockPullquote):
            page_block_type=enums.PageBlockType.PULLQUOTE
        elif isinstance(page_block, raw.types.PageBlockRelatedArticles):
            page_block_type=enums.PageBlockType.RELATED_ARTICLES
        elif isinstance(page_block, raw.types.PageBlockSlideshow):
            page_block_type=enums.PageBlockType.SLIDESHOW
        elif isinstance(page_block, raw.types.PageBlockSubtitle):
            page_block_type=enums.PageBlockType.SUBTITLE
        elif isinstance(page_block, raw.types.PageBlockSubheader):
            page_block_type=enums.PageBlockType.SUBHEADER
        elif isinstance(page_block, raw.types.PageBlockTable):
            page_block_type=enums.PageBlockType.TABLE
        elif isinstance(page_block, raw.types.PageBlockTable):
            page_block_type=enums.PageBlockType.TABLE
        elif isinstance(page_block, raw.types.PageBlockThinking):
            page_block_type=enums.PageBlockType.THINKING
        elif isinstance(page_block, raw.types.PageBlockTitle):
            page_block_type=enums.PageBlockType.TITLE
        elif isinstance(page_block, raw.types.PageBlockUnsupported):
            page_block_type=enums.PageBlockType.UNSUPPORTED
        elif isinstance(page_block, raw.types.PageBlockVideo):
            page_block_type=enums.PageBlockType.VIDEO
        else:
            raise ValueError(f"Unknown page block type: {type(page_block)}")

        return PageBlock(
            client=client,
            page_block_type=page_block_type,
            text=types.RichText._parse(client, getattr(page_block, "text", None)) if getattr(page_block, "text", None) else None,
            title=types.RichText._parse(client, getattr(page_block, "title", None)) if getattr(page_block, "title", None) else None,
            content=types.RichText._parse(client, getattr(page_block, "content", None)) if getattr(page_block, "content", None) else None,
            caption=types.PageCaption._parse(client, getattr(page_block, "caption", None)) if getattr(page_block, "caption", None) else None,
            blocks=[PageBlock._parse(client, b) for b in getattr(page_block, "blocks", [])] if getattr(page_block, "blocks", None) else None,
            chat=types.Chat._parse(client, getattr(page_block, "channel", None)) if getattr(page_block, "channel", None) else None,
            cover=PageBlock._parse(client, getattr(page_block, "cover", None)) if getattr(page_block, "cover", None) else None,
            audio_id=getattr(page_block, "audio_id", None),
            photo_id=getattr(page_block, "photo_id", None),
            video_id=getattr(page_block, "video_id", None),
            author=author,
            author_photo_id=getattr(page_block, "author_photo_id", None),
            url=getattr(page_block, "url", None),
            webpage_id=getattr(page_block, "webpage_id", None),
            poster_photo_id=getattr(page_block, "poster_photo_id", None),
            width=getattr(page_block, "width", None),
            height=getattr(page_block, "height", None),
            date=getattr(page_block, "date", None),
            zoom=getattr(page_block, "zoom", None),
            location=types.Location._parse(client, getattr(page_block, "geo", None)) if getattr(page_block, "geo", None) else None,
            source=types.RichText._parse(client, getattr(page_block, "source", None)) if getattr(page_block, "source", None) else None,
            start=getattr(page_block, "start", None),
            order_type=getattr(page_block, "order", None),
            language=getattr(page_block, "language", None),
            items=items,
            articles=[types.RelatedArticle._parse(client, a) for a in getattr(page_block, "articles", [])] if getattr(page_block, "articles", None) else None,
            rows=[types.TableRow._parse(client, r) for r in getattr(page_block, "rows", [])] if getattr(page_block, "rows", None) else None,
            is_open=getattr(page_block, "is_open", None),
            is_full_width=getattr(page_block, "is_full_width", None),
            is_allow_scrolling=getattr(page_block, "is_allow_scrolling", None),
            is_reversed=getattr(page_block, "is_reversed", None),
            is_spoiler=getattr(page_block, "is_spoiler", None),
            is_bordered=getattr(page_block, "is_bordered", None),
            is_stripped=getattr(page_block, "is_stripped", None),
            is_autoplay=getattr(page_block, "is_autoplay", None),
            is_loop=getattr(page_block, "is_loop", None)
        )
