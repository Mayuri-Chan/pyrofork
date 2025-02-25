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

from .copy_media_group import CopyMediaGroup
from .copy_message import CopyMessage
from .delete_chat_history import DeleteChatHistory
from .delete_messages import DeleteMessages
from .delete_scheduled_messages import DeleteScheduledMessages
from .download_media import DownloadMedia
from .edit_inline_caption import EditInlineCaption
from .edit_inline_media import EditInlineMedia
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_text import EditInlineText
from .edit_message_caption import EditMessageCaption
from .edit_message_media import EditMessageMedia
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessageText
from .forward_media_group import ForwardMediaGroup
from .forward_messages import ForwardMessages
from .get_available_effects import GetAvailableEffects
from .get_chat_history import GetChatHistory
from .get_chat_history_count import GetChatHistoryCount
from .get_custom_emoji_stickers import GetCustomEmojiStickers
from .get_discussion_message import GetDiscussionMessage
from .get_discussion_replies import GetDiscussionReplies
from .get_discussion_replies_count import GetDiscussionRepliesCount
from .get_media_group import GetMediaGroup
from .get_messages import GetMessages
from .get_message_read_participants import GetMessageReadParticipants
from .get_scheduled_messages import GetScheduledMessages
from .read_chat_history import ReadChatHistory
from .retract_vote import RetractVote
from .search_global import SearchGlobal
from .search_global_count import SearchGlobalCount
from .search_global_hashtag_messages import SearchGlobalHashtagMessages
from .search_global_hashtag_messages_count import SearchGlobalHashtagMessagesCount
from .search_messages import SearchMessages
from .search_messages_count import SearchMessagesCount
from .send_animation import SendAnimation
from .send_audio import SendAudio
from .send_cached_media import SendCachedMedia
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_dice import SendDice
from .send_document import SendDocument
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_photo import SendPhoto
from .send_poll import SendPoll
from .send_reaction import SendReaction
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice
from .send_web_page import SendWebPage
from .start_bot import StartBot
from .stop_poll import StopPoll
from .stream_media import StreamMedia
from .vote_poll import VotePoll
from .transcribe_audio import TranscribeAudio
from .translate_text import TranslateText

class Messages(
    DeleteChatHistory,
    DeleteMessages,
    DeleteScheduledMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageMedia,
    EditMessageText,
    ForwardMediaGroup,
    ForwardMessages,
    GetAvailableEffects,
    GetMediaGroup,
    GetMessages,
    GetMessageReadParticipants,
    GetScheduledMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SendAnimation,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendWebPage,
    SendPoll,
    VotePoll,
    StopPoll,
    RetractVote,
    DownloadMedia,
    GetChatHistory,
    SendCachedMedia,
    GetChatHistoryCount,
    ReadChatHistory,
    EditInlineText,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    SendDice,
    SearchMessages,
    SearchGlobal,
    SearchGlobalHashtagMessages,
    CopyMessage,
    CopyMediaGroup,
    SearchMessagesCount,
    SearchGlobalCount,
    SearchGlobalHashtagMessagesCount,
    GetDiscussionMessage,
    SendReaction,
    GetDiscussionReplies,
    GetDiscussionRepliesCount,
    StreamMedia,
    GetCustomEmojiStickers,
    TranscribeAudio,
    TranslateText,
    StartBot
):
    pass
