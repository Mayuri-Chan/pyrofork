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

from typing import Optional
from datetime import datetime

import pyrogram
from pyrogram import raw
from ..object import Object


class RelatedArticle(Object):
    """A link to a related article.

    Parameters:
        url (``str``):
            The URL of the related article.

        webpage_id (``int``):
            Webpage identifier.

        title (``str``, *optional*):
            Title of the article.

        description (``str``, *optional*):
            Description.

        author (``str``, *optional*):
            Author of the article.

        published_date (:py:obj:`~datetime.datetime`, *optional*):
            Published date.

        photo_id (``int``, *optional*):
            Associated photo file identifier.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        url: str,
        webpage_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        published_date: Optional[datetime] = None,
        photo_id: Optional[int] = None,
    ):
        super().__init__(client)
        self.url = url
        self.webpage_id = webpage_id
        self.title = title
        self.description = description
        self.author = author
        self.published_date = published_date
        self.photo_id = photo_id

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        article: "raw.types.PageRelatedArticle"
    ) -> Optional["RelatedArticle"]:
        return RelatedArticle(
            client=client,
            url=getattr(article, "url", None),
            webpage_id=getattr(article, "webpage_id", None),
            title=getattr(article, "title", None),
            description=getattr(article, "description", None),
            author=getattr(article, "author", None),
            published_date=datetime.fromtimestamp(getattr(article, "published_date", None)) if getattr(article, "published_date", None) else None,
            photo_id=getattr(article, "photo_id", None),
        )
