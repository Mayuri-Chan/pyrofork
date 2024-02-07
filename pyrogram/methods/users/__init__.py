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

from .block_user import BlockUser
from .delete_profile_photos import DeleteProfilePhotos
from .delete_stories import DeleteStories
from .edit_story import EditStory
from .export_story_link import ExportStoryLink
from .forward_story import ForwardStory
from .get_chat_photos import GetChatPhotos
from .get_chat_photos_count import GetChatPhotosCount
from .get_common_chats import GetCommonChats
from .get_default_emoji_statuses import GetDefaultEmojiStatuses
from .get_me import GetMe
from .get_all_stories import GetAllStories
from .get_stories import GetStories
from .get_stories_history import GetUserStoriesHistory
from .get_peer_stories import GetPeerStories
from .get_users import GetUsers
from .send_story import SendStory
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_profile import UpdateProfile


class Users(
    BlockUser,
    DeleteStories,
    EditStory,
    ExportStoryLink,
    ForwardStory,
    GetCommonChats,
    GetChatPhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    GetUsers,
    GetMe,
    GetAllStories,
    GetStories,
    GetUserStoriesHistory,
    GetPeerStories,
    SetUsername,
    GetChatPhotosCount,
    UnblockUser,
    UpdateProfile,
    GetDefaultEmojiStatuses,
    SetEmojiStatus,
    SendStory
):
    pass
