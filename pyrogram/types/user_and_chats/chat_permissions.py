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

from pyrogram import raw
from ..object import Object


class ChatPermissions(Object):
    """Describes actions that a non-administrator user is allowed to take in a chat.

    Parameters:
        all_perms (``bool``, *optional*):
            True, if all permissions are allowed.

        can_send_messages (``bool``, *optional*):
            True, if the user is allowed to send text messages, contacts, locations and venues.

        can_send_media_messages (``bool``, *optional*):
            True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes.
            Implies *can_send_messages*.

        can_send_polls (``bool``, *optional*):
            True, if the user is allowed to send polls.
            Implies can_send_messages

        can_add_web_page_previews (``bool``, *optional*):
            True, if the user is allowed to add web page previews to their messages.
            Implies *can_send_media_messages*.

        can_change_info (``bool``, *optional*):
            True, if the user is allowed to change the chat title, photo and other settings.
            Ignored in public supergroups

        can_invite_users (``bool``, *optional*):
            True, if the user is allowed to invite new users to the chat.

        can_pin_messages (``bool``, *optional*):
            True, if the user is allowed to pin messages.
            Ignored in public supergroups.

        can_manage_topics (``bool``, *optional*):
            True, if the user is allowed to create, rename, close, and reopen forum topics.
            supergroups only.

        can_send_audios (``bool``, *optional*):
            True, if the user is allowed to send audios.

        can_send_docs (``bool``, *optional*):
            True, if the user is allowed to send documents.

        can_send_games (``bool``, *optional*):
            True, if the user is allowed to send games.

        can_send_gifs (``bool``, *optional*):
            True, if the user is allowed to send gifs.

        can_send_inline (``bool``, *optional*):
            True, if the user is allowed to send bot inline.

        can_send_photos (``bool``, *optional*):
            True, if the user is allowed to send photos.

        can_send_plain (``bool``, *optional*):
            True, if the user is allowed to send plain texts.

        can_send_roundvideos (``bool``, *optional*):
            True, if the user is allowed to send rounded videos.

        can_send_stickers (``bool``, *optional*):
            True, if the user is allowed to send stickers.

        can_send_videos (``bool``, *optional*):
            True, if the user is allowed to send videos.

        can_send_voices (``bool``, *optional*):
            True, if the user is allowed to send voices.
    """

    def __init__(
        self,
        *,
        all_perms: bool = None,
        can_send_messages: bool = None,  # Text, contacts, locations and venues
        can_send_media_messages: bool = None,  # Audio files, documents, photos, videos, video notes and voice notes
        can_send_polls: bool = None,
        can_add_web_page_previews: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None,
        can_manage_topics: bool = None,
        can_send_audios: bool = None,
        can_send_docs: bool = None,
        can_send_games: bool = None,
        can_send_gifs: bool = None,
        can_send_inline: bool = None,
        can_send_photos: bool = None,
        can_send_plain: bool = None,
        can_send_roundvideos: bool = None,
        can_send_stickers: bool = None,
        can_send_videos: bool = None,
        can_send_voices: bool = None
    ):
        super().__init__(None)

        self.all_perms = all_perms
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.can_manage_topics = can_manage_topics
        self.can_send_audios = can_send_audios
        self.can_send_docs = can_send_docs
        self.can_send_games = can_send_games
        self.can_send_gifs = can_send_gifs
        self.can_send_inline = can_send_inline
        self.can_send_photos = can_send_photos
        self.can_send_plain = can_send_plain
        self.can_send_roundvideos = can_send_roundvideos
        self.can_send_stickers = can_send_stickers
        self.can_send_videos = can_send_videos
        self.can_send_voices = can_send_voices
        if (
            all_perms is None
            and can_send_messages is None
            and can_send_media_messages is None
            and can_send_polls is None
            and can_add_web_page_previews is None
            and can_change_info is None
            and can_invite_users is None
            and can_pin_messages is None
            and can_manage_topics is None
            and can_send_audios is None
            and can_send_docs is None
            and can_send_games is None
            and can_send_gifs is None
            and can_send_inline is None
            and can_send_photos is None
            and can_send_plain is None
            and can_send_roundvideos is None
            and can_send_stickers is None
            and can_send_videos is None
            and can_send_voices is None
        ):
            self.all_perms = False

    @staticmethod
    def _parse(denied_permissions: "raw.base.ChatBannedRights") -> "ChatPermissions":
        if isinstance(denied_permissions, raw.types.ChatBannedRights):
            all_permissions = None
            all_params = [
                denied_permissions.send_messages,
                denied_permissions.send_media,
                denied_permissions.embed_links,
                denied_permissions.send_polls,
                denied_permissions.change_info,
                denied_permissions.invite_users,
                denied_permissions.pin_messages,
                denied_permissions.send_audios,
                denied_permissions.send_docs,
                denied_permissions.send_games,
                denied_permissions.send_gifs,
                denied_permissions.send_inline,
                denied_permissions.send_photos,
                denied_permissions.send_plain,
                denied_permissions.send_roundvideos,
                denied_permissions.send_stickers,
                denied_permissions.send_videos,
                denied_permissions.send_voices
            ]
            all_params_not = [
                not denied_permissions.send_messages,
                not denied_permissions.send_media,
                not denied_permissions.embed_links,
                not denied_permissions.send_polls,
                not denied_permissions.change_info,
                not denied_permissions.invite_users,
                not denied_permissions.pin_messages,
                not denied_permissions.send_audios,
                not denied_permissions.send_docs,
                not denied_permissions.send_games,
                not denied_permissions.send_gifs,
                not denied_permissions.send_inline,
                not denied_permissions.send_photos,
                not denied_permissions.send_plain,
                not denied_permissions.send_roundvideos,
                not denied_permissions.send_stickers,
                not denied_permissions.send_videos,
                not denied_permissions.send_voices
            ]
            if all(all_params):
                all_permissions = False
            elif all(all_params_not):
                all_permissions = True
            return ChatPermissions(
                all_perms=all_permissions,
                can_send_messages=not denied_permissions.send_messages,
                can_send_media_messages=not denied_permissions.send_media,
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_send_polls=not denied_permissions.send_polls,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages,
                can_manage_topics=not denied_permissions.manage_topics,
                can_send_audios=not denied_permissions.send_audios,
                can_send_docs=not denied_permissions.send_docs,
                can_send_games=not denied_permissions.send_games,
                can_send_gifs=not denied_permissions.send_gifs,
                can_send_inline=not denied_permissions.send_inline,
                can_send_photos=not denied_permissions.send_photos,
                can_send_plain=not denied_permissions.send_plain,
                can_send_roundvideos=not denied_permissions.send_roundvideos,
                can_send_stickers=not denied_permissions.send_stickers,
                can_send_videos=not denied_permissions.send_videos,
                can_send_voices=not denied_permissions.send_voices
            )
