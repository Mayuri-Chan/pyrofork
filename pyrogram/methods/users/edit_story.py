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

import os
import re
from typing import List

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

class EditStory:
    def _split(self, message, entities, *args, **kwargs):
        return message, entities

    async def edit_story(
        self: "pyrogram.Client",
        story_id: int,
        chat_id: int = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        #allowed_chats: List[int] = None,
        #denied_chats: List[int] = None,
        animation: str = None,
        photo: str = None,
        video: str = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        media_areas: List["types.InputMediaArea"] = None
    ) -> "types.Story":
        """Edit story.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            story_id (``int``):
                Unique identifier (int) of the target story.
            
            chat_id (``int``, *optional*):
                Unique identifier (int) of the target channel.
                You can also use channel public link in form of *t.me/<username>* (str).

            animation (``str`` | ``BinaryIO``, *optional*):
                New story Animation.
                Pass a file_id as string to send a animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a animation from the Internet,
                pass a file path as string to upload a new animation that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            photo (``str`` | ``BinaryIO``, *optional*):
                New story photo.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet,
                pass a file path as string to upload a new photo that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                New story video.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new video that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            privacy (:obj:`~pyrogram.enums.StoriesPrivacyRules`, *optional*):
                Story privacy.

            allowed_users (List of ``int``, *optional*):
                List of user_id whos allowed to view the story.

            denied_users (List of ``int``, *optional*):
                List of user_id whos denied to view the story.

            caption (``str``, *optional*):
                Story caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            media_areas (List of :obj:`~pyrogram.types.InputMediaArea`):
                List of media area object to be included in story.

        Returns:
            :obj:`~pyrogram.types.Story` a single story is returned.

        Example:
            .. code-block:: python

                # Edit story photo
                photo_id = "abcd12345"
                await app.edit_story(story_id=1, photo=photo_id)

        Raises:
            ValueError: In case of invalid arguments.
        """

        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        media = None
        privacy_rules = None

        if privacy:
            privacy_rules = [types.StoriesPrivacyRules(type=privacy)]

        if animation:
            if isinstance(animation, str):
                if os.path.isfile(animation):
                    file = await self.save_file(animation)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(animation) or "video/mp4",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True,
                                duration=0,
                                w=0,
                                h=0
                            ),
                            raw.types.DocumentAttributeAnimated()
                        ]
                    )
                elif re.match("^https?://", animation):
                    media = raw.types.InputMediaDocumentExternal(
                        url=animation
                    )
                else:
                    media = utils.get_input_media_from_file_id(animation, FileType.ANIMATION)
            else:
                file = await self.save_file(animation)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(animation) or "video/mp4",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=True,
                            duration=0,
                            w=0,
                            h=0
                        ),
                        raw.types.DocumentAttributeAnimated()
                    ]
                )
        elif photo:
            if isinstance(photo, str):
                if os.path.isfile(photo):
                    file = await self.save_file(photo)
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file
                    )
                elif re.match("^https?://", photo):
                    media = raw.types.InputMediaPhotoExternal(
                        url=photo
                    )
                else:
                    media = utils.get_input_media_from_file_id(photo, FileType.PHOTO)
            else:
                file = await self.save_file(photo)
                media = raw.types.InputMediaUploadedPhoto(
                    file=file
                )
        elif video:
            if isinstance(video, str):
                if os.path.isfile(video):
                    file = await self.save_file(video)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video) or "video/mp4",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True,
                                duration=0,
                                w=0,
                                h=0
                            )
                        ]
                    )
                elif re.match("^https?://", video):
                    media = raw.types.InputMediaDocumentExternal(
                        url=video
                    )
                else:
                    media = utils.get_input_media_from_file_id(video, FileType.VIDEO)
            else:
                file = await self.save_file(video)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(video) or "video/mp4",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=True,
                            duration=0,
                            w=0,
                            h=0
                        )
                    ]
                )
        text = None
        entities = None
        if caption:
            text, entities = self._split(**await utils.parse_text_entities(self, caption, parse_mode, caption_entities))

        '''
        if allowed_chats and len(allowed_chats) > 0:
            chats = [int(str(chat_id)[3:]) if str(chat_id).startswith("-100") else chat_id for chat_id in allowed_chats]
            privacy_rules.append(raw.types.InputPrivacyValueAllowChatParticipants(chats=chats))
        if denied_chats and len(denied_chats) > 0:
            chats = [int(str(chat_id)[3:]) if str(chat_id).startswith("-100") else chat_id for chat_id in denied_chats]
            privacy_rules.append(raw.types.InputPrivacyValueDisallowChatParticipants(chats=chats))
        '''
        if allowed_users and len(allowed_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in allowed_users]
            privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=users))
        if denied_users and len(denied_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in denied_users]
            privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))

        r = await self.invoke(
            raw.functions.stories.EditStory(
                id=story_id,
                peer=peer,
                media=media,
                privacy_rules=privacy_rules,
                caption=text,
                entities=entities,
                media_areas=[
                    await media_area.write(self)
                    for media_area in media_areas
                ]
            )
        )
        return await types.Story._parse(self, r.updates[0].story, r.updates[0].peer)
