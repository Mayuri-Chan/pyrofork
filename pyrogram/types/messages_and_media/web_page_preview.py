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

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class WebPagePreview(Object):
    """A web page preview.

    Parameters:
        webpage (:obj:`~pyrogram.types.WebPage`):
            Web Page Information.

        force_large_media (``bool``, *optional*):
            True, If the preview media size is forced to large.

        force_small_media  (``bool``, *optional*):
            True, If the preview media size is forced to small.
    """

    def __init__(
        self,
        *,
        webpage: "types.WebPage",
        force_large_media: bool = None,
        force_small_media: bool = None,
        invert_media: bool = None
    ):
        super().__init__()

        self.webpage = webpage
        self.force_large_media = force_large_media
        self.force_small_media = force_small_media
        self.invert_media = invert_media

    @staticmethod
    def _parse(web_page_preview: "raw.types.MessageMediaVenue", invert_media: bool = None):
        return WebPagePreview(
            webpage=types.WebPageEmpty._parse(web_page_preview.webpage),
            force_large_media=web_page_preview.force_large_media,
            force_small_media=web_page_preview.force_small_media,
            invert_media=invert_media
        )
