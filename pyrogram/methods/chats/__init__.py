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

from .add_chat_members import AddChatMembers
from .archive_chats import ArchiveChats
from .ban_chat_member import BanChatMember
from .create_channel import CreateChannel
from .create_forum_topic import CreateForumTopic
from .create_group import CreateGroup
from .create_supergroup import CreateSupergroup
from .close_forum_topic import CloseForumTopic
from .close_general_topic import CloseGeneralTopic
from .delete_channel import DeleteChannel
from .delete_chat_photo import DeleteChatPhoto
from .delete_folder import DeleteFolder
from .delete_forum_topic import DeleteForumTopic
from .delete_supergroup import DeleteSupergroup
from .delete_user_history import DeleteUserHistory
from .edit_forum_topic import EditForumTopic
from .edit_general_topic import EditGeneralTopic
from .export_folder_link import ExportFolderLink
from .reopen_forum_topic import ReopenForumTopic
from .reopen_general_topic import ReopenGeneralTopic
from .hide_general_topic import HideGeneralTopic
from .unhide_general_topic import UnhideGeneralTopic
from .get_chat import GetChat
from .get_chat_event_log import GetChatEventLog
from .get_chat_member import GetChatMember
from .get_chat_members import GetChatMembers
from .get_chat_members_count import GetChatMembersCount
from .get_chat_online_count import GetChatOnlineCount
from .get_dialogs import GetDialogs
from .get_dialogs_count import GetDialogsCount
from .get_folders import GetFolders
from .get_forum_topics import GetForumTopics
from .get_forum_topics_by_id import GetForumTopicsByID
from .get_forum_topics_count import GetForumTopicsCount
from .get_send_as_chats import GetSendAsChats
from .join_chat import JoinChat
from .leave_chat import LeaveChat
from .mark_chat_unread import MarkChatUnread
from .pin_chat_message import PinChatMessage
from .promote_chat_member import PromoteChatMember
from .restrict_chat_member import RestrictChatMember
from .set_administrator_title import SetAdministratorTitle
from .set_chat_description import SetChatDescription
from .set_chat_permissions import SetChatPermissions
from .set_chat_photo import SetChatPhoto
from .set_chat_protected_content import SetChatProtectedContent
from .set_chat_title import SetChatTitle
from .set_chat_username import SetChatUsername
from .set_send_as_chat import SetSendAsChat
from .set_slow_mode import SetSlowMode
from .transfer_chat_ownership import TransferChatOwnership
from .unarchive_chats import UnarchiveChats
from .unban_chat_member import UnbanChatMember
from .unpin_all_chat_messages import UnpinAllChatMessages
from .unpin_chat_message import UnpinChatMessage
from .update_color import UpdateColor
from .update_folder import UpdateFolder


class Chats(
    GetChat,
    LeaveChat,
    JoinChat,
    BanChatMember,
    UnbanChatMember,
    RestrictChatMember,
    PromoteChatMember,
    GetChatMembers,
    GetChatMember,
    SetChatPhoto,
    DeleteChatPhoto,
    SetChatTitle,
    SetChatDescription,
    PinChatMessage,
    UnpinChatMessage,
    GetDialogs,
    GetChatMembersCount,
    SetChatUsername,
    SetChatPermissions,
    GetDialogsCount,
    GetFolders,
    GetForumTopics,
    GetForumTopicsByID,
    GetForumTopicsCount,
    ArchiveChats,
    UnarchiveChats,
    CreateGroup,
    CreateSupergroup,
    CreateChannel,
    CreateForumTopic,
    CloseForumTopic,
    CloseGeneralTopic,
    AddChatMembers,
    DeleteChannel,
    DeleteFolder,
    DeleteForumTopic,
    DeleteSupergroup,
    EditForumTopic,
    EditGeneralTopic,
    ExportFolderLink,
    ReopenForumTopic,
    ReopenGeneralTopic,
    HideGeneralTopic,
    UnhideGeneralTopic,
    SetAdministratorTitle,
    SetSlowMode,
    DeleteUserHistory,
    UnpinAllChatMessages,
    MarkChatUnread,
    GetChatEventLog,
    GetChatOnlineCount,
    GetSendAsChats,
    SetSendAsChat,
    SetChatProtectedContent,
    TransferChatOwnership,
    UpdateColor,
    UpdateFolder
):
    pass
