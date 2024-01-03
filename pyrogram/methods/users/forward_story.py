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

from typing import List, Union

import pyrogram
from pyrogram import enums, types

class ForwardStory:
    def _split(self, message, entities, *args, **kwargs):
        return message, entities

    async def forward_story(
        self: "pyrogram.Client",
        from_chat_id: Union[int, str],
        from_story_id: int,
        chat_id: Union[int, str] = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        #allowed_chats: List[int] = None,
        #denied_chats: List[int] = None,
        pinned: bool = None,
        protect_content: bool = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        period: int = None
    ) -> "types.Story":
        """Forward a story.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat/user.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            from_story_id (``int``):
                Unique identifier of original story.

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target channel.
                If you want to forward story to a channel.
                You can also use channel public link in form of *t.me/<username>* (str).

            privacy (:obj:`~pyrogram.enums.StoriesPrivacyRules`, *optional*):
                Story privacy.
                Defaults to :obj:`~pyrogram.enums.StoriesPrivacyRules.PUBLIC`

            allowed_users (List of ``int``, *optional*):
                List of user_id whos allowed to view the story.

            denied_users (List of ``int``, *optional*):
                List of user_id whos denied to view the story.

            pinned (``bool``, *optional*):
                if True, the story will be pinned.
                default to False.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent story from forwarding and saving.
                default to False.

            caption (``str``, *optional*):
                Story caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            period (``int``, *optional*):
                How long the story will posted, in secs.
                only for premium users.

        Returns:
            :obj:`~pyrogram.types.Story` a single story is returned.

        Example:
            .. code-block:: python

                # forward a story
                await app.forward_story(from_chat_id='wulan17', from_story_id=1, caption='Hello guys.')

        Raises:
            ValueError: In case of invalid arguments.
        """
        
        return await self.send_story(
            chat_id=chat_id,
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users,
            pinned=pinned,
            protect_content=protect_content,
            caption=caption,
            caption_entities=caption_entities,
            parse_mode=parse_mode,
            period=period,
            forward_from_chat_id=from_chat_id,
            forward_from_story_id=from_story_id
        )
