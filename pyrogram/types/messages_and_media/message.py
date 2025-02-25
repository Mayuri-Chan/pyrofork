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

import logging
from datetime import datetime
from functools import partial
from typing import List, Match, Union, BinaryIO, Optional, Callable

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.errors import ChannelPrivate, MessageIdsEmpty, PeerIdInvalid
from pyrogram.parser import utils as parser_utils, Parser
from ..object import Object
from ..update import Update

log = logging.getLogger(__name__)


class Str(str):
    def __init__(self, *args):
        super().__init__()

        self.entities = None

    def init(self, entities):
        self.entities = entities

        return self

    @property
    def markdown(self):
        return Parser.unparse(self, self.entities, False)

    @property
    def html(self):
        return Parser.unparse(self, self.entities, True)

    def __getitem__(self, item):
        return parser_utils.remove_surrogates(parser_utils.add_surrogates(self)[item])


class Message(Object, Update):
    """A message.

    Parameters:
        id (``int``):
            Unique message identifier inside this chat.

        message_thread_id (``int``, *optional*):
            Unique identifier of a message thread to which the message belongs.
            for supergroups only

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender, empty for messages sent to channels.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the message, sent on behalf of a chat.
            The channel itself for channel messages.
            The supergroup itself for messages from anonymous group administrators.
            The linked channel for messages automatically forwarded to the discussion group.

        sender_business_bot (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the message, sent on behalf of a business bot.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was sent.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Conversation the message belongs to.

        topic (:obj:`~pyrogram.types.ForumTopic`, *optional*):
            Topic the message belongs to.
            only returned using when client.get_messages.

        forward_from (:obj:`~pyrogram.types.User`, *optional*):
            For forwarded messages, sender of the original message.

        forward_sender_name (``str``, *optional*):
            For messages forwarded from users who have hidden their accounts, name of the user.

        forward_from_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            For messages forwarded from channels, information about the original channel. For messages forwarded from anonymous group administrators, information about the original supergroup.

        forward_from_message_id (``int``, *optional*):
            For messages forwarded from channels, identifier of the original message in the channel.

        forward_signature (``str``, *optional*):
            For messages forwarded from channels, signature of the post author if present.

        forward_date (:py:obj:`~datetime.datetime`, *optional*):
            For forwarded messages, date the original message was sent.

        is_topic_message (``bool``, *optional*):
            True, if the message is sent to a forum topic

        reply_to_chat_id (``int``, *optional*):
            Unique identifier of the chat where the replied message belongs to.

        reply_to_message_id (``int``, *optional*):
            The id of the message which this message directly replied to.

        reply_to_story_id (``int``, *optional*):
            The id of the story which this message directly replied to.

        reply_to_story_user_id (``int``, *optional*):
            The id of the story sender which this message directly replied to.

        reply_to_story_chat_id (``int``, *optional*):
            The id of the chat where the story was sent which this message directly replied to.

        reply_to_top_message_id (``int``, *optional*):
            The id of the first message which started this message thread.

        reply_to_message (:obj:`~pyrogram.types.Message`, *optional*):
            For replies, the original message. Note that the Message object in this field will not contain
            further reply_to_message fields even if it itself is a reply.

        reply_to_story (:obj:`~pyrogram.types.Story`, *optional*):
            For replies, the original story.

        business_connection_id (``str``, *optional*):
            The business connection identifier.

        mentioned (``bool``, *optional*):
            The message contains a mention.

        empty (``bool``, *optional*):
            The message is empty.
            A message can be empty in case it was deleted or you tried to retrieve a message that doesn't exist yet.

        service (:obj:`~pyrogram.enums.MessageServiceType`, *optional*):
            The message is a service message.
            This field will contain the enumeration type of the service message.
            You can use ``service = getattr(message, message.service.value)`` to access the service message.

        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The message is a media message.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(message, message.media.value)`` to access the media message.

        edit_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was last edited.

        edit_hide (``bool``, *optional*):
            The message shown as not modified.
            A message can be not modified in case it has received a reaction.

        media_group_id (``str``, *optional*):
            The unique identifier of a media message group this message belongs to.

        author_signature (``str``, *optional*):
            Signature of the post author for messages in channels, or the custom title of an anonymous group
            administrator.

        has_protected_content (``bool``, *optional*):
            True, if the message can't be forwarded.

        has_media_spoiler (``bool``, *optional*):
            True, if the message media is covered by a spoiler animation.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear
            in the caption.

        quote_text (``str``, *optional*):
            Quoted reply text.

        quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For quote text, special entities like usernames, URLs, bot commands, etc. that appear in the quote text.

        effect_id (``str``, *optional*):
            Unique identifier of the message effect added to the message.

        invert_media (``bool``, *optional*):
            True, If the media position is inverted.
            only animation, photo, video, and webpage preview messages.

        audio (:obj:`~pyrogram.types.Audio`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`~pyrogram.types.Document`, *optional*):
            Message is a general file, information about the file.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Message is a photo, information about the photo.

        paid_media (:obj:`~pyrogram.types.PaidMedia`, *optional*):
            Message is a paid media, information about the paid media.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Message is a sticker, information about the sticker.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Message is an animation, information about the animation.

        game (:obj:`~pyrogram.types.Game`, *optional*):
            Message is a game, information about the game.

        giveaway (:obj:`~pyrogram.types.Giveaway`, *optional*):
            Message is a giveaway, information about the giveaway.

        giveaway_result (:obj:`~pyrogram.types.GiveawayResult`, *optional*):
            Message is a giveaway result, information about the giveaway result.

        invoice (:obj:`~pyrogram.types.Invoice`, *optional*):
            Message is an invoice for a payment, information about the invoice.

        story (:obj:`~pyrogram.types.MessageStory` | :obj:`~pyrogram.types.Story`, *optional*):
            Message is a forwarded story, information about the forwarded story.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Message is a video, information about the video.

        voice (:obj:`~pyrogram.types.Voice`, *optional*):
            Message is a voice message, information about the file.

        video_note (:obj:`~pyrogram.types.VideoNote`, *optional*):
            Message is a video note, information about the video message.

        web_page_preview (:obj:`~pyrogram.types.WebPagePreview`, *optional*):
            Message is a web page preview, information about the web page preview message.

        caption (``str``, *optional*):
            Caption for the audio, document, photo, video or voice, 0-1024 characters.
            If the message contains caption entities (bold, italic, ...) you can access *caption.markdown* or
            *caption.html* to get the marked up caption text. In case there is no caption entity, the fields
            will contain the same text as *caption*.

        contact (:obj:`~pyrogram.types.Contact`, *optional*):
            Message is a shared contact, information about the contact.

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Message is a shared location, information about the location.

        venue (:obj:`~pyrogram.types.Venue`, *optional*):
            Message is a venue, information about the venue.

        poll (:obj:`~pyrogram.types.Poll`, *optional*):
            Message is a native poll, information about the poll.

        dice (:obj:`~pyrogram.types.Dice`, *optional*):
            A dice containing a value that is randomly generated by Telegram.

        new_chat_members (List of :obj:`~pyrogram.types.User`, *optional*):
            New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members).

        chat_joined_by_request (:obj:`~pyrogram.types.ChatJoinedByRequest`, *optional*):
            New members chat join request has been approved in group or supergroup.

        left_chat_member (:obj:`~pyrogram.types.User`, *optional*):
            A member was removed from the group, information about them (this member may be the bot itself).

        new_chat_title (``str``, *optional*):
            A chat title was changed to this value.

        new_chat_photo (:obj:`~pyrogram.types.Photo`, *optional*):
            A chat photo was change to this value.

        delete_chat_photo (``bool``, *optional*):
            Service message: the chat photo was deleted.

        group_chat_created (``bool``, *optional*):
            Service message: the group has been created.

        supergroup_chat_created (``bool``, *optional*):
            Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            supergroup when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a directly created supergroup.

        channel_chat_created (``bool``, *optional*):
            Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            channel when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a channel.

        migrate_to_chat_id (``int``, *optional*):
            The group has been migrated to a supergroup with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        migrate_from_chat_id (``int``, *optional*):
            The supergroup has been migrated from a group with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Specified message was pinned.
            Note that the Message object in this field will not contain further reply_to_message fields even if it
            is itself a reply.

        game_high_score (:obj:`~pyrogram.types.GameHighScore`, *optional*):
            The game score for a user.
            The reply_to_message field will contain the game Message.

        views (``int``, *optional*):
            Channel post views.
        
        forwards (``int``, *optional*):
            Channel post forwards.

        via_bot (:obj:`~pyrogram.types.User`):
            The information of the bot that generated the message from an inline query of a user.

        outgoing (``bool``, *optional*):
            Whether the message is incoming or outgoing.
            Messages received from other chats are incoming (*outgoing* is False).
            Messages sent from yourself to other chats are outgoing (*outgoing* is True).
            An exception is made for your own personal chat; messages sent there will be incoming.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the text of this message. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.

        command (List of ``str``, *optional*):
            A list containing the command and its arguments, if any.
            E.g.: "/start 1 2 3" would produce ["start", "1", "2", "3"].
            Only applicable when using :obj:`~pyrogram.filters.command`.

        bot_allowed (:obj:`~pyrogram.types.BotAllowed`, *optional*):
            Contains information about a allowed bot.

        chats_shared (List of :obj:`~pyrogram.types.RequestedChats`, *optional*):
            Service message: chats shared

        forum_topic_created (:obj:`~pyrogram.types.ForumTopicCreated`, *optional*):
            Service message: forum topic created

        forum_topic_closed (:obj:`~pyrogram.types.ForumTopicClosed`, *optional*):
            Service message: forum topic closed

        forum_topic_reopened (:obj:`~pyrogram.types.ForumTopicReopened`, *optional*):
            Service message: forum topic reopened

        forum_topic_edited (:obj:`~pyrogram.types.ForumTopicEdited`, *optional*):
            Service message: forum topic edited

        general_topic_hidden (:obj:`~pyrogram.types.GeneralTopicHidden`, *optional*):
            Service message: forum general topic hidden

        general_topic_unhidden (:obj:`~pyrogram.types.GeneralTopicUnhidden`, *optional*):
            Service message: forum general topic unhidden

        gifted_premium (:obj:`~pyrogram.types.GiftedPremium`, *optional*):
            Info about a gifted Telegram Premium subscription

        giveaway_launcheded (:obj:`~pyrogram.types.GiveawayLaunched`, *optional*):
            Service message: giveaway launched.

        video_chat_scheduled (:obj:`~pyrogram.types.VideoChatScheduled`, *optional*):
            Service message: voice chat scheduled.

        video_chat_started (:obj:`~pyrogram.types.VideoChatStarted`, *optional*):
            Service message: the voice chat started.

        video_chat_ended (:obj:`~pyrogram.types.VideoChatEnded`, *optional*):
            Service message: the voice chat has ended.

        video_chat_members_invited (:obj:`~pyrogram.types.VoiceChatParticipantsInvited`, *optional*):
            Service message: new members were invited to the voice chat.

        web_app_data (:obj:`~pyrogram.types.WebAppData`, *optional*):
            Service message: web app data sent to the bot.

        successful_payment (:obj:`~pyrogram.types.SuccessfulPayment`, *optional*):
            Service message: successful payment.

        payment_refunded (:obj:`~pyrogram.types.PaymentRefunded`, *optional*):
            Service message: payment refunded.

        boosts_applied (``int``, *optional*):
            Service message: how many boosts were applied.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
            Additional interface options. An object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.

        reactions (List of :obj:`~pyrogram.types.Reaction`):
            List of the reactions to this message.

        raw (``pyrogram.raw.types.Message``, *optional*):
            The raw message object, as received from the Telegram API.

        gift_code (:obj:`~pyrogram.types.GiftCode`, *optional*):
            Service message: gift code information.
            Contains a `Telegram Premium giftcode link <https://core.telegram.org/api/links#premium-giftcode-links>`_.

        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            Service message: star gift information.

        gifted_premium (:obj:`~pyrogram.types.GiftedPremium`, *optional*):
            Info about a gifted Telegram Premium subscription

        link (``str``, *property*):
            Generate a link to this message, only for groups and channels.

        content (``str``, *property*):
            The text or caption content of the message.

        scheduled (``bool``, *optional*):
            Message is a scheduled message and still in schedule.

        from_scheduled (``bool``, *optional*):
            Message is a scheduled message and has been sent.

        chat_join_type (:obj:`~pyrogram.enums.ChatJoinType`, *optional*):
            The message is a service message of the type :obj:`~pyrogram.enums.MessageServiceType.NEW_CHAT_MEMBERS`.
            This field will contain the enumeration type of how the user had joined the chat.
    """

    # TODO: Add game missing field, Also connected_website

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        message_thread_id: int = None,
        business_connection_id: str = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        sender_business_bot: "types.User" = None,
        date: datetime = None,
        chat: "types.Chat" = None,
        topic: "types.ForumTopic" = None,
        forward_from: "types.User" = None,
        forward_sender_name: str = None,
        forward_from_chat: "types.Chat" = None,
        forward_from_message_id: int = None,
        forward_signature: str = None,
        forward_date: datetime = None,
        is_topic_message: bool = None,
        reply_to_chat_id: int = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_story_user_id: int = None,
        reply_to_story_chat_id: int = None,
        reply_to_top_message_id: int = None,
        reply_to_message: "Message" = None,
        reply_to_story: "types.Story" = None,
        mentioned: bool = None,
        empty: bool = None,
        service: "enums.MessageServiceType" = None,
        scheduled: bool = None,
        from_scheduled: bool = None,
        edit_hide: bool = None,
        media: "enums.MessageMediaType" = None,
        edit_date: datetime = None,
        media_group_id: str = None,
        author_signature: str = None,
        has_protected_content: bool = None,
        has_media_spoiler: bool = None,
        text: Str = None,
        entities: List["types.MessageEntity"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        effect_id: str = None,
        invert_media: bool = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        photo: "types.Photo" = None,
        paid_media: "types.PaidMedia" = None,
        sticker: "types.Sticker" = None,
        animation: "types.Animation" = None,
        game: "types.Game" = None,
        giveaway: "types.Giveaway" = None,
        giveaway_result: "types.GiveawayResult" = None,
        boosts_applied: int = None,
        chat_theme_updated: "types.ChatTheme" = None,
        chat_wallpaper_updated: "types.ChatWallpaper" = None,
        contact_registered: "types.ContactRegistered" = None,
        gift_code: "types.GiftCode" = None,
        gift: "types.Gift" = None,
        screenshot_taken: "types.ScreenshotTaken" = None,
        invoice: "types.Invoice" = None,
        story: Union["types.MessageStory", "types.Story"] = None,
        alternative_videos: List["types.AlternativeVideo"] = None,
        video: "types.Video" = None,
        voice: "types.Voice" = None,
        video_note: "types.VideoNote" = None,
        web_page_preview: "types.WebPagePreview" = None,
        caption: Str = None,
        contact: "types.Contact" = None,
        location: "types.Location" = None,
        venue: "types.Venue" = None,
        poll: "types.Poll" = None,
        dice: "types.Dice" = None,
        new_chat_members: List["types.User"] = None,
        chat_joined_by_request: "types.ChatJoinedByRequest" = None,
        left_chat_member: "types.User" = None,
        new_chat_title: str = None,
        new_chat_photo: "types.Photo" = None,
        delete_chat_photo: bool = None,
        group_chat_created: bool = None,
        supergroup_chat_created: bool = None,
        channel_chat_created: bool = None,
        migrate_to_chat_id: int = None,
        migrate_from_chat_id: int = None,
        pinned_message: "Message" = None,
        game_high_score: int = None,
        views: int = None,
        forwards: int = None,
        via_bot: "types.User" = None,
        outgoing: bool = None,
        matches: List[Match] = None,
        command: List[str] = None,
        bot_allowed: "types.BotAllowed" = None,
        chats_shared: List["types.RequestedChats"] = None,
        forum_topic_created: "types.ForumTopicCreated" = None,
        forum_topic_closed: "types.ForumTopicClosed" = None,
        forum_topic_reopened: "types.ForumTopicReopened" = None,
        forum_topic_edited: "types.ForumTopicEdited" = None,
        general_topic_hidden: "types.GeneralTopicHidden" = None,
        general_topic_unhidden: "types.GeneralTopicUnhidden" = None,
        gifted_premium: "types.GiftedPremium" = None,
        giveaway_launched: "types.GiveawayLaunched" = None,
        video_chat_scheduled: "types.VideoChatScheduled" = None,
        video_chat_started: "types.VideoChatStarted" = None,
        video_chat_ended: "types.VideoChatEnded" = None,
        video_chat_members_invited: "types.VideoChatMembersInvited" = None,
        web_app_data: "types.WebAppData" = None,
        successful_payment: "types.SuccessfulPayment" = None,
        payment_refunded: "types.PaymentRefunded" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reactions: List["types.Reaction"] = None,
        chat_join_type: "enums.ChatJoinType" = None,
        raw: "raw.types.Message" = None
    ):
        super().__init__(client)

        self.id = id
        self.message_thread_id = message_thread_id
        self.business_connection_id = business_connection_id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.sender_business_bot = sender_business_bot
        self.date = date
        self.chat = chat
        self.topic = topic
        self.forward_from = forward_from
        self.forward_sender_name = forward_sender_name
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.is_topic_message = is_topic_message
        self.reply_to_chat_id = reply_to_chat_id
        self.reply_to_message_id = reply_to_message_id
        self.reply_to_story_id = reply_to_story_id
        self.reply_to_story_user_id = reply_to_story_user_id
        self.reply_to_story_chat_id = reply_to_story_chat_id
        self.reply_to_top_message_id = reply_to_top_message_id
        self.reply_to_message = reply_to_message
        self.reply_to_story = reply_to_story
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.scheduled = scheduled
        self.from_scheduled = from_scheduled
        self.media = media
        self.edit_date = edit_date
        self.edit_hide = edit_hide
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.has_protected_content = has_protected_content
        self.has_media_spoiler = has_media_spoiler
        self.text = text
        self.entities = entities
        self.caption_entities = caption_entities
        self.quote_text = quote_text
        self.quote_entities = quote_entities
        self.effect_id = effect_id
        self.invert_media = invert_media
        self.audio = audio
        self.document = document
        self.photo = photo
        self.paid_media = paid_media
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.gifted_premium = gifted_premium
        self.giveaway = giveaway
        self.giveaway_result = giveaway_result
        self.boosts_applied = boosts_applied
        self.chat_theme_updated = chat_theme_updated
        self.chat_wallpaper_updated = chat_wallpaper_updated
        self.contact_registered = contact_registered
        self.gift_code = gift_code
        self.gift = gift
        self.screenshot_taken = screenshot_taken
        self.invoice = invoice
        self.story = story
        self.video = video
        self.alternative_videos = alternative_videos
        self.voice = voice
        self.video_note = video_note
        self.web_page_preview = web_page_preview
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.poll = poll
        self.dice = dice
        self.new_chat_members = new_chat_members
        self.chat_joined_by_request = chat_joined_by_request
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.game_high_score = game_high_score
        self.views = views
        self.forwards = forwards
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.matches = matches
        self.command = command
        self.reply_markup = reply_markup
        self.bot_allowed = bot_allowed
        self.chats_shared = chats_shared
        self.forum_topic_created = forum_topic_created
        self.forum_topic_closed = forum_topic_closed
        self.forum_topic_reopened = forum_topic_reopened
        self.forum_topic_edited = forum_topic_edited
        self.general_topic_hidden = general_topic_hidden
        self.general_topic_unhidden = general_topic_unhidden
        self.giveaway_launched = giveaway_launched
        self.video_chat_scheduled = video_chat_scheduled
        self.video_chat_started = video_chat_started
        self.video_chat_ended = video_chat_ended
        self.video_chat_members_invited = video_chat_members_invited
        self.web_app_data = web_app_data
        self.successful_payment = successful_payment
        self.payment_refunded = payment_refunded
        self.reactions = reactions
        self.chat_join_type = chat_join_type
        self.raw = raw

    async def wait_for_click(
            self,
            from_user_id: Optional[Union[Union[int, str], List[Union[int, str]]]] = None,
            timeout: Optional[int] = None,
            filters=None,
            alert: Union[str, bool] = True,
    ):
        """Waits for a callback query to be clicked on the message.

        Parameters:
            user_id (``int`` | ``str`` | Iterable of ``int`` | Iterable of ``str``, *optional*):
                The user ID to listen for.

            timeout (``int``, *optional*):
                The maximum amount of time to wait for a message.

            filters (:obj:`~pyrogram.filters`, *optional*):
                A filter to check the incoming message against.

            alert (``str`` | ``bool``):
                The alert to show when the button is clicked by users that are not allowed in from_user_id.

        Returns:
            :obj:`~pyrogram.types.CallbackQuery`: The callback query that was clicked.
        """
        message_id = getattr(self, "id", getattr(self, "message_id", None))

        return await self._client.listen(
            filters=filters,
            timeout=timeout,
            listener_type=pyrogram.enums.ListenerTypes.CALLBACK_QUERY,
            unallowed_click_alert=alert,
            chat_id=self.chat.id,
            user_id=from_user_id,
            message_id=message_id,
        )

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        message: raw.base.Message,
        users: dict,
        chats: dict,
        topics: dict = None,
        is_scheduled: bool = False,
        business_connection_id: str = None,
        replies: int = 1
    ):
        if isinstance(message, raw.types.MessageEmpty):
            return Message(id=message.id, empty=True, client=client, raw=message)

        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        user_id = from_id or peer_id

        if isinstance(message.from_id, raw.types.PeerUser) and isinstance(message.peer_id, raw.types.PeerUser):
            if from_id not in users or peer_id not in users:
                try:
                    r = await client.invoke(
                        raw.functions.users.GetUsers(
                            id=[
                                await client.resolve_peer(from_id),
                                await client.resolve_peer(peer_id)
                            ]
                        )
                    )
                except PeerIdInvalid:
                    pass
                else:
                    users.update({i.id: i for i in r})

        if isinstance(message, raw.types.MessageService):
            message_thread_id = None
            action = message.action

            new_chat_members = None
            chat_joined_by_request = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            channel_chat_created = None
            new_chat_photo = None
            bot_allowed = None
            chats_shared = None
            is_topic_message = None
            forum_topic_created = None
            forum_topic_closed = None
            forum_topic_reopened = None
            forum_topic_edited = None
            general_topic_hidden = None
            general_topic_unhidden = None
            video_chat_scheduled = None
            video_chat_started = None
            video_chat_ended = None
            video_chat_members_invited = None
            web_app_data = None
            gifted_premium = None
            giveaway_launched = None
            giveaway_result = None
            successful_payment = None
            payment_refunded = None
            boosts_applied = None
            chat_theme_updated = None
            chat_wallpaper_updated = None
            contact_registered = None
            gift_code = None
            gift = None
            screenshot_taken = None

            service_type = None
            chat_join_type = None

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            if isinstance(action, raw.types.MessageActionChatAddUser):
                new_chat_members = [types.User._parse(client, users[i]) for i in action.users]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_ADD
            elif isinstance(action, raw.types.MessageActionChatJoinedByLink):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_LINK
            elif isinstance(action, raw.types.MessageActionChatJoinedByRequest):
                chat_joined_by_request = types.ChatJoinedByRequest()
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_REQUEST
            elif isinstance(action, raw.types.MessageActionChatDeleteUser):
                left_chat_member = types.User._parse(client, users[action.user_id])
                service_type = enums.MessageServiceType.LEFT_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatEditTitle):
                new_chat_title = action.title
                service_type = enums.MessageServiceType.NEW_CHAT_TITLE
            elif isinstance(action, raw.types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
                service_type = enums.MessageServiceType.DELETE_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
                service_type = enums.MessageServiceType.MIGRATE_TO_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
                service_type = enums.MessageServiceType.MIGRATE_FROM_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChatCreate):
                group_chat_created = True
                service_type = enums.MessageServiceType.GROUP_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChannelCreate):
                channel_chat_created = True
                service_type = enums.MessageServiceType.CHANNEL_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChatEditPhoto):
                new_chat_photo = types.Photo._parse(client, action.photo)
                service_type = enums.MessageServiceType.NEW_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionBotAllowed):
                bot_allowed = types.BotAllowed._parse(client, action)
                service_type = enums.MessageServiceType.BOT_ALLOWED
            elif isinstance(action, raw.types.MessageActionRequestedPeer) or isinstance(action, raw.types.MessageActionRequestedPeerSentMe):
                chats_shared = await types.RequestedChats._parse(client, action)
                service_type = enums.MessageServiceType.ChatShared
            elif isinstance(action, raw.types.MessageActionTopicCreate):
                forum_topic_created = types.ForumTopicCreated._parse(message)
                service_type = enums.MessageServiceType.FORUM_TOPIC_CREATED
            elif isinstance(action, raw.types.MessageActionTopicEdit):
                if action.title:
                    forum_topic_edited = types.ForumTopicEdited._parse(action)
                    service_type = enums.MessageServiceType.FORUM_TOPIC_EDITED
                elif action.hidden:
                    general_topic_hidden = types.GeneralTopicHidden()
                    service_type = enums.MessageServiceType.GENERAL_TOPIC_HIDDEN
                elif action.closed:
                    forum_topic_closed = types.ForumTopicClosed()
                    service_type = enums.MessageServiceType.FORUM_TOPIC_CLOSED
                else:
                    if hasattr(action, "hidden") and action.hidden is not None:
                        general_topic_unhidden = types.GeneralTopicUnhidden()
                        service_type = enums.MessageServiceType.GENERAL_TOPIC_UNHIDDEN
                    else:
                        forum_topic_reopened = types.ForumTopicReopened()
                        service_type = enums.MessageServiceType.FORUM_TOPIC_REOPENED
            elif isinstance(action, raw.types.MessageActionGroupCallScheduled):
                video_chat_scheduled = types.VideoChatScheduled._parse(action)
                service_type = enums.MessageServiceType.VIDEO_CHAT_SCHEDULED
            elif isinstance(action, raw.types.MessageActionGroupCall):
                if action.duration:
                    video_chat_ended = types.VideoChatEnded._parse(action)
                    service_type = enums.MessageServiceType.VIDEO_CHAT_ENDED
                else:
                    video_chat_started = types.VideoChatStarted()
                    service_type = enums.MessageServiceType.VIDEO_CHAT_STARTED
            elif isinstance(action, raw.types.MessageActionInviteToGroupCall):
                video_chat_members_invited = types.VideoChatMembersInvited._parse(client, action, users)
                service_type = enums.MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED
            elif isinstance(action, raw.types.MessageActionWebViewDataSentMe):
                web_app_data = types.WebAppData._parse(action)
                service_type = enums.MessageServiceType.WEB_APP_DATA
            elif isinstance(action, raw.types.MessageActionGiftPremium):
                gifted_premium = await types.GiftedPremium._parse(client, action, from_user.id)
                service_type = enums.MessageServiceType.GIFTED_PREMIUM
            elif isinstance(action, raw.types.MessageActionGiveawayLaunch):
                giveaway_launched = types.GiveawayLaunched._parse(client, action)
                service_type = enums.MessageServiceType.GIVEAWAY_LAUNCHED
            elif isinstance(action, raw.types.MessageActionGiveawayResults):
                giveaway_result = await types.GiveawayResult._parse(client, action, True)
                service_type = enums.MessageServiceType.GIVEAWAY_RESULT
            elif isinstance(action, raw.types.MessageActionBoostApply):
                boosts_applied = action.boosts
                service_type = enums.MessageServiceType.BOOST_APPLY
            elif isinstance(action, (raw.types.MessageActionPaymentSent, raw.types.MessageActionPaymentSentMe)):
                successful_payment = types.SuccessfulPayment._parse(client, action)
                service_type = enums.MessageServiceType.SUCCESSFUL_PAYMENT
            elif isinstance(action, raw.types.MessageActionPaymentRefunded):
                payment_refunded = await types.PaymentRefunded._parse(client, action)
                service_type = enums.MessageServiceType.PAYMENT_REFUNDED
            elif isinstance(action, raw.types.MessageActionSetChatTheme):
                chat_theme_updated = types.ChatTheme._parse(action)
                service_type = enums.MessageServiceType.CHAT_THEME_UPDATED
            elif isinstance(action, raw.types.MessageActionSetChatWallPaper):
                chat_wallpaper_updated = types.ChatWallpaper._parse(client, action)
                service_type = enums.MessageServiceType.CHAT_WALLPAPER_UPDATED
            elif isinstance(action, raw.types.MessageActionContactSignUp):
                contact_registered = types.ContactRegistered()
                service_type = enums.MessageServiceType.CONTACT_REGISTERED
            elif isinstance(action, raw.types.MessageActionGiftCode):
                gift_code = types.GiftCode._parse(client, action, chats)
                service_type = enums.MessageServiceType.GIFT_CODE
            elif isinstance(action, (raw.types.MessageActionStarGift, raw.types.MessageActionStarGiftUnique)):
                gift = await types.Gift._parse_action(client, message, users, chats)
                service_type = enums.MessageServiceType.GIFT
            elif isinstance(action, raw.types.MessageActionScreenshotTaken):
                screenshot_taken = types.ScreenshotTaken()
                service_type = enums.MessageServiceType.SCREENSHOT_TAKEN

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                topic=None,
                from_user=from_user,
                service=service_type,
                new_chat_members=new_chat_members,
                chat_joined_by_request=chat_joined_by_request,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=utils.get_channel_id(migrate_to_chat_id) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                bot_allowed=bot_allowed,
                channel_chat_created=channel_chat_created,
                chats_shared=chats_shared,
                is_topic_message=is_topic_message,
                forum_topic_created=forum_topic_created,
                forum_topic_closed=forum_topic_closed,
                forum_topic_reopened=forum_topic_reopened,
                forum_topic_edited=forum_topic_edited,
                general_topic_hidden=general_topic_hidden,
                general_topic_unhidden=general_topic_unhidden,
                video_chat_scheduled=video_chat_scheduled,
                video_chat_started=video_chat_started,
                video_chat_ended=video_chat_ended,
                video_chat_members_invited=video_chat_members_invited,
                web_app_data=web_app_data,
                gifted_premium=gifted_premium,
                giveaway_launched=giveaway_launched,
                giveaway_result=giveaway_result,
                successful_payment=successful_payment,
                gift=gift,
                payment_refunded=payment_refunded,
                boosts_applied=boosts_applied,
                chat_theme_updated=chat_theme_updated,
                chat_wallpaper_updated=chat_wallpaper_updated,
                contact_registered=contact_registered,
                gift_code=gift_code,
                screenshot_taken=screenshot_taken,
                raw=message,
                chat_join_type=chat_join_type,
                client=client
                # TODO: supergroup_chat_created
            )
            if parsed_message.chat.type is not enums.ChatType.CHANNEL:
                parsed_message.sender_chat = sender_chat

            if isinstance(action, raw.types.MessageActionPinMessage):
                try:
                    parsed_message.pinned_message = await client.get_messages(
                        parsed_message.chat.id,
                        reply_to_message_ids=message.id,
                        replies=0
                    )

                    parsed_message.service = enums.MessageServiceType.PINNED_MESSAGE
                except MessageIdsEmpty:
                    pass

            if isinstance(action, raw.types.MessageActionGameScore):
                parsed_message.game_high_score = types.GameHighScore._parse_action(client, message, users)

                if message.reply_to and replies:
                    try:
                        parsed_message.reply_to_message = await client.get_messages(
                            parsed_message.chat.id,
                            reply_to_message_ids=message.id,
                            replies=0
                        )

                        parsed_message.service = enums.MessageServiceType.GAME_HIGH_SCORE
                    except MessageIdsEmpty:
                        pass

            client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            if message.reply_to:
                if message.reply_to.forum_topic:
                    if message.reply_to.reply_to_top_id:
                        parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                    else:
                        parsed_message.message_thread_id = message.reply_to.reply_to_msg_id
                    parsed_message.is_topic_message = True
            elif parsed_message.chat.is_forum and parsed_message.message_thread_id is None:
                parsed_message.message_thread_id = 1
                parsed_message.is_topic_message = True

            return parsed_message

        if isinstance(message, raw.types.Message):
            message_thread_id = None
            entities = [types.MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))

            sender_business_bot = None
            forward_from = None
            forward_sender_name = None
            forward_from_chat = None
            forward_from_message_id = None
            forward_signature = None
            forward_date = None
            is_topic_message = None

            forward_header = message.fwd_from  # type: raw.types.MessageFwdHeader

            if forward_header:
                forward_date = utils.timestamp_to_datetime(forward_header.date)

                if forward_header.from_id:
                    raw_peer_id = utils.get_raw_peer_id(forward_header.from_id)
                    peer_id = utils.get_peer_id(forward_header.from_id)

                    if peer_id > 0:
                        forward_from = types.User._parse(client, users[raw_peer_id])
                    else:
                        forward_from_chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])
                        forward_from_message_id = forward_header.channel_post
                        forward_signature = forward_header.post_author
                elif forward_header.from_name:
                    forward_sender_name = forward_header.from_name

            photo = None
            paid_media = None
            location = None
            contact = None
            venue = None
            game = None
            giveaway = None
            giveaway_result = None
            invoice = None
            story = None
            audio = None
            voice = None
            animation = None
            video = None
            alternative_videos = []
            video_note = None
            web_page_preview = None
            sticker = None
            document = None
            poll = None
            dice = None

            media = message.media
            media_type = None
            has_media_spoiler = None

            if media:
                if isinstance(media, raw.types.MessageMediaPhoto):
                    photo = types.Photo._parse(client, media.photo, media.ttl_seconds)
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw.types.MessageMediaGeo):
                    location = types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw.types.MessageMediaContact):
                    contact = types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw.types.MessageMediaVenue):
                    venue = types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw.types.MessageMediaGame):
                    game = types.Game._parse(client, message)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw.types.MessageMediaGiveaway):
                    giveaway = await types.Giveaway._parse(client, message)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw.types.MessageMediaGiveawayResults):
                    giveaway_result = await types.GiveawayResult._parse(client, message.media)
                    media_type = enums.MessageMediaType.GIVEAWAY_RESULT
                elif isinstance(media, raw.types.MessageMediaStory):
                    story = await types.MessageStory._parse(client, media)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw.types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, raw.types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                raw.types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if raw.types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                            animation = types.Animation._parse(client, doc, video_attributes, file_name)
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeSticker in attributes:
                            sticker = await types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw.types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = types.VideoNote._parse(client, doc, video_attributes)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = types.Video._parse(client, doc, video_attributes, file_name, media.ttl_seconds, media.video_cover, media.video_timestamp)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler

                                altdocs = media.alt_documents or []
                                for altdoc in altdocs:
                                    if isinstance(altdoc, raw.types.Document):
                                        altdoc_attributes = {type(i): i for i in altdoc.attributes}

                                        altdoc_file_name = getattr(
                                            altdoc_attributes.get(
                                                raw.types.DocumentAttributeFilename, None
                                            ), "file_name", None
                                        )
                                        altdoc_video_attribute = altdoc_attributes.get(raw.types.DocumentAttributeVideo, None)
                                        if altdoc_video_attribute:
                                            alternative_videos.append(
                                                types.AlternativeVideo._parse(client, altdoc, altdoc_video_attribute, altdoc_file_name)
                                            )
                        elif raw.types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = types.Voice._parse(client, doc, audio_attributes)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = types.Audio._parse(client, doc, audio_attributes, file_name)
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = types.Document._parse(client, doc, file_name)
                            media_type = enums.MessageMediaType.DOCUMENT
                elif isinstance(media, raw.types.MessageMediaWebPage):
                    if isinstance(media.webpage, raw.types.WebPage) or isinstance(media.webpage, raw.types.WebPageEmpty):
                        web_page_preview = types.WebPagePreview._parse(client, media, message.invert_media)
                        media_type = enums.MessageMediaType.WEB_PAGE_PREVIEW
                    else:
                        media = None
                elif isinstance(media, raw.types.MessageMediaPoll):
                    poll = await types.Poll._parse(client, media, users)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw.types.MessageMediaDice):
                    dice = types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                elif isinstance(media, raw.types.MessageMediaInvoice):
                    invoice = types.Invoice._parse(media)
                    media = enums.MessageMediaType.INVOICE
                elif isinstance(media, raw.types.MessageMediaPaidMedia):
                    paid_media = types.PaidMedia._parse(client, media)
                    media_type = enums.MessageMediaType.PAID_MEDIA
                else:
                    media = None

            reply_markup = message.reply_markup

            if reply_markup:
                if isinstance(reply_markup, raw.types.ReplyKeyboardForceReply):
                    reply_markup = types.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardMarkup):
                    reply_markup = types.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyInlineMarkup):
                    reply_markup = types.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardHide):
                    reply_markup = types.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            reactions = types.MessageReactions._parse(client, message.reactions, users)

            if message.via_business_bot_id:
                sender_business_bot = types.User._parse(client, users.get(message.via_business_bot_id, None))

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                business_connection_id=business_connection_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                topic=None,
                from_user=from_user,
                sender_business_bot=sender_business_bot,
                text=(
                    Str(message.message).init(entities) or None
                    if media is None or web_page_preview is not None
                    else None
                ),
                caption=(
                    Str(message.message).init(entities) or None
                    if media is not None and web_page_preview is None
                    else None
                ),
                entities=(
                    entities or None
                    if media is None or web_page_preview is not None
                    else None
                ),
                caption_entities=(
                    entities or None
                    if media is not None and web_page_preview is None
                    else None
                ),
                author_signature=message.post_author,
                has_protected_content=message.noforwards,
                has_media_spoiler=has_media_spoiler,
                forward_from=forward_from,
                forward_sender_name=forward_sender_name,
                forward_from_chat=forward_from_chat,
                forward_from_message_id=forward_from_message_id,
                forward_signature=forward_signature,
                forward_date=forward_date,
                is_topic_message=is_topic_message,
                mentioned=message.mentioned,
                scheduled=is_scheduled,
                from_scheduled=message.from_scheduled,
                media=media_type,
                edit_hide=message.edit_hide,
                edit_date=utils.timestamp_to_datetime(message.edit_date),
                media_group_id=message.grouped_id,
                invert_media=message.invert_media,
                photo=photo,
                paid_media=paid_media,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                giveaway=giveaway,
                giveaway_result=giveaway_result,
                invoice=invoice,
                story=story,
                video=video,
                alternative_videos=types.List(alternative_videos) if alternative_videos else None,
                video_note=video_note,
                web_page_preview=web_page_preview,
                sticker=sticker,
                document=document,
                poll=poll,
                dice=dice,
                views=message.views,
                forwards=message.forwards,
                via_bot=types.User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                reply_markup=reply_markup,
                reactions=reactions,
                effect_id=getattr(message, "effect", None),
                raw=message,
                client=client
            )
            if parsed_message.chat.type is not enums.ChatType.CHANNEL:
                parsed_message.sender_chat = sender_chat

            if message.reply_to:
                if isinstance(message.reply_to, raw.types.MessageReplyHeader):
                    parsed_message.quote_text = message.reply_to.quote_text
                    if len(message.reply_to.quote_entities) > 0:
                        quote_entities = [types.MessageEntity._parse(client, entity, users) for entity in message.reply_to.quote_entities]
                        parsed_message.quote_entities = types.List(filter(lambda x: x is not None, quote_entities))
                    if message.reply_to.forum_topic:
                        if message.reply_to.reply_to_top_id:
                            thread_id = message.reply_to.reply_to_top_id
                            parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        else:
                            thread_id = message.reply_to.reply_to_msg_id
                        parsed_message.message_thread_id = thread_id
                        parsed_message.is_topic_message = True
                        if topics:
                            parsed_message.topic = types.ForumTopic._parse(topics[thread_id])
                        else:
                            try:
                                msg = await client.get_messages(parsed_message.chat.id,message.id)
                                if getattr(msg, "topic"):
                                    parsed_message.topic = msg.topic
                            except Exception:
                                pass
                    else:
                        parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        parsed_message.reply_to_top_message_id = message.reply_to.reply_to_top_id
                else:
                    parsed_message.reply_to_story_id = message.reply_to.story_id
                    if isinstance(message.reply_to.peer, raw.types.PeerUser):
                        parsed_message.reply_to_story_user_id = message.reply_to.peer.user_id
                    elif isinstance(message.reply_to.peer, raw.types.PeerChat):
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.chat_id)
                    else:
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.channel_id)
                rtci = getattr(message.reply_to, "reply_to_peer_id", None)
                reply_to_chat_id = utils.get_channel_id(utils.get_raw_peer_id(rtci)) if rtci else None
                if rtci is not None and parsed_message.chat.id != reply_to_chat_id:
                    parsed_message.reply_to_chat_id = reply_to_chat_id

                if replies:
                    if parsed_message.reply_to_message_id:
                        if rtci is not None and parsed_message.chat.id != reply_to_chat_id:
                            key = (reply_to_chat_id, message.reply_to.reply_to_msg_id)
                            reply_to_params = {"chat_id": key[0], 'message_ids': key[1]}
                        else:
                            key = (parsed_message.chat.id, parsed_message.reply_to_message_id)
                            reply_to_params = {'chat_id': key[0], 'reply_to_message_ids': message.id}

                        try:
                            reply_to_message = client.message_cache[key]

                            if not reply_to_message:
                                reply_to_message = await client.get_messages(
                                    replies=replies - 1,
                                    **reply_to_params
                                )
                            if reply_to_message and not reply_to_message.forum_topic_created:
                                parsed_message.reply_to_message = reply_to_message
                        except MessageIdsEmpty:
                            pass
                        except ChannelPrivate:
                            pass
                    elif parsed_message.reply_to_story_id:
                        try:
                            reply_to_story = await client.get_stories(
                                parsed_message.reply_to_story_user_id or parsed_message.reply_to_story_chat_id,
                                parsed_message.reply_to_story_id
                            )
                        except Exception:
                            pass
                        else:
                            parsed_message.reply_to_story = reply_to_story
            if parsed_message.chat.is_forum and parsed_message.message_thread_id is None:
                parsed_message.message_thread_id = 1
                parsed_message.is_topic_message = True

            if not parsed_message.poll:  # Do not cache poll messages
                client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            return parsed_message

    @property
    def link(self) -> str:
        if (
            self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)
            and self.chat.username
        ):
            return f"https://t.me/{self.chat.username}/{self.id}"
        else:
            return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"

    @property
    def content(self) -> str:
        return self.text or self.caption or Str("").init([])
    
    async def get_media_group(self) -> List["types.Message"]:
        """Bound method *get_media_group* of :obj:`~pyrogram.types.Message`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.get_media_group(
                chat_id=message.chat.id,
                message_id=message.id
            )
            
        Example:
            .. code-block:: python

                await message.get_media_group()
                
        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of messages of the media group is returned.
            
        Raises:
            ValueError: In case the passed message id doesn't belong to a media group.
        """

        return await self._client.get_media_group(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def reply_text(
        self,
        text: str,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        invert_media: bool = None,
        reply_markup=None
    ) -> "Message":
        """Bound method *reply_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *reply*.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text="hello",
                reply_to_message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.reply_text("hello", quote=True)

        Parameters:
            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id (``int`` | ``str``, *optional*):
                Unique identifier for the origin chat.
                for reply to message from another chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            invert_media (``bool``, *optional*):
                Move web page preview to above the message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            invert_media=invert_media,
            reply_markup=reply_markup
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        quote: bool = None,
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
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_animation* :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_animation(
                chat_id=message.chat.id,
                animation=animation
            )

        Example:
            .. code-block:: python

                await message.reply_animation(animation)

        Parameters:
            animation (``str``):
                Animation to send.
                Pass a file_id as string to send an animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an animation from the Internet, or
                pass a file path as string to upload a new animation that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id (``int`` | ``str``, *optional*):
                Unique identifier for the origin chat.
                for reply to message from another chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            invert_media (``bool``, *optional*):
                True to invert the animation and caption position..

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_animation(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_audio* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_audio(
                chat_id=message.chat.id,
                audio=audio
            )

        Example:
            .. code-block:: python

                await message.reply_audio(audio)

        Parameters:
            audio (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio file from the Internet, or
                pass a file path as string to upload a new audio file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_audio(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_cached_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id
            )

        Example:
            .. code-block:: python

                await message.reply_cached_media(file_id)

        Parameters:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_cached_media(
            chat_id=chat_id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_chat_action(
        self,
        action: "enums.ChatAction",
        business_connection_id: str = None,
        emoji: str = None,
        emoji_message_id: int = None,
        emoji_message_interaction: "raw.types.DataJSON" = None
    ) -> bool:
        """Bound method *reply_chat_action* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            from pyrogram import enums

            await client.send_chat_action(
                chat_id=message.chat.id,
                action=enums.ChatAction.TYPING
            )

        Example:
            .. code-block:: python

                from pyrogram import enums

                await message.reply_chat_action(enums.ChatAction.TYPING)

        Parameters:
            action (:obj:`~pyrogram.enums.ChatAction`):
                Type of action to broadcast.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            emoji (``str``, *optional*):
                The animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION` and :obj:`~pyrogram.enums.ChatAction.WATCH_EMOJI_ANIMATION`.

            emoji_message_id (``int``, *optional*):
                Message identifier of the message containing the animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

            emoji_message_interaction (:obj:`raw.types.DataJSON`, *optional*):
                Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided string is not a valid chat action.
        """
        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        return await self._client.send_chat_action(
            chat_id=self.chat.id,
            business_connection_id=business_connection_id,
            action=action,
            emoji=emoji,
            emoji_message_id=emoji_message_id,
            emoji_message_interaction=emoji_message_interaction
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        quote: bool = None,
        last_name: str = "",
        vcard: str = "",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_contact* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_contact(
                chat_id=message.chat.id,
                phone_number=phone_number,
                first_name=first_name
            )

        Example:
            .. code-block:: python

                await message.reply_contact("+1-123-456-7890", "Name")

        Parameters:
            phone_number (``str``):
                Contact's phone number.

            first_name (``str``):
                Contact's first name.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            last_name (``str``, *optional*):
                Contact's last name.

            vcard (``str``, *optional*):
                Additional data about the contact in the form of a vCard, 0-2048 bytes

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_contact(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            business_connection_id=business_connection_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

    async def reply_document(
        self,
        document: Union[str, BinaryIO],
        quote: bool = None,
        thumb: Union[str, BinaryIO] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        file_name: str = None,
        force_document: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_document* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_document(
                chat_id=message.chat.id,
                document=document
            )

        Example:
            .. code-block:: python

                await message.reply_document(document)

        Parameters:
            document (``str``):
                File to send.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a file from the Internet, or
                pass a file path as string to upload a new file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            file_name (``str``, *optional*):
                File name of the document sent.
                Defaults to file's path basename.

            force_document (``bool``, *optional*):
                Pass True to force sending files as document. Useful for video files that need to be sent as
                document messages instead of video messages.
                Defaults to False.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.
            
            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_document(
            chat_id=chat_id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            file_name=file_name,
            force_document=force_document,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            schedule_date=schedule_date,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_game(
        self,
        game_short_name: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_game* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_game(
                chat_id=message.chat.id,
                game_short_name="lumberjack"
            )

        Example:
            .. code-block:: python

                await message.reply_game("lumberjack")

        Parameters:
            game_short_name (``str``):
                Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An object for an inline keyboard. If empty, one ‘Play game_title’ button will be shown automatically.
                If not empty, the first button must launch the game.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        return await self._client.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None
    ) -> "Message":
        """Bound method *reply_inline_bot_result* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=query_id,
                result_id=result_id
            )

        Example:
            .. code-block:: python

                await message.reply_inline_bot_result(query_id, result_id)

        Parameters:
            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        return await self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: bool = None,
        horizontal_accuracy: float = None,
        # TODO
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_location* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_location(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude
            )

        Example:
            .. code-block:: python

                await message.reply_location(latitude, longitude)

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            horizontal_accuracy (``float``, *optional*):
                The radius of uncertainty for the location, measured in meters; 0-1500.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_location(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            parse_mode=parse_mode,
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
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        business_connection_id: str = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        invert_media: bool = None
    ) -> List["types.Message"]:
        """Bound method *reply_media_group* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_media_group(
                chat_id=message.chat.id,
                media=list_of_media
            )

        Example:
            .. code-block:: python

                await message.reply_media_group(list_of_media)

        Parameters:
            media (``list``):
                A list containing either :obj:`~pyrogram.types.InputMediaPhoto` or
                :obj:`~pyrogram.types.InputMediaVideo` objects
                describing photos and videos to be sent, must include 2–10 items.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.                

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

        Returns:
            On success, a :obj:`~pyrogram.types.Messages` object is returned containing all the
            single messages sent.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_media_group(
            chat_id=chat_id,
            media=media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            invert_media=invert_media
        )

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        view_once: bool = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_photo* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo
            )

        Example:
            .. code-block:: python

                await message.reply_photo(photo)

        Parameters:
            photo (``str``):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet, or
                pass a file path as string to upload a new photo that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            view_once (``bool``, *optional*):
                Self-Destruct Timer.
                If True, the photo will self-destruct after it was viewed.

            invert_media (``bool``, *optional*):
                Pass True to invert the photo and caption position.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            view_once=view_once,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_poll(
        self,
        question: str,
        options: List["types.PollOption"],
        question_entities: List["types.MessageEntity"] = None,
        is_anonymous: bool = True,
        type: "enums.PollType" = enums.PollType.REGULAR,
        allows_multiple_answers: bool = None,
        correct_option_id: int = None,
        explanation: str = None,
        explanation_parse_mode: "enums.ParseMode" = None,
        explanation_entities: List["types.MessageEntity"] = None,
        open_period: int = None,
        close_date: datetime = None,
        is_closed: bool = None,
        quote: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_poll* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_poll(
                chat_id=message.chat.id,
                question="This is a poll",
                options=[
                    PollOption("A"),
                    PollOption("B"),
                    PollOption("C")
                ]
            )

        Example:
            .. code-block:: python

                await message.reply_poll(
                    "This is a poll",
                    [
                        PollOption("A"),
                        PollOption("B"),
                        PollOption("C")
                    ]
                )

        Parameters:
            question (``str``):
                Poll question, 1-255 characters.

            options (List of :obj:`~pyrogram.types.PollOption`):
                List of PollOption.

            question_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in the poll question, which can be specified instead of *parse_mode*.

            is_anonymous (``bool``, *optional*):
                True, if the poll needs to be anonymous.
                Defaults to True.

            type (:obj`~pyrogram.enums.PollType`, *optional*):
                Poll type, :obj:`~pyrogram.enums.PollType.QUIZ` or :obj:`~pyrogram.enums.PollType.REGULAR`.
                Defaults to :obj:`~pyrogram.enums.PollType.REGULAR`.

            allows_multiple_answers (``bool``, *optional*):
                True, if the poll allows multiple answers, ignored for polls in quiz mode.
                Defaults to False.

            correct_option_id (``int``, *optional*):
                0-based identifier of the correct answer option, required for polls in quiz mode.

            explanation (``str``, *optional*):
                Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style
                poll, 0-200 characters with at most 2 line feeds after entities parsing.

            explanation_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            explanation_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll explanation, which can be specified instead of
                *parse_mode*.

            open_period (``int``, *optional*):
                Amount of time in seconds the poll will be active after creation, 5-600.
                Can't be used together with *close_date*.

            close_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the poll will be automatically closed.
                Must be at least 5 and no more than 600 seconds in the future.
                Can't be used together with *open_period*.

            is_closed (``bool``, *optional*):
                Pass True, if the poll needs to be immediately closed.
                This can be useful for poll preview.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            question_entities=question_entities,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_thread_id=message_thread_id,
            business_connection_id=business_connection_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            parse_mode=parse_mode,
            schedule_date=schedule_date,
            reply_markup=reply_markup
        )

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        quote: bool = None,
        emoji: str = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_sticker* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=sticker
            )

        Example:
            .. code-block:: python

                await message.reply_sticker(sticker)

        Parameters:
            sticker (``str``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet, or
                pass a file path as string to upload a new sticker that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            emoji (``str``, *optional*):
                Emoji associated with the sticker; only for just uploaded stickers

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            emoji=emoji,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        quote: bool = None,
        foursquare_id: str = "",
        foursquare_type: str = "",
        # TODO
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_venue* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_venue(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude,
                title="Venue title",
                address="Venue address"
            )

        Example:
            .. code-block:: python

                await message.reply_venue(latitude, longitude, "Venue title", "Venue address")

        Parameters:
            latitude (``float``):
                Latitude of the venue.

            longitude (``float``):
                Longitude of the venue.

            title (``str``):
                Name of the venue.

            address (``str``):
                Address of the venue.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            foursquare_id (``str``, *optional*):
                Foursquare identifier of the venue.

            foursquare_type (``str``, *optional*):
                Foursquare type of the venue, if known.
                (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_venue(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        quote: bool = None,
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
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        cover: Union[str, BinaryIO] = None,
        start_timestamp: int = None,
        schedule_date: datetime = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video(
                chat_id=message.chat.id,
                video=video
            )

        Example:
            .. code-block:: python

                await message.reply_video(video)

        Parameters:
            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots.

            cover (``str`` | ``BinaryIO``, *optional*):
                Video cover.
                Pass a file_id as string to attach a photo that exists on the Telegram servers,
                pass a HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new photo civer that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.
            
            start_timestamp (``int``, *optional*):
                Timestamp from which the video playing must start, in seconds.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            invert_media (``bool``, *optional*):
                Pass True to invert the video and caption position.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_video(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            cover=cover,
            start_timestamp=start_timestamp,
            schedule_date=schedule_date,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        quote: bool = None,
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        ttl_seconds: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video_note* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video_note(
                chat_id=message.chat.id,
                video_note=video_note
            )

        Example:
            .. code-block:: python

                await message.reply_video_note(video_note)

        Parameters:
            video_note (``str``):
                Video note to send.
                Pass a file_id as string to send a video note that exists on the Telegram servers, or
                pass a file path as string to upload a new video note that exists on your local machine.
                Sending video notes by a URL is currently unsupported.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the video note will self-destruct in *ttl_seconds*
                seconds after it was viewed.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_video_note(
            chat_id=chat_id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            ttl_seconds=ttl_seconds,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_voice* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_voice(
                chat_id=message.chat.id,
                voice=voice
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

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

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

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

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
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_voice(
            chat_id=chat_id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
    async def reply_web_page(
        self,
        url: str,
        text: str = "",
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        large_media: bool = None,
        invert_media: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        business_connection_id: str = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_markup=None
    ) -> "Message":
        """Bound method *reply_web_page* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_web_page(
                chat_id=message.chat.id,
                url="https://github.com/Mayuri-Chan/pyrofork",
                reply_to_message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.reply_web_page("https://github.com/Mayuri-Chan/pyrofork")

        Parameters:
            url (``str``):
                Link that will be previewed.

            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            large_media (``bool``, *optional*):
                Make web page preview image larger.

            invert_media (``bool``, *optional*):
                Move web page preview to above the message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_in_chat_id: Union[int, str] = None,
                Unique identifier of target chat.
                for reply message in another chat.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if business_connection_id is None and self.business_connection_id:
            business_connection_id = self.business_connection_id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_web_page(
            chat_id=chat_id,
            url=url,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            large_media=large_media,
            invert_media=invert_media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            business_connection_id=business_connection_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            message_effect_id=message_effect_id,
            reply_markup=reply_markup
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None
    ) -> "Message":
        """Bound method *edit_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *edit*.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_text("hello")

        Parameters:
            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            invert_media=invert_media,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id
        )

    edit = edit_text

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None
    ) -> "Message":
        """Bound method *edit_caption* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_caption("hello")

        Parameters:
            caption (``str``):
                New caption of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            invert_media=invert_media,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id
        )

    async def edit_media(
        self,
        media: "types.InputMedia",
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None
    ) -> "Message":
        """Bound method *edit_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=media
            )

        Example:
            .. code-block:: python

                await message.edit_media(media)

        Parameters:
            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.id,
            media=media,
            invert_media=invert_media,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id
        )

    async def edit_reply_markup(
        self,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None
    ) -> "Message":
        """Bound method *edit_reply_markup* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.id,
                reply_markup=inline_reply_markup
            )

        Example:
            .. code-block:: python

                await message.edit_reply_markup(inline_reply_markup)

        Parameters:
            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
            On success, if edited message is sent by the bot, the edited
            :obj:`~pyrogram.types.Message` is returned, otherwise True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id
        )

    async def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: int = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        drop_author: bool = None,
        remove_caption: bool = None,
        new_video_start_timestamp: int = None,
    ) -> Union["types.Message", List["types.Message"]]:
        """Bound method *forward* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.forward_messages(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.forward(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs; for supergroups only

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            drop_author (``bool``, *optional*):
                Forwards messages without quoting the original author.
                
            remove_caption (``bool``, *optional*):
                Pass True to remove media captions of message copies.
                
            new_video_start_timestamp (``int``, *optional*):
                The new video start timestamp. Pass time to replace video start timestamp in the forwarded message.

        Returns:
            On success, the forwarded Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_ids=self.id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            drop_author=drop_author,
            remove_caption=remove_caption,
            new_video_start_timestamp=new_video_start_timestamp,
        )

    async def copy(
        self,
        chat_id: Union[int, str],
        caption: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_to_message_id: int = None,
        reply_to_chat_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = object
    ) -> Union["types.Message", List["types.Message"]]:
        """Bound method *copy* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.copy(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            caption (``string``, *optional*):
                New caption for media, 0-1024 characters after entities parsing.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the new caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_chat_id (``int``, *optional*):
                Unique identifier for the origin chat.
                for reply to message from another chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.
                If not specified, the original reply markup is kept.
                Pass None to remove the reply markup.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the copied message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.service:
            log.warning("Service messages cannot be copied. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.game and not await self._client.storage.is_bot():
            log.warning("Users cannot send messages with Game media type. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.empty:
            log.warning("Empty messages cannot be copied.")
        elif self.text:
            return await self._client.send_message(
                chat_id,
                text=self.text,
                entities=self.entities,
                parse_mode=enums.ParseMode.DISABLED,
                disable_web_page_preview=not self.web_page_preview,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                reply_to_chat_id=reply_to_chat_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )
        elif self.media:
            send_media = partial(
                self._client.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                reply_to_chat_id=reply_to_chat_id,
                schedule_date=schedule_date,
                has_spoiler=has_spoiler,
                protect_content=protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                invert_media=invert_media,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )

            if self.photo:
                file_id = self.photo.file_id
            elif self.audio:
                file_id = self.audio.file_id
            elif self.document:
                file_id = self.document.file_id
            elif self.video:
                file_id = self.video.file_id
            elif self.animation:
                file_id = self.animation.file_id
            elif self.voice:
                file_id = self.voice.file_id
            elif self.sticker:
                file_id = self.sticker.file_id
            elif self.video_note:
                file_id = self.video_note.file_id
            elif self.contact:
                return await self._client.send_contact(
                    chat_id,
                    phone_number=self.contact.phone_number,
                    first_name=self.contact.first_name,
                    last_name=self.contact.last_name,
                    vcard=self.contact.vcard,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast,
                )
            elif self.location:
                return await self._client.send_location(
                    chat_id,
                    latitude=self.location.latitude,
                    longitude=self.location.longitude,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast
                )
            elif self.venue:
                return await self._client.send_venue(
                    chat_id,
                    latitude=self.venue.location.latitude,
                    longitude=self.venue.location.longitude,
                    title=self.venue.title,
                    address=self.venue.address,
                    foursquare_id=self.venue.foursquare_id,
                    foursquare_type=self.venue.foursquare_type,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast
                )
            elif self.poll:
                return await self._client.send_poll(
                    chat_id,
                    question=self.poll.question,
                    options=[
                        types.PollOption(
                            text=opt.text,
                            entities=opt.entities
                        ) for opt in self.poll.options
                    ],
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast
                )
            elif self.game:
                return await self._client.send_game(
                    chat_id,
                    game_short_name=self.game.short_name,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    allow_paid_broadcast=allow_paid_broadcast
                )
            elif self.web_page_preview:
                return await self._client.send_web_page(
                    chat_id,
                    url=self.web_page_preview.webpage.url,
                    text=self.text,
                    entities=self.entities,
                    parse_mode=enums.ParseMode.DISABLED,
                    large_media=self.web_page_preview.force_large_media,
                    invert_media=self.web_page_preview.invert_media,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    reply_to_message_id=reply_to_message_id,
                    reply_to_chat_id=reply_to_chat_id,
                    quote_text=quote_text,
                    quote_entities=quote_entities,
                    schedule_date=schedule_date,
                    protect_content=protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            else:
                raise ValueError("Unknown media type")

            if self.sticker or self.video_note:  # Sticker and VideoNote should have no caption
                return await send_media(
                    file_id=file_id,
                    message_thread_id=message_thread_id,
                    allow_paid_broadcast=allow_paid_broadcast
                )
            else:
                if caption is None:
                    caption = self.caption or ""
                    caption_entities = self.caption_entities

                return await send_media(
                    file_id=file_id,
                    caption=caption,
                    parse_mode=parse_mode,
                    caption_entities=caption_entities,
                    has_spoiler=has_spoiler,
                    message_thread_id=message_thread_id,
                    allow_paid_broadcast=allow_paid_broadcast
                )
        else:
            raise ValueError("Can't copy this message")

    async def delete(self, revoke: bool = True):
        """Bound method *delete* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.delete()

        Parameters:
            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            True on success, False otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            revoke=revoke
        )

    async def click(
        self,
        x: Union[int, str] = 0,
        y: int = None,
        quote: bool = None,
        timeout: int = 10,
        request_write_access: bool = True,
        password: str = None
    ):
        """Bound method *click* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for clicking a button attached to the message instead of:

        - Clicking inline buttons:

        .. code-block:: python

            await client.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.id,
                callback_data=message.reply_markup[i][j].callback_data
            )

        - Clicking normal buttons:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text=message.reply_markup[i][j].text
            )

        Example:
            This method can be used in three different ways:

            1.  Pass one integer argument only (e.g.: ``.click(2)``, to click a button at index 2).
                Buttons are counted left to right, starting from the top.

            2.  Pass two integer arguments (e.g.: ``.click(1, 0)``, to click a button at position (1, 0)).
                The origin (0, 0) is top-left.

            3.  Pass one string argument only (e.g.: ``.click("Settings")``, to click a button by using its label).
                Only the first matching button will be pressed.

        Parameters:
            x (``int`` | ``str``):
                Used as integer index, integer abscissa (in pair with y) or as string label.
                Defaults to 0 (first button).

            y (``int``, *optional*):
                Used as ordinate only (in pair with x).

            quote (``bool``, *optional*):
                Useful for normal buttons only, where pressing it will result in a new message sent.
                If ``True``, the message will be sent as a reply to this message.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            timeout (``int``, *optional*):
                Timeout in seconds.

            request_write_access (``bool``, *optional*):
                Only used in case of :obj:`~pyrogram.types.LoginUrl` button.
                True, if the bot can send messages to the user.
                Defaults to ``True``.

            password (``str``, *optional*):
                When clicking certain buttons (such as BotFather's confirmation button to transfer ownership), if your account has 2FA enabled, you need to provide your account's password.
                The 2-step verification password for the current user. Only applicable, if the :obj:`~pyrogram.types.InlineKeyboardButton` contains ``requires_password``.

        Returns:
            -   The result of :meth:`~pyrogram.Client.request_callback_answer` in case of inline callback button clicks.
            -   The result of :meth:`~Message.reply()` in case of normal button clicks.
            -   A string in case the inline button is a URL, a *switch_inline_query* or a
                *switch_inline_query_current_chat* button.
            -   A string URL with the user details, in case of a WebApp button.
            -   A :obj:`~pyrogram.types.Chat` object in case of a ``KeyboardButtonUserProfile`` button.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided index or position is out of range or the button label was not found.
            TimeoutError: In case, after clicking an inline button, the bot fails to answer within the timeout.
        """

        if isinstance(self.reply_markup, types.ReplyKeyboardMarkup):
            keyboard = self.reply_markup.keyboard
            is_inline = False
        elif isinstance(self.reply_markup, types.InlineKeyboardMarkup):
            keyboard = self.reply_markup.inline_keyboard
            is_inline = True
        else:
            raise ValueError("The message doesn't contain any keyboard")

        if isinstance(x, int) and y is None:
            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                ][x]
            except IndexError:
                raise ValueError(f"The button at index {x} doesn't exist")
        elif isinstance(x, int) and isinstance(y, int):
            try:
                button = keyboard[y][x]
            except IndexError:
                raise ValueError(f"The button at position ({x}, {y}) doesn't exist")
        elif isinstance(x, str) and y is None:
            label = x.encode("utf-16", "surrogatepass").decode("utf-16")

            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                    if label == button.text
                ][0]
            except IndexError:
                raise ValueError(f"The button with label '{x}' doesn't exists")
        else:
            raise ValueError("Invalid arguments")

        if is_inline:
            if button.callback_data:
                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    timeout=timeout
                )
            elif button.requires_password:
                if password is None:
                    raise ValueError(
                        "This button requires a password"
                    )

                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    password=password,
                    timeout=timeout
                )
            elif button.url:
                return button.url
            elif button.web_app:
                web_app = button.web_app

                bot_peer_id = (
                    self.via_bot and
                    self.via_bot.id
                ) or (
                    self.from_user and
                    self.from_user.is_bot and
                    self.from_user.id
                ) or None

                if not bot_peer_id:
                    raise ValueError(
                        "This button requires a bot as the sender"
                    )

                r = await self._client.invoke(
                    raw.functions.messages.RequestWebView(
                        peer=await self._client.resolve_peer(self.chat.id),
                        bot=await self._client.resolve_peer(bot_peer_id),
                        url=web_app.url,
                        platform=self._client.client_platform.value,
                        # TODO
                    )
                )
                return r.url
            elif button.user_id:
                return await self._client.get_chat(
                    button.user_id,
                    force_full=False
                )
            elif button.switch_inline_query:
                return button.switch_inline_query
            elif button.switch_inline_query_current_chat:
                return button.switch_inline_query_current_chat
            else:
                raise ValueError("This button is not supported yet")
        else:
            await self.reply(text=button, quote=quote)

    async def react(self, emoji: str = "", big: bool = False, add_to_recent: bool = True) -> "types.MessageReactions":
        """Bound method *react* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_reaction(
                chat_id=chat_id,
                message_id=message.id,
                emoji="🔥"
            )

        Example:
            .. code-block:: python

                await message.react(emoji="🔥")

        Parameters:
            emoji (``str``, *optional*):
                Reaction emoji.
                Pass "" as emoji (default) to retract the reaction.
             
            big (``bool``, *optional*):
                Pass True to show a bigger and longer reaction.
                Defaults to False.
                
            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.

        Returns:
            :obj: :obj:`~pyrogram.types.MessageReactions`: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.send_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            emoji=emoji,
            big=big
        )

    async def retract_vote(
        self,
    ) -> "types.Poll":
        """Bound method *retract_vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.retract_vote(
                chat_id=message.chat.id,
                message_id=message_id,
            )

        Example:
            .. code-block:: python

                message.retract_vote()

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the retracted vote is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.retract_vote(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> str:
        """Bound method *download* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.download_media(message)

        Example:
            .. code-block:: python

                await message.download()

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

    async def vote(
        self,
        option: int,
    ) -> "types.Poll":
        """Bound method *vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.vote_poll(
                chat_id=message.chat.id,
                message_id=message.id,
                option=1
            )

        Example:
            .. code-block:: python

                message.vote(6)

        Parameters:
            option (``int``):
                Index of the poll option you want to vote for (0 to 9).

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the chosen option is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.vote_poll(
            chat_id=self.chat.id,
            message_id=self.id,
            options=option
        )

    async def pin(self, disable_notification: bool = False, both_sides: bool = False) -> "types.Message":
        """Bound method *pin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.pin()

        Parameters:
            disable_notification (``bool``):
                Pass True, if it is not necessary to send a notification to all chat members about the new pinned
                message. Notifications are always disabled in channels.

            both_sides (``bool``, *optional*):
                Pass True to pin the message for both sides (you and recipient).
                Applicable to private chats only. Defaults to False.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the service message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id,
            disable_notification=disable_notification,
            both_sides=both_sides
        )

    async def unpin(self) -> bool:
        """Bound method *unpin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.unpin()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def ask(
        self,
        text: str,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        filters=None,
        timeout: int = None
    ) -> "Message":
        """Bound method *ask* of :obj:`~pyrogram.types.Message`.
        
        Use as a shortcut for:

        .. code-block:: python

            client.send_message(chat_id, "What is your name?")

            client.wait_for_message(chat_id)

        Parameters:
            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                Pass "markdown" or "md" to enable Markdown-style parsing only.
                Pass "html" to enable HTML-style parsing only.
                Pass None to completely disable style parsing.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            filters (:obj:`Filters`):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your callback function.

            timeout (``int``, *optional*):
                Timeout in seconds.
            
        Example:
            .. code-block:: python

                message.ask("What is your name?")

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the reply message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            asyncio.TimeoutError: In case reply not received within the timeout.
        """
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        request = await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

        reply_message = await self._client.wait_for_message(
            self.chat.id,
            filters=filters,
            timeout=timeout
        )

        reply_message.request = request
        return reply_message

    async def transcribe(self) -> "types.TranscribeAudio":
        """Bound method *transcribe* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:
        
        .. code-block:: python
        
            await client.transcribe_audio(
                chat_id=message.chat.id,
                message_id=message.id
                )
        
        Example:
            .. code-block:: python
            
            await message.transcribe()
        
        Returns:
            :obj:`~pyrogram.types.TranscribeAudio`: On success.
        
        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.transcribe_audio(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def translate(
        self,
        to_language_code: str
    ) -> "types.TranslatedText":
        """Bound method *translate* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:
            .. code-block:: python

                await client.translate_message_text(
                    chat_id=message.chat.id,
                    message_ids=message_id,
                    to_language_code="en"
                )

        Example:
            .. code-block:: python

                await Message.translate("en")

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

        Returns:
            :obj:`~pyrogram.types.TranslatedText`: The translated result is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.translate_message_text(
            chat_id=self.chat.id,
            message_ids=self.id,
            to_language_code=to_language_code
        )
