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

from datetime import datetime
from pyrogram import enums, raw, types, utils
from typing import List
from ..object import Object
from ..update import Update

class Story(Object, Update):
    """A story.

    Parameters:
        id (``int``):
            Unique story identifier.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story was sent.

        expire_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story will be expired.

        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The media type of the Story.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(message, message.media.value)`` to access the media message.

        has_protected_content (``bool``, *optional*):
            True, if the story can't be forwarded.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Story is an animation, information about the animation.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Story is a photo, information about the photo.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Story is a video, information about the video.
        
        edited (``bool``, *optional*):
           True, if the Story has been edited.

        pinned (``bool``, *optional*):
           True, if the Story is pinned.

        public (``bool``, *optional*):
           True, if the Story is shared with public.

        close_friends (``bool``, *optional*):
           True, if the Story is shared with close_friends only.

        contacts (``bool``, *optional*):
           True, if the Story is shared with contacts only.

        selected_contacts (``bool``, *optional*):
           True, if the Story is shared with selected contacts only.

        caption (``str``, *optional*):
            Caption for the Story, 0-1024 characters.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the caption.

        views (:obj:`~pyrogram.types.StoryViews`, *optional*):
            Stories views.
    """

    # TODO: Add Privacy

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User",
        date: datetime,
        expire_date: datetime,
        media: "enums.MessageMediaType",
        has_protected_content: bool = None,
        animation: "types.Animation" = None,
        photo: "types.Photo" = None,
        video: "types.Video" = None,
        edited: bool = None,
        pinned: bool = None,
        public: bool = None,
        close_friends: bool = None,
        contacts: bool = None,
        selected_contacts: bool = None,
        caption: str = None,
        caption_entities: List["types.MessageEntity"] = None,
        views: "types.StoryViews" = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.date = date
        self.expire_date = expire_date
        self.media = media
        self.has_protected_content = has_protected_content
        self.animation = animation
        self.photo = photo
        self.video = video
        self.edited = edited
        self.pinned = pinned
        self.public = public
        self.close_friends = close_friends
        self.contacts = contacts
        self.selected_contacts = selected_contacts
        self.caption = caption
        self.caption_entities = caption_entities
        self.views = views

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        user_id: int
    ) -> "Story":
        entities = [types.MessageEntity._parse(client, entity, {}) for entity in stories.entities]
        entities = types.List(filter(lambda x: x is not None, entities))
        animation = None
        photo = None
        video = None
        if stories.media:
            if isinstance(stories.media, raw.types.MessageMediaPhoto):
                photo = types.Photo._parse(client, stories.media.photo, stories.media.ttl_seconds)
                media_type = enums.MessageMediaType.PHOTO
            elif isinstance(stories.media, raw.types.MessageMediaDocument):
                doc = stories.media.document

                if isinstance(doc, raw.types.Document):
                    attributes = {type(i): i for i in doc.attributes}

                    if raw.types.DocumentAttributeAnimated in attributes:
                        video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                        animation = types.Animation._parse(client, doc, video_attributes, None)
                        media_type = enums.MessageMediaType.ANIMATION
                    elif raw.types.DocumentAttributeVideo in attributes:
                        video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                        video = types.Video._parse(client, doc, video_attributes, None, stories.media.ttl_seconds)
                        media_type = enums.MessageMediaType.VIDEO
                    else:
                        media_type = None
            else:
                media_type = None
        from_user = await client.get_users(user_id)

        return Story(
            id=stories.id,
            from_user=from_user,
            date=utils.timestamp_to_datetime(stories.date),
            expire_date=utils.timestamp_to_datetime(stories.expire_date),
            media=media_type,
            has_protected_content=stories.noforwards,
            animation=animation,
            photo=photo,
            video=video,
            edited=stories.edited,
            pinned=stories.pinned,
            public=stories.public,
            close_friends=stories.close_friends,
            contacts=stories.contacts,
            selected_contacts=stories.selected_contacts,
            caption=stories.caption,
            caption_entities=entities or None,
            views=types.StoryViews._parse(stories.views)
        )
