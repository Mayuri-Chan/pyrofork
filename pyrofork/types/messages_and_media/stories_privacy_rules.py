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

from pyrofork import enums, raw
from ..object import Object

class StoriesPrivacyRules(Object):
    """A story privacy.

    Parameters:
        type (:obj:`~pyrofork.enums.StoriesPrivacyRules`):
            Story privacy type.
    """

    def __init__(
        self, *,
        type: "enums.StoriesPrivacyRules"
    ):
        super().__init__()
        self.type = type

    def write(self):
        if self.type == enums.StoriesPrivacyRules.PUBLIC:
            return raw.types.InputPrivacyValueAllowAll().write()
        if self.type == enums.StoriesPrivacyRules.CLOSE_FRIENDS:
            return raw.types.InputPrivacyValueAllowCloseFriends().write()
        if self.type == enums.StoriesPrivacyRules.CONTACTS:
            return raw.types.InputPrivacyValueAllowContacts().write()
        if self.type == enums.StoriesPrivacyRules.NO_CONTACTS:
            return raw.types.InputPrivacyValueDisallowContacts().write()
        if self.type == enums.StoriesPrivacyRules.PRIVATE:
            return raw.types.InputPrivacyValueDisallowAll().write()
