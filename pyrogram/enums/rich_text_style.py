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


class RichTextStyle(AutoName):
    """Rich text style enumeration used in :obj:`~pyrogram.types.RichText`."""

    PLAIN = auto()
    """Plain text style."""

    BOLD = auto()
    """Bold text style."""

    ITALIC = auto()
    """Italic text style."""

    UNDERLINE = auto()
    """Underlined text style."""

    STRIKE = auto()
    """Strikethrough text style."""

    FIXED = auto()
    """Fixed-width (monospace) text style."""

    URL = auto()
    """URL link text style."""

    EMAIL = auto()
    """Email address link text style."""

    CONCAT = auto()
    """Concatenated/styled text block."""

    SUBSCRIPT = auto()
    """Subscript text style."""

    SUPERSCRIPT = auto()
    """Superscript text style."""

    MARKED = auto()
    """Marked/highlighted text style."""

    PHONE = auto()
    """Phone number link text style."""

    IMAGE = auto()
    """Inline image text style."""

    ANCHOR = auto()
    """Anchor link text style."""

    SPOILER = auto()
    """Spoiler text style."""
