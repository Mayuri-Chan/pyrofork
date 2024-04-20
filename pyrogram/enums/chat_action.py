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
from .auto_name import AutoName


class ChatAction(AutoName):
    """Chat action enumeration used in :obj:`~pyrogram.types.ChatEvent`."""

    TYPING = raw.types.SendMessageTypingAction
    "Typing text message"

    UPLOAD_PHOTO = raw.types.SendMessageUploadPhotoAction
    "Uploading photo"

    RECORD_VIDEO = raw.types.SendMessageRecordVideoAction
    "Recording video"

    UPLOAD_VIDEO = raw.types.SendMessageUploadVideoAction
    "Uploading video"

    RECORD_AUDIO = raw.types.SendMessageRecordAudioAction
    "Recording audio"

    UPLOAD_AUDIO = raw.types.SendMessageUploadAudioAction
    "Uploading audio"

    UPLOAD_DOCUMENT = raw.types.SendMessageUploadDocumentAction
    "Uploading document"

    FIND_LOCATION = raw.types.SendMessageGeoLocationAction
    "Finding location"

    RECORD_VIDEO_NOTE = raw.types.SendMessageRecordRoundAction
    "Recording video note"

    UPLOAD_VIDEO_NOTE = raw.types.SendMessageUploadRoundAction
    "Uploading video note"

    PLAYING = raw.types.SendMessageGamePlayAction
    "Playing game"

    CHOOSE_CONTACT = raw.types.SendMessageChooseContactAction
    "Choosing contact"

    SPEAKING = raw.types.SpeakingInGroupCallAction
    "Speaking in group call"

    IMPORT_HISTORY = raw.types.SendMessageHistoryImportAction
    "Importing history"

    CHOOSE_STICKER = raw.types.SendMessageChooseStickerAction
    "Choosing sticker"

    CANCEL = raw.types.SendMessageCancelAction
    "Cancel ongoing chat action"

    TRIGGER_EMOJI_ANIMATION = raw.types.SendMessageEmojiInteraction
    "User has clicked on an animated emoji triggering a `reaction <https://core.telegram.org/api/animated-emojis#emoji-reactions>`_"

    WATCH_EMOJI_ANIMATION = raw.types.SendMessageEmojiInteractionSeen
    "The user is watching animations sent by the other party by clicking on an animated emoji"
