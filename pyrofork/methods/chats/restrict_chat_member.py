#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from datetime import datetime
from typing import Union

import pyrofork
from pyrofork import raw, utils
from pyrofork import types


class RestrictChatMember:
    async def restrict_chat_member(
        self: "pyrofork.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: datetime = utils.zero_datetime()
    ) -> "types.Chat":
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile link in form of *t.me/<username>* (str).

            permissions (:obj:`~pyrofork.types.ChatPermissions`):
                New user permissions.

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~pyrofork.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from datetime import datetime, timedelta
                from pyrofork.types import ChatPermissions

                # Completely restrict chat member (mute) forever
                await app.restrict_chat_member(chat_id, user_id, ChatPermissions())

                # Chat member muted for 24h
                await app.restrict_chat_member(chat_id, user_id, ChatPermissions(),
                    datetime.now() + timedelta(days=1))

                # Chat member can only send text messages
                await app.restrict_chat_member(chat_id, user_id,
                    ChatPermissions(can_send_messages=True))
        """

        if permissions.all_perms is not None:
            send_audios=None
            send_docs=None
            send_games=None
            send_gifs=None
            send_photos=None
            send_plain=None
            send_roundvideos=None
            send_stickers=None
            send_videos=None
            send_voices=None
            if permissions.all_perms:
                send_messages=False
                send_media=False
                send_polls=False
                embed_links=False
                change_info=False
                invite_users=False
                pin_messages=False
                manage_topics=False
                send_inline=False
            else:
                send_messages=True
                send_media=True
                send_polls=True
                embed_links=True
                change_info=True
                invite_users=True
                pin_messages=True
                manage_topics=True
                send_inline=True
        else:
            old_permissions = (await self.get_chat(chat_id)).permissions
            send_messages = None
            send_media = None
            embed_links=not permissions.can_add_web_page_previews if permissions.can_add_web_page_previews is not None else not old_permissions.can_add_web_page_previews
            send_polls=not permissions.can_send_polls if permissions.can_send_polls is not None else not old_permissions.can_send_polls
            change_info=not permissions.can_change_info if permissions.can_change_info is not None else not old_permissions.can_change_info
            invite_users=not permissions.can_invite_users if permissions.can_invite_users is not None else not old_permissions.can_invite_users
            pin_messages=not permissions.can_pin_messages if permissions.can_pin_messages is not None else not old_permissions.can_pin_messages
            manage_topics=not permissions.can_manage_topics if permissions.can_manage_topics is not None else not old_permissions.can_manage_topics
            send_audios=not permissions.can_send_audios if permissions.can_send_audios is not None else not old_permissions.can_send_audios
            send_docs=not permissions.can_send_docs if permissions.can_send_docs is not None else not old_permissions.can_send_docs
            send_games=not permissions.can_send_games if permissions.can_send_games is not None else not old_permissions.can_send_games
            send_gifs=not permissions.can_send_gifs if permissions.can_send_gifs is not None else not old_permissions.can_send_gifs
            send_inline=not permissions.can_send_inline if permissions.can_send_inline is not None else not old_permissions.can_send_inline
            send_photos=not permissions.can_send_photos if permissions.can_send_photos is not None else not old_permissions.can_send_photos
            send_plain=not permissions.can_send_plain if permissions.can_send_plain is not None else not old_permissions.can_send_plain
            send_roundvideos=not permissions.can_send_roundvideos if permissions.can_send_roundvideos is not None else not old_permissions.can_send_roundvideos
            send_stickers=not permissions.can_send_stickers if permissions.can_send_stickers is not None else not old_permissions.can_send_stickers
            send_videos=not permissions.can_send_videos if permissions.can_send_videos is not None else not old_permissions.can_send_videos
            send_voices=not permissions.can_send_voices if permissions.can_send_voices is not None else not old_permissions.can_send_voices
            if permissions.can_send_messages is not None:
                if permissions.can_send_messages:
                    send_plain = False
                else:
                    send_plain = True
                if permissions.can_send_media_messages is None:
                    permissions.can_send_media_messages = old_permissions.can_send_media_messages
            if permissions.can_send_media_messages is not None:
                if permissions.can_send_media_messages:
                    embed_links = False
                    send_audios = False
                    send_docs = False
                    send_games = False
                    send_gifs = False
                    send_inline = False
                    send_photos = False
                    send_polls = False
                    send_roundvideos = False
                    send_stickers = False
                    send_videos = False
                    send_voices = False
                else:
                    embed_links = True
                    send_audios = True
                    send_docs = True
                    send_games = True
                    send_gifs = True
                    send_inline = True
                    send_photos = True
                    send_polls = True
                    send_roundvideos = True
                    send_stickers = True
                    send_videos = True
                    send_voices = True
        r = await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=utils.datetime_to_timestamp(until_date),
                    send_messages=send_messages,
                    send_media=send_media,
                    embed_links=embed_links,
                    send_polls=send_polls,
                    change_info=change_info,
                    invite_users=invite_users,
                    pin_messages=pin_messages,
                    manage_topics=manage_topics,
                    send_audios=send_audios,
                    send_docs=send_docs,
                    send_games=send_games,
                    send_gifs=send_gifs,
                    send_inline=send_inline,
                    send_photos=send_photos,
                    send_plain=send_plain,
                    send_roundvideos=send_roundvideos,
                    send_stickers=send_stickers,
                    send_videos=send_videos,
                    send_voices=send_voices
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
