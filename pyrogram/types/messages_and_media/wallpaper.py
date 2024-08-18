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

from ..object import Object
from pyrogram import raw, types

class Wallpaper(Object):
    """A wallpaper.

    parameters:
        id (``int``):
            Unique identifier for this wallpaper.

        slug (``str``):
            The slug of the wallpaper.

        document (:obj:`~pyrogram.types.Document`):
            The document of the wallpaper.

        is_creator (:obj:`bool`, optional):
            True, if the wallpaper was created by the current user.

        is_default (:obj:`bool`, optional):
            True, if the wallpaper is the default wallpaper.

        is_pattern (:obj:`bool`, optional):
            True, if the wallpaper is a pattern.

        id_dark (:obj:`bool`, optional):
            True, if the wallpaper is dark.

        settings (:obj:`~pyrogram.types.WallpaperSettings`, optional):
            The settings of the wallpaper.
    """

    def __init__(
        self,
        id: int,
        slug: str,
        document: "types.Document",
        is_creator: bool = None,
        is_default: bool = None,
        is_pattern: bool = None,
        is_dark: bool = None,
        settings: "types.WallpaperSettings" = None
    ):
        super().__init__()
        self.id = id
        self.slug = slug
        self.document = document
        self.is_creator = is_creator
        self.is_default = is_default
        self.is_pattern = is_pattern
        self.is_dark = is_dark
        self.settings = settings

    @staticmethod
    def _parse(client: "pyrogram.Client", wallpaper: "raw.base.WallPaper") -> "Wallpaper":
        doc = wallpaper.document
        attributes = {type(i): i for i in doc.attributes}

        file_name = getattr(
            attributes.get(
                raw.types.DocumentAttributeFilename, None
            ), "file_name", None
        )
        return Wallpaper(
            id=wallpaper.id,
            slug=wallpaper.slug,
            document=types.Document._parse(client, doc, file_name),
            is_creator=getattr(wallpaper, "creator", None),
            is_default=getattr(wallpaper, "default", None),
            is_pattern=getattr(wallpaper, "pattern", None),
            is_dark=getattr(wallpaper, "dark", None),
            settings=types.WallpaperSettings._parse(wallpaper.settings)
        )
