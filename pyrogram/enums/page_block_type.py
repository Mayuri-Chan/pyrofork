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

from enum import auto

from .auto_name import AutoName


class PageBlockType(AutoName):
    """Message page block type enumeration used in :obj:`~pyrogram.types.PageBlock`."""

    ANCHOR = auto()
    """Anchor link."""

    AUDIO = auto()
    """Audio block."""

    AUTHOR_DATE = auto()
    """Author name and date block."""

    BLOCKQUOTE = auto()
    """Blockquote text block."""

    BLOCKQUOTE_BLOCKS = auto()
    """Blockquote containing other blocks."""

    CHANNEL = auto()
    """Channel block."""

    COLLAGE = auto()
    """Image collage block."""

    COVER = auto()
    """Cover block."""

    DETAILS = auto()
    """Details disclosure block."""

    DIVIDER = auto()
    """Divider/separator block."""

    EMBED = auto()
    """Embedded content block."""

    EMBED_POST = auto()
    """Embedded social media post block."""

    FOOTER = auto()
    """Footer text block."""

    HEADER = auto()
    """Header text block."""

    HEADING1 = auto()
    """Heading level 1."""

    HEADING2 = auto()
    """Heading level 2."""

    HEADING3 = auto()
    """Heading level 3."""

    HEADING4 = auto()
    """Heading level 4."""

    HEADING5 = auto()
    """Heading level 5."""

    HEADING6 = auto()
    """Heading level 6."""

    KICKER = auto()
    """Kicker/prefix text block."""

    LIST = auto()
    """List block."""

    MAP = auto()
    """Map block."""

    MATH = auto()
    """Math/formula block."""

    ORDERED_LIST = auto()
    """Ordered list block."""

    PARAGRAPH = auto()
    """Paragraph text block."""

    PHOTO = auto()
    """Photo block."""

    PREFORMATTED = auto()
    """Preformatted code/text block."""

    PULLQUOTE = auto()
    """Pullquote text block."""

    RELATED_ARTICLES = auto()
    """Related articles block."""

    SLIDESHOW = auto()
    """Image slideshow block."""

    SUBHEADER = auto()
    """Subheader text block."""

    SUBTITLE = auto()
    """Subtitle text block."""

    TABLE = auto()
    """Table block."""

    THINKING = auto()
    """Thinking/loading block."""

    TITLE = auto()
    """Page title block."""

    UNSUPPORTED = auto()
    """Unsupported block."""

    VIDEO = auto()
    """Video block."""
