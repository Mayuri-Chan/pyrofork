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
from typing import BinaryIO, Callable, List, Optional, Union
from ..object import Object
from ..update import Update

class Story(Object, Update):
    """A story.

    Parameters:
        id (``int``):
            Unique story identifier.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

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

        forward_from (:obj:`~pyrogram.types.StoryForwardHeader`, *optional*):
            Story is a forwarded story.
            Information about the original story.

        privacy (:obj:`~pyrogram.enums.StoryPrivacy`, *optional*):
            Story privacy.

        allowed_users (List of ``int``, *optional*):
            List of user_id whos allowed to view the story.

        denied_users (List of ``int``, *optional*):
            List of user_id whos denied to view the story.

        media_areas (List of :obj:`~pyrogram.types.MediaArea`, *optional*):
            List of :obj:`~pyrogram.types.MediaArea` object in story.

        raw (``pyrogram.raw.types.StoryItem``, *optional*):
            The raw story object, as received from the Telegram API.
    """

    # TODO: fix Allowed Chats

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        chat: "types.Chat" = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
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
        views: "types.StoryViews" = None,
        privacy: "enums.StoryPrivacy" = None,
        forward_from: "types.StoryForwardHeader" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        media_areas: List["types.MediaArea"] = None,
        raw: "raw.types.StoryItem" = None
        #allowed_chats: List[int] = None,
        #denied_chats: List[int] = None
    ):
        super().__init__(client)

        self.id = id
        self.chat = chat
        self.from_user = from_user
        self.sender_chat = sender_chat
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
        self.privacy = privacy
        self.forward_from = forward_from
        self.allowed_users = allowed_users
        self.denied_users = denied_users
        self.media_areas = media_areas
        self.raw = raw
        #self.allowed_chats = allowed_chats
        #self.denied_chats = denied_chats

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union[
            "raw.types.PeerChannel",
            "raw.types.PeerUser",
            "raw.types.InputPeerChannel",
            "raw.types.InputPeerUser"
        ]
    ) -> "Story":
        if isinstance(stories, raw.types.StoryItemSkipped):
            return await types.StorySkipped._parse(client, stories, peer)
        if isinstance(stories, raw.types.StoryItemDeleted):
            return await types.StoryDeleted._parse(client, stories, peer)
        entities = [types.MessageEntity._parse(client, entity, {}) for entity in stories.entities]
        entities = types.List(filter(lambda x: x is not None, entities))
        animation = None
        photo = None
        video = None
        chat = None
        from_user = None
        sender_chat = None
        privacy = None
        forward_from = None
        #allowed_chats = None
        allowed_users = None
        #denied_chats = None
        denied_users = None
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
        if isinstance(peer, raw.types.PeerChannel) or isinstance(peer, raw.types.InputPeerChannel):
            chat_id = utils.get_channel_id(peer.channel_id)
            chat = await client.invoke(
                raw.functions.channels.GetChannels(
                    id=[await client.resolve_peer(chat_id)]
                )
            )
            sender_chat = types.Chat._parse_chat(client, chat.chats[0])
        elif isinstance(peer, raw.types.InputPeerSelf):
            from_user = client.me
        else:
            from_user = await client.get_users(peer.user_id)
        
        from_id = getattr(stories, "from_id", None)
        if from_id is not None:
            if getattr(from_id, "user_id", None) is not None:
                from_user = await client.get_users(getattr(from_id, "user_id"))
            elif getattr(from_id, "channel_id", None) is not None:
                chat = await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(utils.get_channel_id(getattr(from_id, "channel_id")))]
                    )
                )
                sender_chat = types.Chat._parse_chat(client, chat.chats[0])
            elif getattr(from_id, "chat_id", None) is not None:
                chat = await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(utils.get_channel_id(getattr(from_id, "chat_id")))]
                    )
                )
                sender_chat = types.Chat._parse_chat(client, chat.chats[0])

        for priv in stories.privacy:
            if isinstance(priv, raw.types.PrivacyValueAllowAll):
                privacy = enums.StoryPrivacy.PUBLIC
            elif isinstance(priv, raw.types.PrivacyValueAllowCloseFriends):
                privacy = enums.StoryPrivacy.CLOSE_FRIENDS
            elif isinstance(priv, raw.types.PrivacyValueAllowContacts):
                privacy = enums.StoryPrivacy.CONTACTS
            elif isinstance(priv, raw.types.PrivacyValueDisallowAll):
                privacy = enums.StoryPrivacy.PRIVATE
            elif isinstance(priv, raw.types.PrivacyValueDisallowContacts):
                privacy = enums.StoryPrivacy.NO_CONTACTS

            '''
            if allowed_chats and len(allowed_chats) > 0:
                chats = [int(str(chat_id)[3:]) if str(chat_id).startswith("-100") else chat_id for chat_id in allowed_chats]
                privacy_rules.append(raw.types.InputPrivacyValueAllowChatParticipants(chats=chats))
            if denied_chats and len(denied_chats) > 0:
                chats = [int(str(chat_id)[3:]) if str(chat_id).startswith("-100") else chat_id for chat_id in denied_chats]
                privacy_rules.append(raw.types.InputPrivacyValueDisallowChatParticipants(chats=chats))
            '''
            if isinstance(priv, raw.types.PrivacyValueAllowUsers):
                allowed_users = priv.users
            if isinstance(priv, raw.types.PrivacyValueDisallowUsers):
                denied_users = priv.users

        if stories.fwd_from is not None:
            forward_from = await types.StoryForwardHeader._parse(client, stories.fwd_from)

        media_areas = None
        if stories.media_areas is not None and len(stories.media_areas) > 0:
            media_areas = [
                await types.MediaArea._parse(client, media_area)
                for media_area in stories.media_areas
            ]

        return Story(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
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
            views=types.StoryViews._parse(stories.views),
            privacy=privacy,
            forward_from=forward_from,
            #allowed_chats=allowed_chats,
            #denied_chats=denied_chats,
            allowed_users=allowed_users,
            denied_users=denied_users,
            media_areas=media_areas,
            raw=stories,
            client=client
        )

    async def reply_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup=None
    ) -> "types.Message":
        """Bound method *reply_text* of :obj:`~pyrogram.types.Story`.

        An alias exists as *reply*.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text="hello",
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_text("hello", quote=True)

        Parameters:
            text (``str``):
                Text of the message to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original story.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_message(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_story_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_animation* :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_animation(
                chat_id=story.from_user.id,
                animation=animation,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_animation(animation)

        Parameters:
            animation (``str``):
                Animation to send.
                Pass a file_id as string to send an animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an animation from the Internet, or
                pass a file path as string to upload a new animation that exists on your local machine.

            caption (``str``, *optional*):
                Animation caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the animation needs to be covered with a spoiler animation.

            duration (``int``, *optional*):
                Duration of sent animation in seconds.

            width (``int``, *optional*):
                Animation width.

            height (``int``, *optional*):
                Animation height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the animation file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the animation sent.
                Defaults to file's path basename.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_animation(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_audio* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_audio(
                chat_id=story.from_user.id,
                audio=audio,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_audio(audio)

        Parameters:
            audio (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio file from the Internet, or
                pass a file path as string to upload a new audio file that exists on your local machine.

            caption (``str``, *optional*):
                Audio caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the audio in seconds.

            performer (``str``, *optional*):
                Performer.

            title (``str``, *optional*):
                Track name.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the music file album cover.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the audio sent.
                Defaults to file's path basename.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_audio(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        """Bound method *reply_cached_media* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_cached_media(
                chat_id=story.from_user.id,
                file_id=file_id,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_cached_media(file_id)

        Parameters:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            caption (``bool``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_cached_media(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup
        )

    async def reply_media_group(
        self,
        media: List[Union[
            "types.InputMediaPhoto",
            "types.InputMediaVideo",
            "types.InputMediaAudio",
            "types.InputMediaDocument"
        ]],
        disable_notification: bool = None,
        reply_to_story_id: int = None
    ) -> List["types.Message"]:
        """Bound method *reply_media_group* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_media_group(
                chat_id=story.from_user.id,
                media=list_of_media,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_media_group(list_of_media)

        Parameters:
            media (``list``):
                A list containing either :obj:`~pyrogram.types.InputMediaPhoto` or
                :obj:`~pyrogram.types.InputMediaVideo` objects
                describing photos and videos to be sent, must include 2–10 items.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            On success, a :obj:`~pyrogram.types.Messages` object is returned containing all the
            single messages sent.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_media_group(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            media=media,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id
        )

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        view_once: bool = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_photo* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_photo(
                chat_id=story.from_user.id,
                photo=photo,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_photo(photo)

        Parameters:
            photo (``str``):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet, or
                pass a file path as string to upload a new photo that exists on your local machine.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            view_once (``bool``, *optional*):
                Self-Destruct Timer.
                If True, the photo will self-destruct after it was viewed.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_photo(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            view_once=view_once,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_sticker* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_sticker(
                chat_id=story.from_user.id,
                sticker=sticker,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_sticker(sticker)

        Parameters:
            sticker (``str``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet, or
                pass a file path as string to upload a new sticker that exists on your local machine.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_sticker(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            sticker=sticker,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_video* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video(
                chat_id=story.from_user.id,
                video=video,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_video(video)

        Parameters:
            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the video needs to be covered with a spoiler animation.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the video will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the video sent.
                Defaults to file's path basename.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_video(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_video_note* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video_note(
                chat_id=story.from_user.id,
                video_note=video_note,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.reply_video_note(video_note)

        Parameters:
            video_note (``str``):
                Video note to send.
                Pass a file_id as string to send a video note that exists on the Telegram servers, or
                pass a file path as string to upload a new video note that exists on your local machine.
                Sending video notes by a URL is currently unsupported.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            length (``int``, *optional*):
                Video width and height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_video_note(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        """Bound method *reply_voice* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_voice(
                chat_id=story.from_user.id,
                voice=voice,
                reply_to_story_id=story.id
            )

        Example:
            .. code-block:: python

                await message.reply_voice(voice)

        Parameters:
            voice (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio from the Internet, or
                pass a file path as string to upload a new audio that exists on your local machine.

            caption (``str``, *optional*):
                Voice message caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the voice message in seconds.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_voice(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def delete(self):
        """Bound method *delete* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.delete_stories(
                story_ids=story.id
            )

        Example:
            .. code-block:: python

                await story.delete()

        Returns:
            True on success, False otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.delete_stories(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_ids=self.id
        )

    async def edit_animation(
        self,
        animation: Union[str, BinaryIO]
    ) -> "types.Story":
        """Bound method *edit_animation* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_animation(
                story_id=story.id,
                animation="/path/to/animation.mp4"
            )

        Example:
            .. code-block:: python

                await story.edit_animation("/path/to/animation.mp4")

        Parameters:
            animation (``str`` | ``BinaryIO``):
                New animation of the story.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            animation=animation
        )

    async def edit(
        self,
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
        """Bound method *edit* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_story(
                story_id=story.id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                await story.edit_caption("hello")

        Parameters:
            story_id (``int``):
                Unique identifier (int) of the target story.

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
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            privacy=privacy,
            #allowed_chats=allowed_chats,
            #denied_chats=denied_chats,
            allowed_users=allowed_users,
            denied_users=denied_users,
            animation=animation,
            photo=photo,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            media_areas=media_areas
        )

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None
    ) -> "types.Story":
        """Bound method *edit_caption* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await c.edit_story(
                channel=chat_id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                await story.edit_caption("hello")

        Parameters:
            caption (``str``):
                New caption of the story.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities
        )

    async def edit_photo(
        self,
        photo: Union[str, BinaryIO]
    ) -> "types.Story":
        """Bound method *edit_photo* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_story(
                story_id=story.id,
                photo="/path/to/photo.png"
            )

        Example:
            .. code-block:: python

                await story.edit_photo("/path/to/photo.png")

        Parameters:
            photo (``str`` | ``BinaryIO``):
                New photo of the story.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            photo=photo
        )

    async def edit_privacy(
        self,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        #allowed_chats: List[int] = None,
        #denied_chats: List[int] = None
    ) -> "types.Story":
        """Bound method *edit_privacy* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_story(
                story_id=story.id,
                privacy=enums.StoriesPrivacyRules.PUBLIC
            )

        Example:
            .. code-block:: python

                await story.edit_privacy(enums.StoriesPrivacyRules.PUBLIC)

        Parameters:
            privacy (:obj:`~pyrogram.enums.StoriesPrivacyRules`, *optional*):
                Story privacy.

            allowed_users (List of ``int``, *optional*):
                List of user_id whos allowed to view the story.

            denied_users (List of ``int``, *optional*):
                List of user_id whos denied to view the story.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            privacy=privacy,
            #allowed_chats=allowed_chats,
            #denied_chats=denied_chats,
            allowed_users=allowed_users,
            denied_users=denied_users
        )

    async def edit_video(
        self,
        video: Union[str, BinaryIO]
    ) -> "types.Story":
        """Bound method *edit_video* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_story(
                story_id=story.id,
                video="/path/to/video.mp4"
            )

        Example:
            .. code-block:: python

                await story.edit_video("/path/to/video.mp4")

        Parameters:
            video (``str`` | ``BinaryIO``):
                New video of the story.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Story` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            video=video
        )

    async def export_link(self) -> "types.ExportedStoryLink":
        """Bound method *export_link* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.export_story_link(
                user_id=story.from_user.id,
                story_id=story.id
            )

        Example:
            .. code-block:: python

                await story.export_link()

        Returns:
            :obj:`~pyrogram.types.ExportedStoryLink`: a single story link is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.export_story_link(chat_id=self.from_user.id if self.from_user else self.sender_chat.id, story_id=self.id)

    async def forward(
        self,
        chat_id: int = None,
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
    ):
        """Bound method *forward* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.forward_story(
                from_chat_id='wulan17',
                from_story_id=1,
                caption='Hello guys.'
            )

        Parameters:
            chat_id (``int``, *optional*):
                Unique identifier (int) of the target channel.
                If you want to forward story to a channel.

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

        Raises:
            ValueError: In case of invalid arguments.
        """
        return await self._client.send_story(
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
            forward_from_chat_id=self.from_user.id if self.from_user is not None else self.sender_chat.id,
            forward_from_story_id=self.id
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> str:
        """Bound method *download* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.download_media(story)

        Example:
            .. code-block:: python

                await story.download()

        Parameters:
            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            in_memory (``bool``, *optional*):
                Pass True to download the media in-memory.
                A binary file-like object with its attribute ".name" set will be returned.
                Defaults to False.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the absolute path of the downloaded file as string is returned, None otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ``ValueError``: If the message doesn't contain any downloadable media
        """
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )
